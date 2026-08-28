#!/usr/bin/env python3
"""Add independently traceable FTC CAD records to the public FTC collection.

The entries here are curated from the public RoboFTC robot archive and official
or maintainer project pages.  Team entries retain a direct CAD link and, where
available, their original project page.  Non-team designs are kept in the
technical-resources section so they are not presented as competition teams.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "ftc-demo-v6.json"


CAD_SOURCES = [
    {
        "season": "2024",
        "teamNumber": 11285,
        "teamName": "Patent Pending",
        "title": "11285 Patent Pending — KNOCKOUT CAD",
        "source": "https://roboftc.github.io/robots/knockout.html",
        "links": [
            {"type": "cad", "url": "https://cad.onshape.com/documents/a7b1da28b8e3acfcd89bb139/w/8f3e036bd754c5930541ff59/e/373937afed146b3a8e324c90?renderMode=0"},
            {"type": "website", "url": "https://roboftc.github.io/robots/knockout.html"},
        ],
    },
    {
        "season": "2024",
        "teamNumber": 788,
        "teamName": "Loomy Squad",
        "title": "788 Loomy Squad — LCC CAD Competition Project",
        "source": "https://roboftc.github.io/robots/loomysquad.html",
        "links": [
            {"type": "cad", "url": "https://cad.onshape.com/documents/f9edc7d2e720ea86e4e3997f/w/e9e7b7ad4a827477f1f358b1/e/897cd1fa3206b87e7a2f8f9f"},
            {"type": "website", "url": "https://roboftc.github.io/robots/loomysquad.html"},
        ],
    },
    {
        "season": "2024",
        "teamNumber": 30030,
        "teamName": "Exodus",
        "title": "30030 Exodus — LCC CAD Competition Project",
        "source": "https://roboftc.github.io/robots/exodus.html",
        "links": [
            {"type": "cad", "url": "https://cad.onshape.com/documents/49cd4bc4d188cf9592aaf817/w/f5d5bfaeb0fe6538bb09b024/e/0e47d121a4ce7c079c69fb56"},
            {"type": "website", "url": "https://roboftc.github.io/robots/exodus.html"},
        ],
    },
]

MERGED_CAD = [
    {
        "season": "2024",
        "teamNumber": 23511,
        "url": "https://cad.onshape.com/documents/ae5ff79658ff2a51ece82558/w/1babafd80652d7e5216f214c",
    },
    {
        "season": "2025",
        "teamNumber": 23511,
        "url": "https://cad.onshape.com/documents/c021b03986672773c2100272/w/74f0a8f10b4c93fb8fe556c1/e/b8bffd930c2a2d8248794936",
    },
    {
        "season": "2025",
        "teamNumber": 16010,
        "url": "https://a360.co/4qBwyjp",
    },
]

TECHNICAL_RESOURCES = [
    {
        "title": "FTC Everybot CAD (2025)",
        "owner": "official",
        "category": "mechanical",
        "description": "由 Robonauts Everybot 发布的公开 FTC 整车 CAD 与配套文档；作为通用技术项目收录，不代表竞赛队伍记录。",
        "url": "https://cad.onshape.com/documents/a2212ec4d0ff04ecfa468fab/w/de74c2fa846c84827f4ffeb0/e/a069a0c4d53cbe62662539e1",
        "sourceType": "official",
    },
    {
        "title": "ServoSwerve — 3D-Printed FTC Robot CAD",
        "owner": "community",
        "category": "mechanical",
        "description": "开源 3D 打印 FTC 机器人与 swerve 设计项目，包含 CAD、代码和构建说明。",
        "url": "https://github.com/john-j-oneill/ServoSwerve",
        "sourceType": "community",
    },
]


def add_link(record: dict, link_type: str, url: str) -> None:
    links = record.setdefault("links", [])
    if not any(link.get("url") == url for link in links):
        links.append({"type": link_type, "url": url})


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    records = data["openTeams"]
    by_season_team = {(str(row.get("season")), int(row.get("teamNumber", -1))): row for row in records}
    added = 0

    for source in CAD_SOURCES:
        key = (source["season"], source["teamNumber"])
        record = by_season_team.get(key)
        if record is None:
            record = {
                **source,
                "views": 0,
                "posts": 0,
                "sourceType": "team",
                "sourcePlatform": "website",
                "tags": ["cad", "website"],
                "activity": 1,
            }
            records.append(record)
            by_season_team[key] = record
            added += 1
        else:
            for link in source["links"]:
                add_link(record, link["type"], link["url"])
            record["tags"] = sorted(set(record.get("tags", [])) | {"cad", "website"})

    for item in MERGED_CAD:
        record = by_season_team.get((item["season"], item["teamNumber"]))
        if record is None:
            raise RuntimeError(f"Expected existing FTC record for {item['season']} #{item['teamNumber']}")
        add_link(record, "cad", item["url"])
        record["tags"] = sorted(set(record.get("tags", [])) | {"cad"})

    resource_urls = {row.get("url") for row in data["resources"]}
    for resource in TECHNICAL_RESOURCES:
        if resource["url"] not in resource_urls:
            data["resources"].append(resource)
            added += 1

    data["summary"]["openTeams"] = len(records)
    data["summary"]["resources"] = len(data["resources"])
    data["audit"].append({
        "source": "RoboFTC, Robonauts Everybot, ServoSwerve",
        "action": "Added public FTC CAD records with original project pages and direct CAD links.",
    })
    DATA_PATH.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(f"FTC CAD collection updated: {len(records)} team records, {len(data['resources'])} technical resources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
