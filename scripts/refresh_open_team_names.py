"""Refresh FRC Open Alliance team names from public FIRST Event Web lists."""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
REPORT = ROOT / "data" / "frc-open-name-audit.json"
DATA_RE = re.compile(r"const DATA = (.*?);\r?\n")
USER_AGENT = "FIRSTHub public team-name maintenance/1.0 (+https://firsthub.site/)"


def clean(value: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value)).split())


def fetch_names(year: int) -> dict[int, str]:
    url = f"https://frc-events.firstinspires.org/{year}/AllTeams"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response:
        page = response.read().decode("utf-8", errors="replace")
    names: dict[int, str] = {}
    pattern = re.compile(
        rf'<a class="list-group-item[^>]+href="/{year}/team/(\d+)"[^>]*>(.*?)</a>',
        re.S,
    )
    for match in pattern.finditer(page):
        number = int(match.group(1))
        values = [clean(item) for item in re.findall(r"<div[^>]*>(.*?)</div>", match.group(2), re.S)]
        values = [value for value in values if value]
        # The final four textual columns are team number, name, district, location.
        try:
            number_index = values.index(str(number))
        except ValueError:
            continue
        if number_index + 1 < len(values) and values[number_index + 1]:
            names[number] = values[number_index + 1]
    print(f"{year}: {len(names)} official teams")
    return names


def fetch_team_name(number: int) -> tuple[int, str]:
    url = f"https://frc-events.firstinspires.org/team/{number}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            page = response.read().decode("utf-8", errors="replace")
    except Exception:
        return number, ""
    match = re.search(rf"Team\s+{number}\s+-\s+([^<\r\n]+)", page, re.I)
    return number, clean(match.group(1)) if match else ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="+", type=int, default=[2026, 2025, 2024, 2023, 2022, 2021])
    args = parser.parse_args()

    # Newest season wins; older lists only fill teams absent from newer seasons.
    official: dict[int, dict] = {}
    source_counts = []
    failures = []
    for year in args.years:
        try:
            names = fetch_names(year)
            source_counts.append({"year": year, "teams": len(names)})
            for number, name in names.items():
                official.setdefault(number, {"name": name, "year": year, "source": f"https://frc-events.firstinspires.org/{year}/team/{number}"})
        except Exception as error:
            failures.append({"year": year, "error": str(error)})
            print(f"{year}: FAILED {error}")

    source = INDEX.read_text(encoding="utf-8")
    match = DATA_RE.search(source)
    if not match:
        raise RuntimeError("Could not locate DATA payload in index.html")
    data = json.loads(match.group(1))

    open_numbers = {int(team["n"]) for season_data in data["seasons"].values() for team in season_data.get("open", [])}
    missing_numbers = sorted(open_numbers - official.keys())
    recovered = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for number, name in executor.map(fetch_team_name, missing_numbers):
            if name:
                official[number] = {"name": name, "year": None, "source": f"https://frc-events.firstinspires.org/team/{number}"}
                recovered += 1
    print(f"Direct team-page fallback: recovered {recovered}/{len(missing_numbers)}")

    changes = []
    unmatched: dict[int, dict] = {}
    occurrences = 0
    for season, season_data in data["seasons"].items():
        for team in season_data.get("open", []):
            occurrences += 1
            number = int(team["n"])
            current = str(team.get("nm") or "").strip()
            record = official.get(number)
            if not record:
                unmatched.setdefault(number, {"teamNumber": number, "currentName": current, "seasons": []})["seasons"].append(season)
                continue
            if current != record["name"]:
                changes.append({
                    "teamNumber": number,
                    "season": season,
                    "oldName": current,
                    "newName": record["name"],
                    "officialSeason": record["year"],
                    "source": record["source"],
                })
                team["nm"] = record["name"]

    # A number that exists in neither recent All Teams lists nor the permanent
    # official team page is not a verifiable FRC team record. These are crawler
    # false positives (often years, product numbers, or FTC team numbers).
    unmatched_numbers = set(unmatched)
    removed = []
    for season, season_data in data["seasons"].items():
        kept = []
        for team in season_data.get("open", []):
            if int(team["n"]) in unmatched_numbers:
                removed.append({"season": season, "teamNumber": int(team["n"]), "currentName": team.get("nm", ""), "source": team.get("cd") or team.get("gh") or ""})
            else:
                kept.append(team)
        season_data["open"] = kept

    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    INDEX.write_text(source[: match.start(1)] + encoded + source[match.end(1) :], encoding="utf-8")
    report = {
        "officialSources": source_counts,
        "sourceFailures": failures,
        "openTeamOccurrences": occurrences,
        "renamedOccurrences": len(changes),
        "renamedUniqueTeams": len({item["teamNumber"] for item in changes}),
        "unmatchedUniqueTeams": len(unmatched),
        "removedUnverifiableOccurrences": len(removed),
        "changes": changes,
        "unmatched": sorted(unmatched.values(), key=lambda item: item["teamNumber"]),
        "removed": removed,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Updated {report['renamedOccurrences']} entries for {report['renamedUniqueTeams']} teams; "
        f"removed {report['removedUnverifiableOccurrences']} unverifiable entries"
    )


if __name__ == "__main__":
    main()
