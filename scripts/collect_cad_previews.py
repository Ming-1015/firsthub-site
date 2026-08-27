#!/usr/bin/env python3
"""Generate static previews for public Onshape CAD links in FIRSTHub.

The collector opens each public share link in an isolated anonymous browser
context, discovers the current workspace and a useful assembly/part studio,
then asks Onshape for a shaded view. Only the rendered image is stored; the
original CAD URL remains the canonical source linked from the site.

Dependencies:
    python -m pip install playwright Pillow
    python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import contextlib
import hashlib
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageStat
from playwright.async_api import BrowserContext, Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright


ROOT = Path(__file__).resolve().parents[1]
DATA_JS = ROOT / "assets" / "js" / "data.js"
INDEX_HTML = ROOT / "index.html"
PREVIEW_ROOT = ROOT / "assets" / "cad-previews"
MANIFEST_PATH = PREVIEW_ROOT / "manifest.json"
DATA_PATTERN = re.compile(r"^const DATA = (.*);\s*$", re.DOTALL)
ONSHAPE_PATTERN = re.compile(
    r"^https://cad\.onshape\.com/documents/(?P<did>[0-9a-f]{24})/"
    r"(?P<wv>[wvm])/(?P<wvid>[0-9a-f]{24})/e/(?P<eid>[0-9a-f]{24})",
    re.IGNORECASE,
)

# Onshape's shaded-view API accepts a 3x4 model-to-view matrix.  This is the
# documented isometric view: model Z stays up while the camera looks down from
# the front-right corner.  FRC teams generally model the robot with Z up and
# the front aligned to a horizontal axis, making this a useful, consistent
# front three-quarter preview.  Individual records can override it with a
# ``cadPreviewViewMatrix`` value when a team's coordinate system differs.
FRONT_UPPER_VIEW_MATRIX = (
    "0.612,0.612,0,0,"
    "-0.354,0.354,0.707,0,"
    "0.707,-0.707,0.707,0"
)


def load_data() -> dict:
    match = DATA_PATTERN.match(DATA_JS.read_text(encoding="utf-8"))
    if not match:
        raise RuntimeError("Could not locate DATA payload in assets/js/data.js")
    return json.loads(match.group(1))


def save_data(data: dict) -> None:
    DATA_JS.write_text(
        "const DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    version = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    index = INDEX_HTML.read_text(encoding="utf-8")
    index = re.sub(r"assets/js/data\.js\?v=[^\"']+", f"assets/js/data.js?v={version}", index)
    INDEX_HTML.write_text(index, encoding="utf-8")


def preview_path(year: str, team: dict) -> tuple[Path, str]:
    digest = hashlib.sha256(team["cad"].encode("utf-8")).hexdigest()[:10]
    rel = Path("assets") / "cad-previews" / year / f"{team['n']}-{digest}.webp"
    return ROOT / rel, rel.as_posix()


def element_score(element: dict, requested_eid: str) -> int:
    element_type = element.get("elementType", "")
    if element_type not in {"ASSEMBLY", "PARTSTUDIO"}:
        return -10_000
    name = str(element.get("name", "")).lower()
    score = 200 if element_type == "ASSEMBLY" else 20
    # The linked tab is a useful hint, but many team posts link to a sketch or
    # a field tab beside the actual full-robot assembly.  Do not let that hint
    # outweigh a clearly named robot assembly.
    if element.get("id") == requested_eid:
        score += 100
    phrases = {
        "full robot": 400,
        "robot assembly": 350,
        "master assembly": 320,
        "main assembly": 300,
        "competition robot": 280,
        "robot": 180,
        "assembly": 40,
        "drivetrain": 20,
        "chassis": 20,
    }
    for phrase, points in phrases.items():
        if phrase in name:
            score += points
    for weak_name in (
        "bom", "layout", "test", "copy", "bearing", "wheel", "shaft",
        "sketch", "playground", "example", "field", "driver station",
    ):
        if weak_name in name:
            score -= 80
    return score


def encode_webp(image_bytes: bytes, output: Path) -> None:
    with Image.open(io.BytesIO(image_bytes)) as image:
        image.load()
        if image.width < 240 or image.height < 160:
            raise ValueError("rendered image is unexpectedly small")
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        if alpha.getbbox() is None:
            raise ValueError("rendered image is fully transparent")
        rgb = Image.new("RGB", rgba.size, (247, 247, 245))
        rgb.paste(rgba, mask=alpha)
        if max(ImageStat.Stat(rgb.resize((64, 36))).stddev) < 2.0:
            raise ValueError("rendered image appears blank")
        output.parent.mkdir(parents=True, exist_ok=True)
        rgb.save(output, "WEBP", quality=82, method=6)


async def wait_for_elements_url(page, timeout_ms: int) -> str:
    loop = asyncio.get_running_loop()
    future: asyncio.Future[str] = loop.create_future()

    def observe(request) -> None:
        if "/elements?" in request.url and not future.done():
            future.set_result(request.url)

    page.on("request", observe)
    try:
        return await asyncio.wait_for(future, timeout_ms / 1000)
    finally:
        page.remove_listener("request", observe)


async def collect_one(browser, year: str, team: dict, timeout_ms: int) -> dict:
    match = ONSHAPE_PATTERN.match(team["cad"])
    if not match:
        raise ValueError("unsupported CAD URL")
    output, relative = preview_path(year, team)
    context: BrowserContext = await browser.new_context(
        viewport={"width": 960, "height": 640},
        user_agent="FIRSTHub public CAD preview collector",
    )
    page = await context.new_page()
    elements_task: asyncio.Task[str] | None = None
    try:
        # Public workspace/version links do not need the heavy CAD editor merely
        # to resolve their element catalogue. Calling the endpoint directly
        # makes a full-library refresh several times faster.
        source_kind = match.group("wv").lower()
        source_id = match.group("wvid")
        elements_url = (
            f"https://cad.onshape.com/api/documents/d/{match.group('did')}"
            f"/{source_kind}/{source_id}/elements?withThumbnails=true"
        )
        response = await context.request.get(
            elements_url.replace("withThumbnails=false", "withThumbnails=true"), timeout=timeout_ms
        )
        if not response.ok:
            raise ValueError(f"element catalogue returned HTTP {response.status}")
        elements = await response.json()
        requested = next(
            (item for item in elements if item.get("id") == match.group("eid")), None
        )
        requested_name = str((requested or {}).get("name", "")).lower()
        renderable_names = " ".join(
            str(item.get("name", "")).lower()
            for item in elements
            if item.get("elementType") in {"ASSEMBLY", "PARTSTUDIO"}
        )
        if (
            any(word in requested_name for word in ("field", "driver station", "field wall"))
            and not any(
                word in renderable_names
                for word in ("robot", "robot assembly", "chassis", "drivetrain")
            )
        ):
            raise ValueError("linked Onshape document appears to contain a field, not a robot")
        renderable = [
            item
            for item in elements
            if item.get("elementType") in {"ASSEMBLY", "PARTSTUDIO"}
        ]
        if renderable and all(
            any(
                word in str(item.get("name", "")).lower()
                for word in ("feature playground", "test ps", "sandbox")
            )
            for item in renderable
        ):
            raise ValueError("linked Onshape document contains feature tests, not a robot")
        candidates = sorted(
            elements, key=lambda item: element_score(item, match.group("eid")), reverse=True
        )
        if not candidates or element_score(candidates[0], match.group("eid")) < 0:
            raise ValueError("no renderable assembly or part studio found")
        element = candidates[0]
        kind = "assemblies" if element["elementType"] == "ASSEMBLY" else "partstudios"
        render_url = (
            f"https://cad.onshape.com/api/v14/{kind}/d/{match.group('did')}"
            f"/{source_kind}/{source_id}/e/{element['id']}/shadedviews"
        )
        rendered = await context.request.get(
            render_url,
            params={
                "viewMatrix": str(
                    team.get("cadPreviewViewMatrix", FRONT_UPPER_VIEW_MATRIX)
                ),
                "outputWidth": "640",
                "outputHeight": "360",
                "pixelSize": "0",
                "edges": "show",
                "useAntiAliasing": "true",
            },
            timeout=timeout_ms,
        )
        if not rendered.ok:
            raise ValueError(f"shaded view returned HTTP {rendered.status}")
        payload = await rendered.json()
        images = payload.get("images", [])
        if not images:
            raise ValueError("shaded view did not include an image")
        encode_webp(base64.b64decode(images[0]), output)
        team["cadPreview"] = relative
        team["cadPreviewElement"] = element.get("name", "")
        team["cadPreviewAngle"] = "front-upper-three-quarter"
        return {
            "year": year,
            "team": team["n"],
            "cad": team["cad"],
            "preview": relative,
            "element": element.get("name", ""),
            "angle": "front-upper-three-quarter",
            "updatedAt": datetime.now(timezone.utc).isoformat(),
            "status": "ok",
        }
    finally:
        if elements_task and not elements_task.done():
            elements_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await elements_task
        await context.close()


async def run(args: argparse.Namespace) -> int:
    data = load_data()
    years = set(args.years or data["seasons"].keys())
    jobs: list[tuple[str, dict]] = []
    skipped = 0
    for year, season in data["seasons"].items():
        if year not in years:
            continue
        for team in season.get("open", []):
            if args.teams and str(team.get("n")) not in set(args.teams):
                continue
            cad = str(team.get("cad", ""))
            if urlparse(cad).hostname != "cad.onshape.com" or not ONSHAPE_PATTERN.match(cad):
                continue
            output, relative = preview_path(year, team)
            if args.existing_only and not (team.get("cadPreview") and output.exists()):
                continue
            if not args.force and output.exists() and not team.get("cadPreview"):
                # Recover a completed image after an interrupted long backfill.
                team["cadPreview"] = relative
                team["cadPreviewAngle"] = "front-upper-three-quarter"
                skipped += 1
                continue
            if not args.force and team.get("cadPreview") and output.exists():
                skipped += 1
                continue
            jobs.append((year, team))
    jobs.sort(key=lambda item: (item[0], -(int(item[1].get("views", 0) or 0)), int(item[1]["n"])))
    if args.limit:
        jobs = jobs[: args.limit]
    print(f"CAD previews: {len(jobs)} queued, {skipped} already cached", flush=True)
    if not jobs:
        return 0

    PREVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {"generatedAt": "", "entries": [], "failures": []}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    existing = {(entry.get("year"), entry.get("team")): entry for entry in manifest.get("entries", [])}
    failures: list[dict] = []
    completed = 0
    semaphore = asyncio.Semaphore(args.workers)

    async with async_playwright() as playwright:
        launch_options = {"headless": True}
        if args.executable_path:
            launch_options["executable_path"] = args.executable_path
        browser = await playwright.chromium.launch(**launch_options)

        async def guarded(year: str, team: dict) -> None:
            nonlocal completed
            async with semaphore:
                last_error: Exception | None = None
                for attempt in range(1, args.retries + 1):
                    try:
                        entry = await collect_one(browser, year, team, args.timeout * 1000)
                        existing[(year, team["n"])] = entry
                        completed += 1
                        print(f"OK {year} #{team['n']}: {entry['element']}", flush=True)
                        if args.delay:
                            await asyncio.sleep(args.delay)
                        return
                    except (ValueError, OSError, PlaywrightError, PlaywrightTimeoutError, asyncio.TimeoutError) as error:
                        last_error = error
                        if attempt < args.retries:
                            await asyncio.sleep(attempt * 2 + args.delay)
                failures.append(
                    {
                        "year": year,
                        "team": team["n"],
                        "cad": team["cad"],
                        "error": str(last_error)[:300],
                    }
                )
                if args.force:
                    output, _ = preview_path(year, team)
                    output.unlink(missing_ok=True)
                    for field in ("cadPreview", "cadPreviewElement", "cadPreviewAngle"):
                        team.pop(field, None)
                print(f"SKIP {year} #{team['n']}: {last_error}", flush=True)

        await asyncio.gather(*(guarded(year, team) for year, team in jobs))
        await browser.close()

    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "entries": sorted(existing.values(), key=lambda item: (item["year"], int(item["team"]))),
        "failures": failures,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_data(data)
    print(f"Generated {completed} previews; {len(failures)} links used the CAD-button fallback.", flush=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--years", nargs="+", help="Only process these season years")
    parser.add_argument("--teams", nargs="+", help="Only process these team numbers")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent isolated browser contexts")
    parser.add_argument("--limit", type=int, default=0, help="Maximum number of missing previews this run")
    parser.add_argument("--timeout", type=int, default=45, help="Per-request timeout in seconds")
    parser.add_argument("--retries", type=int, default=3, help="Attempts per public CAD link")
    parser.add_argument(
        "--delay",
        type=float,
        default=1.5,
        help="Polite delay between public Onshape jobs/retries in seconds",
    )
    parser.add_argument("--force", action="store_true", help="Regenerate existing previews")
    parser.add_argument(
        "--existing-only",
        action="store_true",
        help="Only process records that already have a cached preview (use with --force)",
    )
    parser.add_argument("--executable-path", help="Use an existing Chromium/Edge executable")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run(parse_args())))
