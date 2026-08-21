#!/usr/bin/env python3
"""Generate crawlable static SEO pages from the inline FirstHub dataset."""

from __future__ import annotations

import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://firsthub.site"
YEARS = ["2021", "2022", "2023", "2024", "2025", "2026"]


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_data() -> dict:
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    marker = "const DATA = "
    start = source.find(marker)
    if start < 0:
        raise RuntimeError("Could not locate inline DATA payload in index.html")
    payload = source[start + len(marker):]
    data, _ = json.JSONDecoder().raw_decode(payload)
    return data


STYLE = """
:root{--blue:#3447db;--ink:#17223b;--muted:#64748b;--bg:#f5f7fb;--line:#dbe3ef}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.65}
a{color:#263ed0;text-decoration:none}a:hover{text-decoration:underline}.top{background:linear-gradient(135deg,#27368f,#4258ee);color:white;padding:34px 20px}.wrap{max-width:1080px;margin:auto}.top a{color:white}.brand{font-size:1.8rem;font-weight:800}.tag{opacity:.88}.nav{margin-top:14px;display:flex;gap:14px;flex-wrap:wrap}.nav a{border:1px solid #ffffff55;border-radius:999px;padding:4px 12px}
main{max-width:1080px;margin:28px auto;padding:0 20px 60px}h1{font-size:2rem;line-height:1.25}h2{margin-top:34px}.lead{font-size:1.08rem;color:#475569;max-width:850px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}.card,.row{background:white;border:1px solid var(--line);border-radius:12px;padding:18px}.row{margin:10px 0}.num{font-size:1.25rem;font-weight:800;color:var(--blue)}.meta{color:var(--muted);font-size:.92rem}.links{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}.pill{display:inline-block;background:#eef2ff;border-radius:999px;padding:2px 9px;font-size:.82rem}.crumb{color:var(--muted);font-size:.9rem}.language{float:right}footer{border-top:1px solid var(--line);background:white;padding:24px 20px;color:var(--muted)}
"""


TEXT = {
    "en": {
        "lang": "en",
        "brand": "FRC Community Resource Hub",
        "tag": "Community-built FRC award, team, and technical resources",
        "home": "Main site",
        "index": "Browse all resources",
        "switch": "中文",
        "overview": "Season overview",
        "impact": "Impact Award teams",
        "open": "Open Alliance teams",
        "scripts": "Award scripts",
        "impact_lead": "Official FIRST Impact Award materials, current team names, and award-event sources.",
        "open_lead": "Public Build Threads, CAD, code, videos, and team websites collected for the FRC community.",
        "script_lead": "Official team award citations written by judges and published on FIRST event pages.",
        "source": "FIRST event page",
        "essay": "Official essay",
        "build": "Build Thread",
        "code": "Code",
        "cad": "CAD",
        "video": "Video",
        "website": "Website",
        "views": "views",
        "records": "records",
        "events": "events",
    },
    "zh": {
        "lang": "zh-CN",
        "brand": "FRC 智库网",
        "tag": "开放的 FRC 奖项、队伍与技术资料库",
        "home": "互动主站",
        "index": "搜索目录",
        "switch": "English",
        "overview": "赛季总览",
        "impact": "Impact Award 获奖队伍",
        "open": "Open Alliance 开源队伍",
        "scripts": "官方颁奖词",
        "impact_lead": "整理 FIRST 官方 Impact Award 获奖材料、最新队名和获奖赛事来源。",
        "open_lead": "为 FRC 社区汇总公开的 Build Thread、CAD、代码、视频与队伍网站。",
        "script_lead": "收录 FIRST 官方赛事页面公开的评委队伍奖项颁奖词。",
        "source": "官方赛事来源",
        "essay": "官方 Essay",
        "build": "Build Thread",
        "code": "代码",
        "cad": "CAD",
        "video": "视频",
        "website": "网站",
        "views": "次浏览",
        "records": "条记录",
        "events": "场赛事",
    },
}


def page(*, lang: str, path: str, title: str, description: str, body: str, other_path: str, schema: dict) -> str:
    t = TEXT[lang]
    canonical = f"{BASE}{path}"
    other = f"{BASE}{other_path}"
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="{t['lang']}" href="{canonical}"><link rel="alternate" hreflang="{'zh-CN' if lang == 'en' else 'en'}" href="{other}"><link rel="alternate" hreflang="x-default" href="{BASE}/en/">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/og-cover.png">
<style>{STYLE}</style><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script></head>
<body><header class="top"><div class="wrap"><a class="language" href="{other}">{t['switch']}</a><div class="brand">{t['brand']}</div><div class="tag">{t['tag']}</div><nav class="nav"><a href="/">{t['home']}</a><a href="/{lang}/">{t['index']}</a></nav></div></header><main>{body}</main>
<footer><div class="wrap">{t['brand']} · Built by FRC Team 5449 · <a href="/sitemap.xml">Sitemap</a></div></footer>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"471714dc027b4b71abdb6f6098af33e9"}}'></script></body></html>"""


def write_page(path: str, content: str) -> None:
    target = ROOT / path.lstrip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def links_for_team(team: dict, t: dict) -> str:
    specs = [("cd", t["build"]), ("cad", t["cad"]), ("gh", t["code"]), ("yt", t["video"]), ("site", t["website"])]
    links = [f'<a href="{esc(team.get(key))}" rel="noopener">{label}</a>' for key, label in specs if team.get(key)]
    return '<div class="links">' + " · ".join(links) + "</div>" if links else ""


def generate(data: dict) -> list[str]:
    generated: list[str] = []
    seasons = data["seasons"]
    for lang, t in TEXT.items():
        other = "zh" if lang == "en" else "en"
        cards = []
        for year in YEARS:
            season = seasons[year]
            cards.append(f'<article class="card"><h2>{year} · {esc(season["game"])}</h2><p>{len(season.get("impact", []))} {t["impact"]}<br>{len(season.get("open", []))} {t["open"]}</p><div class="links"><a href="/{lang}/seasons/{year}/">{t["overview"]}</a><a href="/{lang}/impact/{year}/">{t["impact"]}</a><a href="/{lang}/open-teams/{year}/">{t["open"]}</a>{f'<a href="/{lang}/award-scripts/{year}/">{t["scripts"]}</a>' if year != '2021' else ''}</div></article>')
        desc = "Browse FRC Impact Award materials, official award scripts, and Open Alliance team resources by season." if lang == "en" else "按赛季浏览 FRC Impact Award 获奖队伍、官方颁奖词及 Open Alliance 开源资料。"
        body = f'<p class="crumb"><a href="/">{t["home"]}</a></p><h1>{t["brand"]} · {t["index"]}</h1><p class="lead">{desc}</p><section class="cards">{"".join(cards)}</section>'
        schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{t['brand']} {t['index']}", "url": f"{BASE}/{lang}/", "isPartOf": {"@type": "WebSite", "name": "FRC Community Resource Hub", "url": BASE}}
        write_page(f"/{lang}", page(lang=lang, path=f"/{lang}/", other_path=f"/{other}/", title=f"{t['brand']} · {t['index']}", description=desc, body=body, schema=schema)); generated.append(f"/{lang}/")

        for year in YEARS:
            season = seasons[year]
            game = season["game"]
            overview_desc = (f"Resources from the {year} FRC {game} season, including Impact Award teams, Open Alliance teams, and official award materials." if lang == "en" else f"{year} FRC {game} 赛季：Impact Award 获奖队伍、Open Alliance 开源队伍和官方奖项资料。")
            body = f'<p class="crumb"><a href="/{lang}/">{t["index"]}</a></p><h1>{year} FRC {esc(game)}</h1><p class="lead">{overview_desc}</p><section class="cards"><article class="card"><h2>{t["impact"]}</h2><p>{len(season.get("impact", []))}</p><a href="/{lang}/impact/{year}/">{t["impact"]}</a></article><article class="card"><h2>{t["open"]}</h2><p>{len(season.get("open", []))}</p><a href="/{lang}/open-teams/{year}/">{t["open"]}</a></article>{f'<article class="card"><h2>{t["scripts"]}</h2><a href="/{lang}/award-scripts/{year}/">{t["scripts"]}</a></article>' if year != '2021' else ''}</section>'
            schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{year} FRC {game}", "url": f"{BASE}/{lang}/seasons/{year}/"}
            write_page(f"/{lang}/seasons/{year}", page(lang=lang, path=f"/{lang}/seasons/{year}/", other_path=f"/{other}/seasons/{year}/", title=f"{year} FRC {game} · {t['brand']}", description=overview_desc, body=body, schema=schema)); generated.append(f"/{lang}/seasons/{year}/")

            impact_rows = []
            for team in season.get("impact", []):
                events = " · ".join(f'<a href="{esc(e.get("url"))}" rel="noopener">{esc(e.get("name"))}</a>' for e in team.get("events", []) if e.get("url"))
                links = f'<div class="links"><a href="{esc(team.get("e"))}" rel="noopener">{t["essay"]}</a></div>' if team.get("e") else ""
                impact_rows.append(f'<article class="row"><div class="num">FRC {esc(team.get("n"))} · {esc(team.get("nm"))}</div><div class="meta">{events}</div>{links}</article>')
            impact_desc = f"{year} FRC Impact Award teams, official essays, and Regional or District award-event sources." if lang == "en" else f"{year} FRC Impact Award 获奖队伍、官方 Essay 及 Regional 或 District 获奖赛事来源。"
            body = f'<p class="crumb"><a href="/{lang}/seasons/{year}/">{year} {esc(game)}</a></p><h1>{year} {t["impact"]}</h1><p class="lead">{t["impact_lead"]}</p>{"".join(impact_rows)}'
            schema = {"@context": "https://schema.org", "@type": "Dataset", "name": f"{year} FRC Impact Award teams", "description": impact_desc, "url": f"{BASE}/{lang}/impact/{year}/", "creator": {"@type": "Organization", "name": "FRC Community Resource Hub"}}
            write_page(f"/{lang}/impact/{year}", page(lang=lang, path=f"/{lang}/impact/{year}/", other_path=f"/{other}/impact/{year}/", title=f"{year} FRC Impact Award Teams · {t['brand']}", description=impact_desc, body=body, schema=schema)); generated.append(f"/{lang}/impact/{year}/")

            open_rows = []
            for team in sorted(season.get("open", []), key=lambda x: int(x.get("n", 0))):
                tag_en = {"底盘":"Drivetrain","自瞄":"Vision","吸取":"Intake","射击":"Shooter","爬升":"Climb","自动":"Autonomous","侦察":"Scouting"}
                tags = " ".join(f'<span class="pill">{esc(tag_en.get(tag, tag) if lang == "en" else tag)}</span>' for tag in team.get("tags", []))
                view_text = f'{esc(team.get("views"))} {t["views"]}' if team.get("views") else ""
                open_rows.append(f'<article class="row"><div class="num">FRC {esc(team.get("n"))} · {esc(team.get("nm"))}</div><div class="meta">{view_text} {tags}</div>{links_for_team(team, t)}</article>')
            open_desc = f"{year} FRC Open Alliance teams with public Build Threads, CAD, code, video and websites." if lang == "en" else f"{year} FRC Open Alliance 开源队伍及公开 Build Thread、CAD、代码、视频和网站。"
            body = f'<p class="crumb"><a href="/{lang}/seasons/{year}/">{year} {esc(game)}</a></p><h1>{year} {t["open"]}</h1><p class="lead">{t["open_lead"]}</p>{"".join(open_rows)}'
            schema = {"@context": "https://schema.org", "@type": "Dataset", "name": f"{year} FRC Open Alliance teams", "description": open_desc, "url": f"{BASE}/{lang}/open-teams/{year}/", "creator": {"@type": "Organization", "name": "FRC Community Resource Hub"}}
            write_page(f"/{lang}/open-teams/{year}", page(lang=lang, path=f"/{lang}/open-teams/{year}/", other_path=f"/{other}/open-teams/{year}/", title=f"{year} FRC Open Alliance Teams · {t['brand']}", description=open_desc, body=body, schema=schema)); generated.append(f"/{lang}/open-teams/{year}/")

            award_file = ROOT / "data" / "award-scripts" / f"{year}.json"
            if award_file.exists():
                awards = json.loads(award_file.read_text(encoding="utf-8"))
                records = awards.get("records") or awards.get("awards") or []
                names: dict[str, int] = {}
                events: dict[str, int] = {}
                for record in records:
                    award = str(record.get("awardName") or record.get("award_name") or record.get("award") or "Award")
                    event = str(record.get("eventName") or record.get("event_name") or record.get("event") or "Event")
                    names[award] = names.get(award, 0) + 1; events[event] = events.get(event, 0) + 1
                award_list = "".join(f'<article class="row"><strong>{esc(name)}</strong><span class="meta"> · {count}</span></article>' for name, count in sorted(names.items(), key=lambda x: (-x[1], x[0])))
                script_desc = f"{year} official FRC team award scripts indexed by award and event." if lang == "en" else f"{year} FRC 官方队伍奖项颁奖词索引，按奖项与赛事整理。"
                body = f'<p class="crumb"><a href="/{lang}/seasons/{year}/">{year} {esc(game)}</a></p><h1>{year} {t["scripts"]}</h1><p class="lead">{t["script_lead"]} {len(records)} {t["records"]} · {len(events)} {t["events"]}.</p>{award_list}<p><a href="/#{year}">{t["home"]}</a></p>'
                schema = {"@context": "https://schema.org", "@type": "Dataset", "name": f"{year} FRC official award scripts", "description": script_desc, "url": f"{BASE}/{lang}/award-scripts/{year}/", "creator": {"@type": "Organization", "name": "FRC Community Resource Hub"}}
                write_page(f"/{lang}/award-scripts/{year}", page(lang=lang, path=f"/{lang}/award-scripts/{year}/", other_path=f"/{other}/award-scripts/{year}/", title=f"{year} FRC Award Scripts · {t['brand']}", description=script_desc, body=body, schema=schema)); generated.append(f"/{lang}/award-scripts/{year}/")
    return generated


def main() -> None:
    for name in ("en", "zh"):
        path = ROOT / name
        if path.exists():
            shutil.rmtree(path)
    generated = generate(load_data())
    urls = [f"{BASE}/"] + [f"{BASE}{path}" for path in generated]
    today = date.today().isoformat()
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{esc(url)}</loc><lastmod>{today}</lastmod></url>" for url in urls) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8", newline="\n")
    print(f"Generated {len(generated)} crawlable pages plus sitemap.xml and robots.txt")


if __name__ == "__main__":
    main()
