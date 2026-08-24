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
    ("FTC Stack", "learning", "community", "按主题整理 FTC 编程库、控制框架与常用工具的参考站。", "https://www.ftcstack.com/docs/reference/libraries"),
    ("Blueprint", "learning", "community", "由 FTC 队伍建设的软硬件教程、交互式模拟器与代码案例知识库。", "https://ftcblueprint.com/"),
    ("FIRST FTC Team Resources", "official", "official", "FIRST 官方 StarterBot、检查清单、接线、SDK、模拟器与队伍支持资源入口。", "https://ftc-resources.firstinspires.org/ftc/team"),
    ("FTC Open House", "learning", "community", "面向新老 FTC 队伍的机械、CAD、编程与队伍运营学习入口。", "https://ftcopenhouse.com/"),
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
    ("Blueprint · FTC Knowledge Base", "community", "learning", "FTC 队伍维护的软硬件指南、模拟器、作品集与代码评审站。", "https://ftcblueprint.com/"),
    ("FTC Stack", "community", "programming", "集中介绍 FTC 编程库、框架与工具的技术参考站。", "https://www.ftcstack.com/docs/reference/libraries"),
    ("FTC Open House", "community", "learning", "覆盖入门、CAD、机械与编程主题的社区学习站。", "https://ftcopenhouse.com/"),
    ("Tech Ninja Team 9929 Archive", "team", "awards", "FTC 9929 公开的多赛季 Engineering Portfolio 与 Engineering Notebook 档案。", "https://ftc9929.com/past-season-engineering-notebooks/"),
    ("Techalongs 17062 Portfolio Library", "team", "awards", "FTC 17062 整理的历年作品集、模板与其他队伍示例入口。", "https://sites.google.com/view/techalongs/portfolios-notebooks"),
    ("Potential Energy 19706 Resources", "team", "awards", "FTC 19706 公开的作品集、工程笔记与培训资料。", "https://www.potentialenergyftc.com/resources"),
]

CURATED_PORTFOLIOS = [
    {"id": "team-9929-2024", "season": "2024", "teamNumber": 9929, "teamName": "Tech Ninja Team", "seasonLabel": "2024 Into The Deep", "level": "Team-published", "award": "Engineering Portfolio", "pdf": "https://ftc9929.com/past-season-engineering-notebooks/", "sourceType": "team", "source": "https://ftc9929.com/past-season-engineering-notebooks/"},
    {"id": "team-17062-2024", "season": "2024", "teamNumber": 17062, "teamName": "Techalongs", "seasonLabel": "2024 Into The Deep", "level": "Team-published", "award": "Engineering Portfolio", "pdf": "https://sites.google.com/view/techalongs/portfolios-notebooks", "sourceType": "team", "source": "https://sites.google.com/view/techalongs/portfolios-notebooks"},
    {"id": "team-19706-2024", "season": "2024", "teamNumber": 19706, "teamName": "Potential Energy", "seasonLabel": "2024 Into The Deep", "level": "Team-published", "award": "Engineering Portfolio", "pdf": "https://www.potentialenergyftc.com/resources", "sourceType": "team", "source": "https://www.potentialenergyftc.com/resources"},
    {"id": "team-14374-2023", "season": "2023", "teamNumber": 14374, "teamName": "Dark Matter", "seasonLabel": "2023 Centerstage", "level": "Team-published", "award": "Engineering Portfolio", "pdf": "https://darkmatterrobotics.com/wp-content/uploads/2024/03/14374_DMportfolio_CenterstageSTATE_FINAL-SMALL.pdf", "sourceType": "team", "source": "https://darkmatterrobotics.com/"},
    {"id": "team-23396-2023", "season": "2023", "teamNumber": 23396, "teamName": "Hivemind", "seasonLabel": "2023 Centerstage", "level": "Regional", "award": "Think Award", "pdf": "https://www.chiefdelphi.com/t/team-23396-hivemind-2024-centerstage-cad-release-portfolio/468348", "sourceType": "team", "source": "https://www.chiefdelphi.com/t/team-23396-hivemind-2024-centerstage-cad-release-portfolio/468348"},
    {"id": "team-288-2021", "season": "2021", "teamNumber": 288, "teamName": "Spare Parts", "seasonLabel": "2021 Freight Frenzy", "level": "Team-published", "award": "Engineering Portfolio", "pdf": "https://www.chiefdelphi.com/t/team-288-spare-parts-2021-2022-freight-frenzy-engineering-portfolio/414943", "sourceType": "team", "source": "https://www.chiefdelphi.com/t/team-288-spare-parts-2021-2022-freight-frenzy-engineering-portfolio/414943"},
]

CURATED_TEAM_RESOURCES = [
    {"season": "2023", "teamNumber": 23396, "teamName": "Hivemind", "title": "Centerstage CAD release and Engineering Portfolio", "posts": 8, "sourceType": "team", "sourcePlatform": "chief-delphi", "source": "https://www.chiefdelphi.com/t/team-23396-hivemind-2024-centerstage-cad-release-portfolio/468348"},
    {"season": "2024", "teamNumber": 13193, "teamName": "Code Blue", "title": "INTO THE DEEP Road Runner robot code", "posts": 0, "sourceType": "team", "sourcePlatform": "github", "source": "https://github.com/loarado/Code_Blue_13193_Roadrunner_INTO_THE_DEEP", "links": [{"type": "code", "url": "https://github.com/loarado/Code_Blue_13193_Roadrunner_INTO_THE_DEEP"}]},
    {"season": "2025", "teamNumber": 492, "teamName": "Titan Robotics", "title": "Reusable FTC robot framework and season template", "posts": 0, "sourceType": "team", "sourcePlatform": "github", "source": "https://github.com/trc492/FtcTemplate", "links": [{"type": "code", "url": "https://github.com/trc492/FtcTemplate"}]},
    {"season": "2025", "teamNumber": 6448, "teamName": "Jesuit Blue Jays", "title": "Cross-platform Webots FTC Simulator", "posts": 0, "sourceType": "team", "sourcePlatform": "github", "source": "https://github.com/BlueJays6448/FTCSimulator", "links": [{"type": "code", "url": "https://github.com/BlueJays6448/FTCSimulator"}]},
    {"season": "2022", "teamNumber": 6547, "teamName": "Cobalt Colts", "title": "Engineering Portfolio template discussion and sample", "posts": 0, "sourceType": "team", "sourcePlatform": "reddit", "source": "https://www.reddit.com/r/FTC/comments/10ej3yy/engineering_portfolio_template_from_6547_cobalt/", "links": [{"type": "website", "url": "https://www.reddit.com/r/FTC/comments/10ej3yy/engineering_portfolio_template_from_6547_cobalt/"}]},
    {"season": "2025", "teamNumber": 14779, "teamName": "Spontaneous Construction", "title": "Team technical wiki and public updates", "posts": 0, "sourceType": "team", "sourcePlatform": "x", "source": "https://x.com/SponConFTC", "links": [{"type": "website", "url": "https://x.com/SponConFTC"}, {"type": "website", "url": "http://projectrobotica.wiki"}]},
    {"season": "2025", "teamNumber": 14291, "teamName": "Small Town Robotics", "title": "Public team updates on X", "posts": 0, "sourceType": "team", "sourcePlatform": "x", "source": "https://x.com/SmallTownFTC", "links": [{"type": "website", "url": "https://x.com/SmallTownFTC"}]},
    {"season": "2024", "teamNumber": 701, "teamName": "The GONK Squad", "title": "2025 INTO THE DEEP Robot Reveal", "posts": 0, "sourceType": "team", "sourcePlatform": "youtube", "source": "https://www.youtube.com/watch?v=efxuzZgxmoA", "links": [{"type": "video", "url": "https://www.youtube.com/watch?v=efxuzZgxmoA"}]},
    {"season": "2024", "teamNumber": 19705, "teamName": "FTC WX WXY WXYZ", "title": "2024–25 INTO THE DEEP Season Final Robot Reveal", "posts": 0, "sourceType": "team", "sourcePlatform": "youtube", "source": "https://www.youtube.com/watch?v=oG_gRNIp2DU", "links": [{"type": "video", "url": "https://www.youtube.com/watch?v=oG_gRNIp2DU"}]},
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


def clean_mojibake(value: str) -> str:
    if not isinstance(value, str) or not any(marker in value for marker in ("â", "Ã", "ð")):
        return value
    try:
        return value.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value


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
    previous = json.loads(args.output.read_text(encoding="utf-8")) if args.output.exists() else {}
    previous_links = {item.get("source", ""): item.get("links", []) for item in previous.get("openTeams", [])}

    awards, seen_awards = [], set()
    for item in payload.get("awards", []):
        key = (item.get("season"), item.get("eventCode"), item.get("award"), item.get("teamNumber"))
        if key in seen_awards or not item.get("teamNumber"):
            continue
        seen_awards.add(key)
        item["category"] = award_category(item.get("award", ""))
        awards.append(item)

    portfolios, seen_portfolios = [], set()
    for item in payload.get("portfolios", []) + CURATED_PORTFOLIOS:
        key = item.get("id") or (item.get("season"), item.get("teamNumber"), item.get("pdf"))
        if key not in seen_portfolios and (item.get("teamNumber") is not None) and (item.get("pdf") or item.get("source")):
            seen_portfolios.add(key)
            item["teamName"] = clean_mojibake(item.get("teamName", ""))
            if isinstance(item.get("pdf"), str) and item["pdf"].startswith("/http"):
                item["pdf"] = item["pdf"][1:]
            item["category"] = "portfolio"
            portfolios.append(item)

    open_teams, seen_open = [], set()
    raw_open = payload.get("openTeams", []) + CURATED_TEAM_RESOURCES
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
        combined_links = item.get("links", []) + previous_links.get(url, []) + enriched.get(url, [])
        item["links"] = list({(link.get("type"), link.get("url")): link for link in combined_links if link.get("url")}.values())
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
