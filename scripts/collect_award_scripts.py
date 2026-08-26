"""Collect public team award scripts from FIRST Event Web pages.

The default run intentionally collects a small, reviewable demo event. Pass
additional event codes to expand the sample without changing the website.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROW_RE = re.compile(r'<tr id="award\d+">(.*?)</tr>', re.S)
EXCLUDED_AWARD_TERMS = (
    "dean's list", "woodie flowers", "volunteer of the year", "wildcard",
    "regional winners", "regional finalists", "district event winner",
    "district event finalist", "district championship winner",
    "district championship finalist", "championship division winner",
    "championship division finalist",
)


def text(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    return " ".join(html.unescape(value).split())


def collect_event(year: int, event_code: str) -> tuple[str, list[dict], int]:
    source = f"https://frc-events.firstinspires.org/{year}/{event_code}/awards"
    request = urllib.request.Request(source, headers={"User-Agent": "FirstHub award-script demo/1.0"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                page = response.read().decode("utf-8")
            break
        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))
    else:
        raise last_error or RuntimeError(f"Unable to fetch {source}")

    title_match = re.search(r"<title>\s*(.*?)\s+FRC Event Web\s*:\s*Awards", page, re.S)
    event_name = text(title_match.group(1)) if title_match else event_code
    records: list[dict] = []
    source_team_rows = 0
    for row in ROW_RE.findall(page):
        award = re.search(r'href="/[0-9]+/awards\?id=(\d+)">(.*?)</a>', row, re.S)
        team = re.search(r'href="/[0-9]+/team/(\d+)">(\d+)</a>', row)
        script = re.search(r'data-bs-script="(.*?)"\s+data-bs-team=', row, re.S)
        if not (award and team):
            continue
        source_team_rows += 1
        team_name = re.search(r"<b>(.*?)</b>", row, re.S)
        record = {
            "year": year,
            "eventCode": event_code.upper(),
            "eventName": event_name,
            "eventLevel": "regional" if "Regional" in event_name else "event",
            "awardId": int(award.group(1)),
            "awardName": text(award.group(2)),
            "teamNumber": int(team.group(1)),
            "teamName": text(team_name.group(1)) if team_name else "",
            "script": text(script.group(1)) if script else "",
            "hasCitation": bool(script and text(script.group(1))),
            "language": "en",
            "source": source,
        }
        if not any(term in record["awardName"].lower() for term in EXCLUDED_AWARD_TERMS):
            records.append(record)
    return event_name, records, source_team_rows


def list_event_codes(year: int) -> list[str]:
    source = f"https://frc-events.firstinspires.org/{year}/Events/EventList"
    request = urllib.request.Request(source, headers={"User-Agent": "FirstHub award-script archive/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8")
    codes = re.findall(rf'href="/{year}/([A-Za-z0-9]+)/?"', page)
    excluded = {"EVENTS", "EVENTLIST", "AWARDS", "TEAMS", "TEAM", "ALLTEAMS", "DISTRICTS"}
    return sorted({code.upper() for code in codes if code.upper() not in excluded})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("event_codes", nargs="*", default=["CODE"])
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--all-events", action="store_true")
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    all_records: list[dict] = []
    events: list[dict] = []
    event_codes = list_event_codes(args.year) if args.all_events else args.event_codes
    failures: list[dict] = []
    def store_result(index: int, code: str, name: str, records: list[dict], source_rows: int) -> None:
        citations = sum(bool(record.get("script")) for record in records)
        events.append({"code": code, "name": name, "sourceRows": source_rows, "records": len(records), "scripts": citations})
        all_records.extend(records)
        print(f"[{index}/{len(event_codes)}] {code} {name}: {len(records)} records, {citations} citations", flush=True)
        if source_rows and not records:
            print(f"WARNING {code}: {source_rows} official team rows were all removed by scope filters", flush=True)

    if args.workers <= 1:
        for index, code in enumerate(event_codes, 1):
            code = code.upper()
            try:
                name, records, source_rows = collect_event(args.year, code)
                store_result(index, code, name, records, source_rows)
            except Exception as error:  # keep the audit trail and continue the season
                failures.append({"code": code, "error": str(error)})
                print(f"[{index}/{len(event_codes)}] {code} FAILED: {error}", flush=True)
            if args.delay and index < len(event_codes):
                time.sleep(args.delay)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(collect_event, args.year, code.upper()): (index, code.upper()) for index, code in enumerate(event_codes, 1)}
            for future in as_completed(futures):
                index, code = futures[future]
                try:
                    name, records, source_rows = future.result()
                    store_result(index, code, name, records, source_rows)
                except Exception as error:
                    failures.append({"code": code, "error": str(error)})
                    print(f"[{index}/{len(event_codes)}] {code} FAILED: {error}", flush=True)

    events.sort(key=lambda item: item["code"])
    all_records.sort(key=lambda item: (item["eventCode"], item["awardName"], item["teamNumber"]))
    failures.sort(key=lambda item: item["code"])

    citation_count = sum(bool(record.get("script")) for record in all_records)
    payload = {
        "year": args.year,
        "status": "complete" if args.all_events and not failures else "demo",
        "generatedFrom": "FIRST Event Web public awards pages",
        "events": events,
        "failures": failures,
        "records": all_records,
        "recordCount": len(all_records),
        "citationCount": citation_count,
    }
    output = ROOT / "data" / "award-scripts" / f"{args.year}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(all_records)} team award records ({citation_count} citations) from {len(events)} event(s); {len(failures)} failures to {output}")


if __name__ == "__main__":
    main()
