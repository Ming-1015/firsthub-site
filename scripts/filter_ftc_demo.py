"""Normalize and classify FTC public records for the browser demo.

The collector writes raw public records.  This second stage keeps presentation
rules out of the scraper: it de-duplicates records, assigns stable filter tags,
rejects obvious false team-number matches, and adds a small reviewed catalogue
of durable official/community resources.  It uses only the Python standard
library and can optionally check outbound links.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "ftc-demo-raw.json"
DEFAULT_OUTPUT = ROOT / "data" / "ftc-demo.json"
USER_AGENT = "FIRSTHub FTC resource filter/1.0 (+https://firsthub.site/)"

RESOURCE_CATALOGUE = [
    ("FTC Documentation", "official", "official", "FIRST 官方控制系统、硬件、编程与赛季技术文档。", "https://ftc-docs.firstinspires.org/"),
    ("FTC Robot Controller SDK", "programming", "official", "FIRST 官方 Android Studio SDK、示例 OpMode 与版本说明。", "https://github.com/FIRST-Tech-Challenge/FtcRobotController"),
    ("FTC Game & Season Materials", "season", "official", "当季比赛手册、场地图纸、评审与赛季资料入口。", "https://www.firstinspires.org/resource-library/ftc/game-and-season-info"),
    ("Game Manual 0", "learning", "community", "覆盖机械、电子、编程、策略和队伍运营的社区教程。", "https://gm0.org/"),
    ("Road Runner", "motion", "community", "FTC 轨迹规划、定位和运动控制文档。", "https://rr.brott.dev/"),
    ("Pedro Pathing", "motion", "community", "面向 FTC 的路径生成与跟随库。", "https://pedropathing.com/"),
    ("FTC Dashboard", "programming", "community", "遥测图表、运行时配置和摄像头调试工具。", "https://github.com/acmerobotics/ftc-dashboard"),
    ("FTC Lib", "programming", "community", "模块化 FTC 控制与机器人编程库。", "https://ftclib.org/"),
    ("EasyOpenCV", "vision", "community", "FTC 常用 OpenCV 摄像头和视觉处理库。", "https://github.com/OpenFTC/EasyOpenCV"),
    ("AprilTag Library", "vision", "official", "FTC Docs 中的 AprilTag 检测与定位说明。", "https://ftc-docs.firstinspires.org/en/latest/apriltag/vision_portal/apriltag_intro/apriltag-intro.html"),
    ("CTRL ALT FTC", "learning", "community", "由 FTC 社区维护的设计、制造与控制教程。", "https://www.ctrlaltftc.com/"),
    ("FTC Scouting", "strategy", "community", "FTC 比赛数据、赛程与 scouting 工具入口。", "https://ftcscout.org/"),
]

SITE_CATALOGUE = [
    ("Game Manual 0", "community", "learning", "社区维护的系统性 FTC 教程站。", "https://gm0.org/"),
    ("CTRL ALT FTC", "community", "mechanical", "面向 FTC 队伍的设计、制造和机器人知识库。", "https://www.ctrlaltftc.com/"),
    ("Learn Road Runner", "community", "motion", "Road Runner 官方文档与上手路径。", "https://rr.brott.dev/"),
    ("Pedro Pathing", "community", "motion", "Pedro Pathing 文档、快速开始和 API。", "https://pedropathing.com/"),
    ("FTC Lib", "community", "programming", "FTC Lib 文档与示例。", "https://ftclib.org/"),
    ("OpenFTC", "community", "vision", "EasyOpenCV 等 FTC 开源软件项目主页。", "https://github.com/OpenFTC"),
    ("FTC Scout", "community", "strategy", "赛事数据、队伍和 scouting 检索站。", "https://ftcscout.org/"),
    ("FTC Portfolio Lab", "community", "awards", "公开 Engineering Portfolio 索引和评分资料。", "https://www.ftcportfoliolab.org/portfolio"),
]


def award_category(name: str) -> str:
    text = name.lower()
    for key, terms in {
        "inspire": ("inspire",), "think": ("think",), "connect": ("connect",),
        "innovate": ("innovate",), "control": ("control",), "motivate": ("motivate",),
        "design": ("design",), "alliance": ("alliance", "winning alliance", "finalist alliance"),
        "judges": ("judges", "compass", "dean"),
    }.items():
        if any(term in text for term in terms):
            return key
    return "other"


def open_tags(item: dict) -> list[str]:
    text = f"{item.get('title', '')} {item.get('source', '')} {' '.join(link.get('url', '') for link in item.get('links', []))}".lower()
    tags = ["build-thread"]
    checks = {
        "cad": ("cad", "onshape", "solidworks"), "code": ("code", "github", "software"),
        "video": ("video", "youtube", "reveal"), "portfolio": ("portfolio", "notebook"),
        "website": ("website", ".org", ".com"),
    }
    tags.extend(tag for tag, terms in checks.items() if any(term in text for term in terms))
    return tags


def enrich_team_links(item: dict) -> list[dict]:
    """Read only the public first post and retain recognized resource links."""
    source = item.get("source", "")
    if "chiefdelphi.com/t/" not in source:
        return []
    topic_json = source.rstrip("/") + ".json"
    try:
        request = urllib.request.Request(topic_json, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
        cooked = payload.get("post_stream", {}).get("posts", [{}])[0].get("cooked", "")
        urls = [unescape(value) for value in re.findall(r'href=["\'](https?://[^"\']+)', cooked)]
        accepted, seen = [], set()
        rules = (("cad", ("onshape.com", "cad.onshape")), ("code", ("github.com", "gitlab.com")),
                 ("video", ("youtube.com", "youtu.be", "vimeo.com")), ("website", (".org", ".com", ".net", ".io")))
        for url in urls:
            if "chiefdelphi.com" in url or url in seen:
                continue
            kind = next((name for name, terms in rules if any(term in url.lower() for term in terms)), None)
            if kind:
                seen.add(url)
                accepted.append({"type": kind, "url": url})
        return accepted[:8]
    except Exception:
        return []


def link_status(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            return "ok" if response.status < 400 else f"http-{response.status}"
    except Exception as error:  # A failed HEAD is advisory; records remain visible.
        return "check-failed:" + type(error).__name__


def catalogue(rows: list[tuple], check_links: bool) -> list[dict]:
    statuses = {}
    if check_links:
        with ThreadPoolExecutor(max_workers=8) as pool:
            statuses = dict(zip((row[4] for row in rows), pool.map(link_status, (row[4] for row in rows))))
    output = []
    for title, owner, category, description, url in rows:
        item = {"title": title, "owner": owner, "category": category, "description": description, "url": url, "sourceType": owner}
        if check_links:
            item["linkStatus"] = statuses[url]
        output.append(item)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-links", action="store_true")
    parser.add_argument("--skip-team-links", action="store_true", help="Skip CAD/code/video/site extraction from public Chief Delphi first posts")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))

    awards, seen_awards = [], set()
    for item in payload.get("awards", []):
        key = (item.get("season"), item.get("eventCode"), item.get("award"), item.get("teamNumber"))
        if key in seen_awards or not item.get("teamNumber"):
            continue
        seen_awards.add(key)
        item["category"] = award_category(item.get("award", ""))
        awards.append(item)

    portfolios = []
    for item in payload.get("portfolios", []):
        if item.get("teamNumber") and (item.get("pdf") or item.get("source")):
            item["category"] = "portfolio"
            portfolios.append(item)

    open_teams, seen_open = [], set()
    raw_open = payload.get("openTeams", [])
    enriched = {}
    if not args.skip_team_links:
        with ThreadPoolExecutor(max_workers=6) as pool:
            enriched = {item.get("source", ""): links for item, links in zip(raw_open, pool.map(enrich_team_links, raw_open))}
    for item in raw_open:
        number, url = item.get("teamNumber"), item.get("source", "")
        # Search titles often contain a season year; do not treat it as a team.
        if not number or number < 100 or number in (2024, 2025, 2026) or url in seen_open:
            continue
        seen_open.add(url)
        item["links"] = enriched.get(url, item.get("links", []))
        item["tags"] = open_tags(item)
        item["activity"] = int(item.get("posts") or 0)
        open_teams.append(item)

    resources = catalogue(RESOURCE_CATALOGUE, args.check_links)
    sites = catalogue(SITE_CATALOGUE, args.check_links)
    result = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "mode": "filtered-public-demo", "seasons": payload.get("seasons", {}),
        "awards": awards, "portfolios": portfolios, "openTeams": open_teams,
        "sites": sites, "resources": resources,
        "summary": {"awards": len(awards), "portfolios": len(portfolios), "openTeams": len(open_teams), "sites": len(sites), "resources": len(resources)},
        "audit": payload.get("audit", []),
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
