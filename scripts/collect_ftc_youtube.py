"""Collect public FTC team videos from YouTube search results.

Only metadata and original YouTube URLs are stored. Videos are never
downloaded or re-hosted. A result is accepted only when an FTC team number can
be identified from the title, uploader, channel, or description.

Requires yt-dlp::

    python -m pip install yt-dlp
    python scripts/collect_ftc_youtube.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    import yt_dlp
except ImportError as exc:  # pragma: no cover - dependency guidance
    raise SystemExit("Install the collector dependency with: python -m pip install yt-dlp") from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "ftc-youtube.json"
SEARCHES = {
    "2023": [
        "FTC CENTERSTAGE robot reveal",
        "FTC CENTERSTAGE robot walkthrough team",
        "FTC CENTERSTAGE engineering portfolio team",
    ],
    "2024": [
        "FTC INTO THE DEEP robot reveal",
        "FTC INTO THE DEEP robot walkthrough team",
        "FTC INTO THE DEEP engineering portfolio team",
    ],
    "2025": [
        "FTC DECODE robot reveal",
        "FTC DECODE robot walkthrough team",
        "FTC DECODE engineering portfolio team",
    ],
}
SEASON_MARKERS = {
    "2023": ("centerstage", "center stage"),
    "2024": ("into the deep",),
    "2025": ("decode",),
}

EXPLICIT_TEAM_PATTERNS = (
    re.compile(r"\bFTC\s*(?:Team\s*)?[#:\-]?\s*(\d{3,5})\b", re.I),
    re.compile(r"\bTeam\s*[#:\-]?\s*(\d{3,5})\b", re.I),
    re.compile(r"#(\d{3,5})\b"),
)
LOOSE_TEAM_PATTERNS = (
    re.compile(r"^\s*(\d{3,5})\b"),
    re.compile(r"\b(\d{3,5})\s+(?:robotics|robot|FTC)\b", re.I),
    re.compile(r"(?:ftc|team)[_\-. ]*(\d{3,5})\b", re.I),
)
SEASON_YEARS = {2023, 2024, 2025, 2026}
USER_AGENT = "FIRSTHub FTC YouTube metadata collector/1.0 (+https://firsthub.site/)"


def explicit_team_number(text: str) -> int | None:
    for pattern in EXPLICIT_TEAM_PATTERNS:
        for match in pattern.finditer(text or ""):
            number = int(match.group(1))
            # In "FTC 2024-25", 2024 is a season, not a team number. Explicit
            # "Team 2024" and "#2024" remain valid if encountered.
            if number in SEASON_YEARS and not re.search(r"(?:team|#)", match.group(0), re.I):
                continue
            return number
    return None


def loose_team_number(text: str) -> int | None:
    for pattern in LOOSE_TEAM_PATTERNS:
        match = pattern.search(text or "")
        if match:
            number = int(match.group(1))
            if number not in SEASON_YEARS:
                return number
    return None


def identify_team(entry: dict) -> int | None:
    # Strong evidence in a video title wins over channel-handle heuristics.
    title = entry.get("title") or ""
    uploader_blob = " ".join(
        str(entry.get(key) or "") for key in ("uploader_id", "channel", "uploader")
    )
    number = explicit_team_number(title)
    if number:
        matched_as_team = bool(re.search(r"(?:team|#)\s*[#:\-]?\s*" + str(number), title, re.I))
        uploader_looks_robotics = bool(re.search(r"(?:ftc|team|robot)", uploader_blob, re.I))
        if matched_as_team or uploader_looks_robotics:
            return number
    number = loose_team_number(title)
    if number and (re.search(r"(?:ftc|team|robot)", uploader_blob, re.I) or "behind the bot" in title.lower()):
        return number
    number = explicit_team_number(uploader_blob) or loose_team_number(uploader_blob)
    if number:
        return number
    return None


def search(query: str, limit: int) -> list[dict]:
    options = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "playlistend": limit,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False) or {}
    return [entry for entry in result.get("entries", []) if entry]


def validate_ftc_team(number: int) -> tuple[int, bool | None]:
    """Return False only for an authoritative missing-team response.

    Transient network failures remain None so a temporary outage does not erase
    previously collected records.
    """
    url = f"https://ftc-events.firstinspires.org/team/{number}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            html = response.read().decode("utf-8", "ignore")
        return number, bool(re.search(rf"\bTeam\s+{number}\b", html, re.I))
    except urllib.error.HTTPError as exc:
        return number, False if exc.code == 404 else None
    except (urllib.error.URLError, TimeoutError):
        return number, None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit-per-query", type=int, default=35)
    parser.add_argument("--skip-team-validation", action="store_true")
    args = parser.parse_args()

    collected: dict[str, dict] = {}
    audit = []
    for season, queries in SEARCHES.items():
        for query in queries:
            entries = search(query, args.limit_per_query)
            accepted = 0
            for entry in entries:
                video_id = entry.get("id")
                team_number = identify_team(entry)
                if not video_id or not team_number or team_number < 100:
                    continue
                blob = " ".join(
                    str(entry.get(key) or "")
                    for key in ("title", "description", "channel", "uploader", "uploader_id")
                )
                if "FTC" not in blob.upper():
                    continue
                season_text = " ".join(
                    str(entry.get(key) or "") for key in ("title", "description")
                ).lower()
                if not any(marker in season_text for marker in SEASON_MARKERS[season]):
                    continue
                url = f"https://www.youtube.com/watch?v={video_id}"
                item = {
                    "season": season,
                    "teamNumber": team_number,
                    "teamName": entry.get("channel") or entry.get("uploader") or f"FTC Team {team_number}",
                    "title": entry.get("title") or f"FTC Team {team_number} public video",
                    "views": int(entry.get("view_count") or 0),
                    "posts": 0,
                    "sourceType": "team",
                    "sourcePlatform": "youtube",
                    "source": url,
                    "channel": entry.get("channel_url") or entry.get("uploader_url") or "",
                    "links": [{"type": "video", "url": url}],
                }
                previous = collected.get(video_id)
                if previous is None or int(item["views"]) > int(previous.get("views") or 0):
                    collected[video_id] = item
                accepted += 1
            audit.append({"season": season, "query": query, "results": len(entries), "accepted": accepted})

    validation: dict[int, bool | None] = {}
    if not args.skip_team_validation:
        team_numbers = sorted({item["teamNumber"] for item in collected.values()})
        with ThreadPoolExecutor(max_workers=8) as pool:
            validation = dict(pool.map(validate_ftc_team, team_numbers))
    rejected_numbers = sorted(number for number, valid in validation.items() if valid is False)
    verified_items = [
        item for item in collected.values() if validation.get(item["teamNumber"]) is not False
    ]
    items = sorted(
        verified_items,
        key=lambda item: (item["season"], -int(item.get("views") or 0), item["teamNumber"]),
    )
    result = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": "YouTube public search metadata",
        "policy": "Original URLs only; no video files are downloaded or re-hosted.",
        "items": items,
        "teamValidation": {
            "source": "FIRST FTC Event Web team pages",
            "rejectedMissingTeamNumbers": rejected_numbers,
        },
        "audit": audit,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"videos": len(items), "teams": len({item['teamNumber'] for item in items})}, ensure_ascii=False))


if __name__ == "__main__":
    main()
