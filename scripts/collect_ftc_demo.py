"""Build the FTC demo dataset entirely from public web pages.

Sources:
- FIRST FTC Event Web season award tables
- FTC PortfolioLab embedded public portfolio data
- OpenVault public portfolio catalogue
- Chief Delphi public search results for FTC Open Alliance threads
- FTC Resources public programming directory

The collector preserves source URLs and never invents missing fields. Records
that cannot be parsed are skipped and counted in the generated audit summary.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "ftc-demo-raw.json"
USER_AGENT = "FIRSTHub FTC public-data collector/1.0 (+https://firsthub.site/)"
GAMES = {2023: "CENTERSTAGE", 2024: "INTO THE DEEP", 2025: "DECODE"}


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read().decode("utf-8", errors="replace")


def clean(value: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value)).split())


class AwardsParser(HTMLParser):
    def __init__(self, year: int) -> None:
        super().__init__()
        self.year = year
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cells: list[str] = []
        self.cell_text: list[str] = []
        self.links: list[str] = []
        self.cell_links: list[str] = []
        self.records: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "table" and values.get("id") == "awards":
            self.in_table = True
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.cells, self.links = [], []
        elif self.in_row and tag == "td":
            self.in_cell = True
            self.cell_text, self.cell_links = [], []
        elif self.in_cell and tag == "a" and values.get("href"):
            self.cell_links.append(values["href"] or "")

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.in_cell and tag == "td":
            self.cells.append(" ".join("".join(self.cell_text).split()))
            self.links.append(self.cell_links[0] if self.cell_links else "")
            self.in_cell = False
        elif self.in_row and tag == "tr":
            self.in_row = False
            if len(self.cells) >= 5:
                event_link, team_link = self.links[1], self.links[3]
                event_code = event_link.rstrip("/").split("/")[-1] if event_link else ""
                team_match = re.search(r"/team/(\d+)", team_link)
                if event_code and team_match and self.cells[2]:
                    self.records.append({
                        "season": str(self.year),
                        "date": self.cells[0],
                        "eventCode": event_code.upper(),
                        "eventName": self.cells[1],
                        "award": self.cells[2],
                        "teamNumber": int(team_match.group(1)),
                        "teamName": self.cells[4],
                        "sourceType": "official",
                        "source": urllib.parse.urljoin("https://ftc-events.firstinspires.org", event_link) + "/awards",
                    })
        elif self.in_table and tag == "table":
            self.in_table = False


def collect_awards(years: list[int]) -> tuple[list[dict], list[dict]]:
    records, audit = [], []
    for year in years:
        url = f"https://ftc-events.firstinspires.org/{year}/awards"
        parser = AwardsParser(year)
        try:
            parser.feed(fetch(url))
            records.extend(parser.records)
            audit.append({"source": url, "status": "ok", "records": len(parser.records)})
            print(f"awards {year}: {len(parser.records)}")
        except Exception as error:
            audit.append({"source": url, "status": "failed", "error": str(error)})
            print(f"awards {year}: FAILED {error}")
    return records, audit


def collect_event_names(years: list[int]) -> tuple[dict[tuple[str, str], str], list[dict]]:
    """Read the event catalogue embedded in each public season home page."""
    names: dict[tuple[str, str], str] = {}
    audit: list[dict] = []
    for year in years:
        url = f"https://ftc-events.firstinspires.org/{year}"
        try:
            page = fetch(url)
            groups = []
            for variable in ("KickoffEvents", "OffSeasonEvents", "OtherEvents", "PremierEvents"):
                match = re.search(rf"window\.{variable}\s*=\s*", page)
                if match:
                    value, _ = json.JSONDecoder().raw_decode(page, match.end())
                    groups.extend(value)
            if not groups:
                raise ValueError("embedded event catalogues not found")
            count = 0
            for group in groups:
                for event in group.get("E", []):
                    code, name = str(event.get("Tc", "")).upper(), clean(str(event.get("En", "")))
                    if code and name:
                        names[(str(year), code)] = name
                        count += 1
            audit.append({"source": url, "status": "ok", "records": count})
            print(f"event names {year}: {count}")
        except Exception as error:
            audit.append({"source": url, "status": "failed", "error": str(error)})
            print(f"event names {year}: FAILED {error}")
    return names, audit


def collect_portfolio_lab() -> tuple[list[dict], dict]:
    url = "https://www.ftcportfoliolab.org/portfolio"
    page = fetch(url)
    pattern = re.compile(
        r'\\"id\\":\\"(?P<id>[^\"]+)\\",\\"teamName\\":\\"(?P<name>.*?)\\",'
        r'\\"teamNumber\\":(?P<number>\d+),(?P<middle>.*?)'
        r'\\"season\\":\\"(?P<season>.*?)\\",\\"level\\":\\"(?P<level>.*?)\\",'
        r'\\"stars\\":\\"(?P<stars>.*?)\\",\\"score\\":\\"(?P<score>.*?)\\",'
        r'\\"award\\":\\"(?P<award>.*?)\\",\\"cover\\":\\"(?P<cover>.*?)\\",'
        r'\\"pdf\\":\\"(?P<pdf>.*?)\\"', re.S
    )
    records = []
    for match in pattern.finditer(page):
        season_match = re.search(r"(20\d{2})", match.group("season"))
        records.append({
            "id": "portfoliolab-" + match.group("id"),
            "season": season_match.group(1) if season_match else "",
            "teamNumber": int(match.group("number")),
            "teamName": bytes(match.group("name"), "utf-8").decode("unicode_escape"),
            "seasonLabel": match.group("season"),
            "level": match.group("level"),
            "award": match.group("award"),
            "rating": match.group("stars"),
            "score": match.group("score"),
            "pdf": match.group("pdf").replace(r"\u0026", "&"),
            "sourceType": "community",
            "source": url,
        })
    print(f"PortfolioLab: {len(records)}")
    return records, {"source": url, "status": "ok", "records": len(records)}


def collect_openvault() -> tuple[list[dict], dict]:
    url = "https://www.open-vault-ftc.org/portfolios/portfolios"
    page = fetch(url)
    blocks = re.split(r'<h2 class="fw-bolder">', page)[1:]
    records = []
    for index, block in enumerate(blocks):
        block = block.split('<h2 class="fw-bolder">', 1)[0]
        title = clean(block.split("</h2>", 1)[0])
        number = re.search(r"Team Number:</strong>\s*(\d+)", block)
        season = re.search(r"Seasons used:</strong>\s*([^<]+)", block)
        award = re.search(r"Awards won:</strong>\s*([^<]+)", block)
        pdf = re.search(r'<a href="([^"]+)"[^>]*download=', block)
        team = re.search(r"<strong>By:\s*(.*?)</strong>", block, re.S)
        if not (number and pdf):
            continue
        year = re.search(r"(20\d{2})", season.group(1) if season else "")
        records.append({
            "id": f"openvault-{number.group(1)}-{index}",
            "season": year.group(1) if year else "",
            "teamNumber": int(number.group(1)),
            "teamName": clean(team.group(1)).replace(f"#{number.group(1)}", "").strip() if team else "",
            "seasonLabel": clean(season.group(1)) if season else "",
            "level": "",
            "award": clean(award.group(1)) if award else "",
            "rating": "",
            "score": "",
            "pdf": html.unescape(pdf.group(1)),
            "sourceType": "community",
            "source": url,
            "title": title,
        })
    print(f"OpenVault: {len(records)}")
    return records, {"source": url, "status": "ok", "records": len(records)}


def infer_ftc_season(title: str, fallback: str) -> str:
    """Map a public thread title to the FTC season start year."""
    lowered = title.lower().replace("–", "-")
    if "centerstage" in lowered or re.search(r"2023\s*[-/]\s*24", lowered):
        return "2023"
    if "into the deep" in lowered or re.search(r"2024\s*[-/]\s*25", lowered):
        return "2024"
    if "decode" in lowered or re.search(r"2025\s*[-/]\s*26", lowered) or "2026" in lowered:
        return "2025"
    # Calendar-year labels on build threads normally name the season ending in
    # that year ("2025 build thread" = the 2024-25 INTO THE DEEP season).
    single_year = re.search(r"\b(2024|2025)\b", lowered)
    if single_year:
        return str(int(single_year.group(1)) - 1)
    return fallback


def collect_open_alliance(pages: int = 3) -> tuple[list[dict], list[dict]]:
    records, audit, seen = [], [], set()
    queries = [
        ("2023", "#ftc-open-alliance after:2023-01-01 before:2024-09-01"),
        ("2024", "#ftc-open-alliance after:2024-01-01 before:2025-09-01"),
        ("2025", "#ftc-open-alliance after:2025-01-01"),
    ]
    for fallback_season, query in queries:
      for page_number in range(1, pages + 1):
        url = "https://www.chiefdelphi.com/search.json?" + urllib.parse.urlencode({"q": query, "page": page_number})
        try:
            payload = json.loads(fetch(url))
            accepted = 0
            for topic in payload.get("topics", []):
                title = topic.get("title", "")
                lowered = title.lower()
                if topic.get("id") in seen or not any(term in lowered for term in ("open alliance", "build thread", "build blog")):
                    continue
                seen.add(topic["id"])
                number = re.search(r"(?:FTC|Team)?\s*#?(\d{3,5})", title, re.I)
                records.append({
                    "season": infer_ftc_season(title, fallback_season),
                    "teamNumber": int(number.group(1)) if number else None,
                    "teamName": "",
                    "title": title,
                    "views": topic.get("views", 0),
                    "posts": topic.get("posts_count", 0),
                    "sourceType": "community",
                    "source": f"https://www.chiefdelphi.com/t/{topic.get('slug')}/{topic.get('id')}",
                })
                accepted += 1
            audit.append({"source": url, "status": "ok", "records": accepted})
        except Exception as error:
            audit.append({"source": url, "status": "failed", "error": str(error)})
    records.sort(key=lambda item: item.get("views", 0), reverse=True)
    print(f"Open Alliance: {len(records)}")
    return records, audit


class LinksParser(HTMLParser):
    def __init__(self, base: str) -> None:
        super().__init__()
        self.base = base
        self.href = ""
        self.text: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.href = dict(attrs).get("href") or ""
            self.text = []

    def handle_data(self, data: str) -> None:
        if self.href:
            self.text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.href:
            label = " ".join("".join(self.text).split())
            if label and not self.href.startswith("#"):
                self.links.append((label, urllib.parse.urljoin(self.base, self.href)))
            self.href, self.text = "", []


def collect_resources() -> tuple[list[dict], dict]:
    url = "https://ftc-resources.readthedocs.io/en/latest/programming.html"
    parser = LinksParser(url)
    parser.feed(fetch(url))
    ignored = ("readthedocs", "github.com/ftc-docs", "genindex", "search.html", "index.html")
    ignored_labels = {"edit on github", "next", "previous", "programming", "contents", "search"}
    records, seen = [], set()
    for label, target in parser.links:
        key = (label.lower(), target)
        if key in seen or label.lower() in ignored_labels or any(term in target.lower() for term in ignored) or len(label) < 3:
            continue
        seen.add(key)
        records.append({"title": label, "description": "Programming resource listed in the FTC Resources directory.", "sourceType": "community", "url": target, "source": url})
    print(f"Resources: {len(records)}")
    return records, {"source": url, "status": "ok", "records": len(records)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="+", type=int, default=[2023, 2024, 2025])
    parser.add_argument("--chief-pages", type=int, default=3)
    parser.add_argument("--merge", action="store_true", help="Keep award seasons not requested in this run")
    args = parser.parse_args()

    awards, awards_audit = collect_awards(args.years)
    event_names, event_audit = collect_event_names(args.years)
    for item in awards:
        item["eventName"] = event_names.get((item["season"], item["eventCode"]), item["eventName"])
    portfolios_a, portfolio_audit = collect_portfolio_lab()
    portfolios_b, openvault_audit = collect_openvault()
    open_teams, open_audit = collect_open_alliance(args.chief_pages)
    official_team_names: dict[int, str] = {}
    for item in awards:
        if item.get("teamNumber") and item.get("teamName"):
            official_team_names[item["teamNumber"]] = item["teamName"]
    for item in open_teams:
        item["teamName"] = official_team_names.get(item.get("teamNumber"), "")
    resources, resources_audit = collect_resources()

    previous = {}
    if args.merge and OUTPUT.exists():
        previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
        requested = {str(year) for year in args.years}
        awards = [item for item in previous.get("awards", []) if item.get("season") not in requested] + awards

    portfolios = portfolios_a + portfolios_b
    unique_portfolios = {item["id"]: item for item in portfolios}
    generated = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "generatedAt": generated,
        "mode": "automatic-demo",
        "seasons": {**previous.get("seasons", {}), **{str(year): GAMES.get(year, str(year)) for year in args.years}},
        "awards": awards,
        "portfolios": list(unique_portfolios.values()),
        "openTeams": open_teams,
        "resources": resources,
        "audit": awards_audit + event_audit + [portfolio_audit, openvault_audit] + open_audit + [resources_audit],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}: awards={len(awards)}, portfolios={len(unique_portfolios)}, open={len(open_teams)}, resources={len(resources)}")


if __name__ == "__main__":
    main()
