"""Collect and merge public FRC team videos from YouTube.

Only metadata and original links are stored. Candidate team numbers are
verified against FIRST Event Web before records are merged into each season's
Team-Published Resources list.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import html
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yt_dlp
except ImportError as exc:
    raise SystemExit("Install the collector dependency with: python -m pip install yt-dlp") from exc


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "frc-youtube.json"
DATA_JS = ROOT / "assets" / "js" / "data.js"
INDEX_HTML = ROOT / "index.html"
DATA_RE = re.compile(r"const DATA = (.*?);\r?\n")
USER_AGENT = "FIRSTHub FRC YouTube metadata collector/1.0 (+https://firsthub.site/)"

SEASONS = {
    "2021": ("INFINITE RECHARGE at Home", ("infinite recharge",)),
    "2022": ("RAPID REACT", ("rapid react",)),
    "2023": ("CHARGED UP", ("charged up",)),
    "2024": ("CRESCENDO", ("crescendo",)),
    "2025": ("REEFSCAPE", ("reefscape",)),
    "2026": ("REBUILT", ("rebuilt",)),
}
QUERY_SUFFIXES = ("robot reveal", "robot walkthrough", "team build season")
TEAM_PATTERNS = (
    re.compile(r"\bFRC\s*(?:Team\s*)?[#:\-]?\s*(\d{1,5})\b", re.I),
    re.compile(r"\bTeam\s*[#:\-]?\s*(\d{1,5})\b", re.I),
    re.compile(r"#(\d{1,5})\b"),
)
LOOSE_PATTERNS = (
    re.compile(r"^\s*(\d{1,5})\b"),
    re.compile(r"(?:frc|team)[_\-. ]*(\d{1,5})\b", re.I),
)


def clean(value: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value or "")).split())


def explicit_number(text: str) -> int | None:
    for pattern in TEAM_PATTERNS:
        for match in pattern.finditer(text or ""):
            number = int(match.group(1))
            if number in range(2021, 2027) and not re.search(r"(?:team|#)", match.group(0), re.I):
                continue
            return number
    return None


def loose_number(text: str) -> int | None:
    for pattern in LOOSE_PATTERNS:
        match = pattern.search(text or "")
        if match:
            number = int(match.group(1))
            if number not in range(2021, 2027):
                return number
    return None


def identify_team(entry: dict) -> int | None:
    title = entry.get("title") or ""
    uploader = " ".join(str(entry.get(key) or "") for key in ("uploader_id", "channel", "uploader"))
    number = explicit_number(title)
    if number:
        explicit_team = bool(re.search(r"(?:team|#)\s*[#:\-]?\s*" + str(number), title, re.I))
        if explicit_team or re.search(r"(?:frc|team|robot)", uploader, re.I):
            return number
    number = loose_number(title)
    if number and (re.search(r"(?:frc|team|robot)", uploader, re.I) or "behind the bumpers" in title.lower()):
        return number
    return explicit_number(uploader) or loose_number(uploader)


def youtube_search(query: str, limit: int) -> list[dict]:
    options = {"quiet": True, "no_warnings": True, "extract_flat": True, "skip_download": True, "playlistend": limit}
    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False) or {}
    return [entry for entry in result.get("entries", []) if entry]


def validate_team(number: int) -> tuple[int, bool | None, str]:
    url = f"https://frc-events.firstinspires.org/team/{number}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            page = response.read().decode("utf-8", "ignore")
        match = re.search(rf"Team\s+{number}\s+-\s+([^<\r\n]+)", page, re.I)
        return number, bool(re.search(rf"\bTeam\s+{number}\b", page, re.I)), clean(match.group(1)) if match else ""
    except urllib.error.HTTPError as exc:
        return number, False if exc.code == 404 else None, ""
    except (urllib.error.URLError, TimeoutError):
        return number, None, ""


def head_resource_views() -> dict[tuple[str, int], int]:
    """Read the committed pre-run values so YouTube views do not replace CD views."""
    try:
        result = subprocess.run(
            ["git", "show", "HEAD:assets/js/data.js"], cwd=ROOT,
            check=True, capture_output=True, text=True, encoding="utf-8",
        )
        match = DATA_RE.search(result.stdout)
        data = json.loads(match.group(1)) if match else {}
        return {
            (season, int(team["n"])): int(team.get("resourceViews", team.get("views", 0)) or 0)
            for season, season_data in data.get("seasons", {}).items()
            for team in season_data.get("open", [])
        }
    except Exception:
        return {}


def merge_into_data(items: list[dict], official_names: dict[int, str], previous_urls: set[str]) -> dict:
    source = DATA_JS.read_text(encoding="utf-8")
    match = DATA_RE.search(source)
    if not match:
        raise RuntimeError("Could not locate DATA payload in assets/js/data.js")
    data = json.loads(match.group(1))
    committed_views = head_resource_views()
    for season, season_data in data["seasons"].items():
        kept_teams = []
        for team in season_data.get("open", []):
            number = int(team.get("n", -1))
            team["resourceViews"] = int(team.get("resourceViews", committed_views.get((season, number), team.get("views", 0))) or 0)
            videos = [
                video for video in (team.get("ytVideos") or [])
                if not (video.get("url") in previous_urls and video.get("title") != "Existing public team video")
            ]
            if videos:
                team["ytVideos"] = videos
            else:
                team.pop("ytVideos", None)
            if team.get("yt") in previous_urls and not any(video.get("url") == team["yt"] for video in videos):
                team.pop("yt", None)
            team["views"] = team["resourceViews"]
            if any(team.get(key) for key in ("cd", "cad", "gh", "yt", "ph", "site")):
                kept_teams.append(team)
        season_data["open"] = kept_teams
    added_videos = 0
    added_teams = 0
    for item in items:
        season_data = data["seasons"].get(item["season"])
        if not season_data:
            continue
        team = next((row for row in season_data.get("open", []) if int(row.get("n", -1)) == item["teamNumber"]), None)
        if team is None:
            team = {"n": item["teamNumber"], "nm": official_names.get(item["teamNumber"]) or item["teamName"], "tags": [], "resourceViews": 0}
            season_data.setdefault("open", []).append(team)
            added_teams += 1
        videos = list(team.get("ytVideos") or [])
        if team.get("yt") and not any(video.get("url") == team["yt"] for video in videos):
            videos.append({"title": "Existing public team video", "url": team["yt"], "views": int(team.get("views") or 0)})
        if not any(video.get("url") == item["source"] for video in videos):
            videos.append({"title": item["title"], "url": item["source"], "views": item["views"], "channel": item.get("channel", ""), "autoSource": "frc-youtube"})
            added_videos += 1
        videos.sort(key=lambda video: -int(video.get("views") or 0))
        team["ytVideos"] = videos
        team["yt"] = videos[0]["url"]
        team["views"] = max([int(team.get("resourceViews") or 0), *[int(video.get("views") or 0) for video in videos]])
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    DATA_JS.write_text(source[: match.start(1)] + encoded + source[match.end(1) :], encoding="utf-8")
    version = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:12]
    index = INDEX_HTML.read_text(encoding="utf-8")
    index = re.sub(r"assets/js/data\.js\?v=[^\"']+", f"assets/js/data.js?v={version}", index)
    INDEX_HTML.write_text(index, encoding="utf-8")
    return {"addedVideos": added_videos, "addedTeamCards": added_teams, "dataVersion": version}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--limit-per-query", type=int, default=35)
    parser.add_argument("--skip-team-validation", action="store_true")
    args = parser.parse_args()
    previous_urls: set[str] = set()
    previous_items: list[dict] = []
    if args.output.exists():
        try:
            previous_items = json.loads(args.output.read_text(encoding="utf-8")).get("items", [])
            previous_urls = {item["source"] for item in previous_items}
        except (json.JSONDecodeError, KeyError):
            previous_items = []
            previous_urls = set()
    collected: dict[str, dict] = {}
    audit = []
    for season, (game, markers) in SEASONS.items():
        for suffix in QUERY_SUFFIXES:
            query = f"FRC {game} {suffix}"
            entries = youtube_search(query, args.limit_per_query)
            accepted = 0
            for entry in entries:
                video_id = entry.get("id")
                number = identify_team(entry)
                if not video_id or not number:
                    continue
                blob = " ".join(str(entry.get(key) or "") for key in ("title", "description", "channel", "uploader", "uploader_id"))
                season_text = " ".join(str(entry.get(key) or "") for key in ("title", "description")).lower()
                if "FRC" not in blob.upper() or not any(marker in season_text for marker in markers):
                    continue
                if season == "2021" and "at home" not in season_text and "2021" not in season_text:
                    continue
                url = f"https://www.youtube.com/watch?v={video_id}"
                collected[video_id] = {
                    "season": season, "teamNumber": number,
                    "teamName": entry.get("channel") or entry.get("uploader") or f"FRC Team {number}",
                    "title": entry.get("title") or f"FRC Team {number} public video",
                    "views": int(entry.get("view_count") or 0), "sourcePlatform": "youtube", "source": url,
                    "channel": entry.get("channel_url") or entry.get("uploader_url") or "",
                }
                accepted += 1
            audit.append({"season": season, "query": query, "results": len(entries), "accepted": accepted})
    # YouTube search rankings are not stable. Retain earlier verified public
    # records when they temporarily fall outside the current result window.
    for item in previous_items:
        video_id = item.get("source", "").partition("v=")[2].partition("&")[0]
        if video_id:
            collected.setdefault(video_id, item)
    validation: dict[int, bool | None] = {}
    official_names: dict[int, str] = {}
    if not args.skip_team_validation:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            for number, valid, name in pool.map(validate_team, sorted({item["teamNumber"] for item in collected.values()})):
                validation[number] = valid
                if name:
                    official_names[number] = name
    items = [item for item in collected.values() if validation.get(item["teamNumber"]) is not False]
    items.sort(key=lambda item: (item["season"], -item["views"], item["teamNumber"]))
    merge = merge_into_data(items, official_names, previous_urls)
    result = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": "YouTube public search metadata", "policy": "Original URLs only; no video files are downloaded or re-hosted. Previously verified public records are retained across refreshes.",
        "items": items, "audit": audit,
        "teamValidation": {"source": "FIRST FRC Event Web team pages", "rejectedMissingTeamNumbers": sorted(number for number, valid in validation.items() if valid is False)},
        "merge": merge,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"videos": len(items), "teams": len({item['teamNumber'] for item in items}), **merge}, ensure_ascii=False))


if __name__ == "__main__":
    main()
