"""Enrich Impact essay entries with official event wins and current team names.

The source of truth is the public FIRST Event Web team-season page.  Each
Impact entry receives an ``events`` array for the season in which the essay
was published, while ``nm`` is refreshed from the newest available season.
"""

from __future__ import annotations

import concurrent.futures
import html
import json
import re
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DATA_RE = re.compile(r"const DATA = (.*?);\r?\n")
ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TEAM_NAME_RE = re.compile(r"Team\s+(\d+)\s+-\s+(.*?)\s+\((\d{4})\)", re.S)
AWARD_RE = re.compile(r'href="/\d+/awards\?id=\d+">(.*?)</a>', re.S)
EVENT_RE = re.compile(r'href="/(\d{4})/([A-Za-z0-9]+)"[^>]*title="Winning Event"[^>]*>(.*?)</a>', re.S)


def clean(value: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", value)).split())


def fetch_page(year: int, team: int) -> str:
    url = f"https://frc-events.firstinspires.org/{year}/team/{team}"
    request = urllib.request.Request(url, headers={"User-Agent": "FirstHub data maintenance/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return ""


def parse_page(year: int, team: int, page: str) -> dict:
    name = ""
    match = TEAM_NAME_RE.search(page)
    if match and int(match.group(1)) == team:
        name = clean(match.group(2))

    events = []
    seen = set()
    for row in ROW_RE.findall(page):
        award = AWARD_RE.search(row)
        event = EVENT_RE.search(row)
        if not award or not event:
            continue
        award_name = clean(award.group(1)).lower()
        if "impact award" not in award_name and "chairman" not in award_name:
            continue
        event_name = clean(event.group(3))
        event_code = event.group(2).upper()
        key = (event_code, event_name)
        if key in seen:
            continue
        seen.add(key)
        events.append({
            "code": event_code,
            "name": event_name,
            "url": f"https://frc-events.firstinspires.org/{year}/{event_code}/awards",
        })
    return {"year": year, "team": team, "name": name, "events": events}


def main() -> None:
    source = INDEX.read_text(encoding="utf-8")
    match = DATA_RE.search(source)
    if not match:
        raise RuntimeError("Could not locate DATA payload in index.html")
    data = json.loads(match.group(1))
    seasons = data["seasons"]
    # Two legacy aggregate-PDF links were previously misread as team numbers.
    for year, season in seasons.items():
        season["impact"] = [
            team for team in season["impact"]
            if not (int(team["n"]) == int(year) and not team.get("nm") and not team.get("events"))
        ]
    requested = {(int(year), int(team["n"])) for year, season in seasons.items() for team in season["impact"]}
    all_teams = {team for _, team in requested}
    # Season pages provide award-event history; newest pages provide current names.
    jobs = requested | {(2026, team) for team in all_teams}

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        future_map = {
            executor.submit(fetch_page, year, team): (year, team)
            for year, team in sorted(jobs)
        }
        for index, future in enumerate(concurrent.futures.as_completed(future_map), 1):
            year, team = future_map[future]
            page = future.result()
            results[(year, team)] = parse_page(year, team, page)
            if index % 50 == 0 or index == len(future_map):
                print(f"Fetched {index}/{len(future_map)} FIRST team-season pages")

    # Fall back to the newest historical page when a team has no 2026 profile.
    latest_names = {team: results[(2026, team)]["name"] for team in all_teams if results.get((2026, team), {}).get("name")}
    for year in range(2025, 2020, -1):
        missing = [team for team in all_teams if team not in latest_names and (year, team) in requested]
        for team in missing:
            name = results.get((year, team), {}).get("name")
            if name:
                latest_names[team] = name

    event_count = 0
    renamed = 0
    for year, season in seasons.items():
        for team in season["impact"]:
            number = int(team["n"])
            official_name = latest_names.get(number)
            if official_name and official_name != team.get("nm"):
                team["nm"] = official_name
                renamed += 1
            events = results.get((int(year), number), {}).get("events", [])
            if events:
                team["events"] = events
                event_count += 1

    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    updated = source[: match.start(1)] + encoded + source[match.end(1) :]
    INDEX.write_text(updated, encoding="utf-8")
    print(f"Updated {renamed} team names; added official events to {event_count} Impact entries")


if __name__ == "__main__":
    main()
