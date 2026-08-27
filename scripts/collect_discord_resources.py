"""Collect public team resource links from explicitly approved Discord channels.

This collector is deliberately narrow.  Discord does not offer a public,
site-wide search API, so it only reads channels listed in
``data/discord-sources.json`` after the server owner has added FIRSTHub's bot.
It never stores message text, usernames, membership lists, or attachments.
Only a qualifying team number, an external public resource URL, and the
permalink needed to audit the finding are written to the repository.

Setup:

    set DISCORD_BOT_TOKEN=...  # PowerShell: $env:DISCORD_BOT_TOKEN='...'
    python scripts/collect_discord_resources.py

The bot needs View Channels and Read Message History only.  Enable the
Message Content privileged intent in the Discord Developer Portal if it is
going to classify links from message content.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "data" / "discord-sources.json"
DEFAULT_OUTPUT = ROOT / "data" / "discord-resources.json"
DEFAULT_STATE = ROOT / "data" / "discord-state.json"
API_ROOT = "https://discord.com/api/v10"
USER_AGENT = "FIRSTHub approved Discord resource collector/1.0 (+https://firsthub.site/)"
URL_RE = re.compile(r"https?://[^\s<>\]\[\](){}\"']+", re.I)
TEAM_RE = re.compile(r"\b(?:FRC|FTC)\s*(?:team\s*)?[#:\-]?\s*(\d{2,5})\b|\bteam\s*[#:\-]?\s*(\d{2,5})\b", re.I)
SEASON_RE = re.compile(r"\b(20(?:2[0-9]|3[0-9]))(?:[-–](\d{2,4}))?\b")


def load_json(path: Path, fallback: object) -> object:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def request_json(url: str, token: str) -> list[dict]:
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bot {token}", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"Discord API returned HTTP {error.code}: {body}") from error


def external_urls(text: str) -> list[str]:
    urls: list[str] = []
    for raw in URL_RE.findall(text or ""):
        url = raw.rstrip(".,;:!?)]}\"")
        host = urllib.parse.urlparse(url).netloc.lower()
        # A Discord jump URL is provenance, not a public team resource.
        if host.endswith("discord.com") or host.endswith("discord.gg"):
            continue
        if url not in urls:
            urls.append(url)
    return urls[:8]


def team_number(text: str, program: str) -> int | None:
    for match in TEAM_RE.finditer(text or ""):
        prefix = match.group(0).lower()
        number = int(match.group(1) or match.group(2))
        # A configured FTC/FRC channel may use "Team 1234" shorthand.  When
        # the post names the other program, reject it instead of guessing.
        if "frc" in prefix and program != "frc":
            continue
        if "ftc" in prefix and program != "ftc":
            continue
        return number
    return None


def season_value(text: str, configured: object) -> str | None:
    if isinstance(configured, (str, int)) and str(configured):
        return str(configured)
    match = SEASON_RE.search(text or "")
    if not match:
        return None
    start, end = match.groups()
    return f"{start}-{end[-2:]}" if end else start


def resource_kind(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.lower()
    path = urllib.parse.urlparse(url).path.lower()
    if "onshape" in host or "cad" in host or path.endswith((".step", ".stp", ".f3d", ".sldprt")):
        return "cad"
    if host in {"github.com", "gitlab.com", "codeberg.org"}:
        return "code"
    if "youtube" in host or host == "youtu.be" or "vimeo" in host:
        return "video"
    if path.endswith(".pdf"):
        return "document"
    return "website"


def configured_channels(config: object) -> list[dict]:
    channels: list[dict] = []
    for source in (config or {}).get("sources", []):
        program = str(source.get("program", "")).lower()
        guild_id = str(source.get("guildId", ""))
        if program not in {"frc", "ftc"} or not guild_id:
            continue
        for channel in source.get("channels", []):
            channel_id = str(channel.get("id", ""))
            if channel_id:
                channels.append({
                    "id": channel_id,
                    "name": str(channel.get("name", channel_id)),
                    "guildId": guild_id,
                    "guildName": str(source.get("name", guild_id)),
                    "program": program,
                    "season": channel.get("season", source.get("season")),
                })
    return channels


def collect_channel(channel: dict, token: str, after: str, max_pages: int) -> tuple[list[dict], str]:
    newest = after
    records: list[dict] = []
    before = ""
    for _ in range(max_pages):
        query = {"limit": "100"}
        if after:
            query["after"] = after
        elif before:
            query["before"] = before
        endpoint = f"{API_ROOT}/channels/{channel['id']}/messages?{urllib.parse.urlencode(query)}"
        messages = request_json(endpoint, token)
        if not messages:
            break
        for message in messages:
            message_id = str(message.get("id", ""))
            if message_id and (not newest or int(message_id) > int(newest)):
                newest = message_id
            text = str(message.get("content") or "")
            number = team_number(text, channel["program"])
            if not number:
                continue
            for url in external_urls(text):
                records.append({
                    "program": channel["program"],
                    "teamNumber": number,
                    "season": season_value(text, channel.get("season")),
                    "kind": resource_kind(url),
                    "resourceUrl": url,
                    "sourceMessageUrl": f"https://discord.com/channels/{channel['guildId']}/{channel['id']}/{message_id}",
                    "sourceGuild": channel["guildName"],
                    "sourceChannel": channel["name"],
                    "evidence": "explicit team number + public external URL",
                })
        if after or len(messages) < 100:
            break
        before = str(messages[-1].get("id", ""))
        if not before:
            break
    return records, newest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--max-pages", type=int, default=5, help="Maximum 100-message pages per configured channel")
    parser.add_argument("--dry-run", action="store_true", help="Validate configuration without calling Discord")
    args = parser.parse_args()

    config = load_json(args.config, {"version": 1, "sources": []})
    channels = configured_channels(config)
    if not channels:
        print("No approved Discord channels are configured; nothing collected.")
        return 0
    if args.dry_run:
        print(f"Validated {len(channels)} approved Discord channel(s); dry run made no API calls.")
        return 0
    token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        print("DISCORD_BOT_TOKEN is required when approved Discord channels are configured.", file=sys.stderr)
        return 2

    state = load_json(args.state, {"version": 1, "channels": {}})
    previous = load_json(args.output, {"version": 1, "records": []})
    existing = {(item.get("sourceMessageUrl"), item.get("resourceUrl")): item for item in previous.get("records", [])}
    failures: list[str] = []
    for channel in channels:
        channel_state = state.setdefault("channels", {}).setdefault(channel["id"], {})
        try:
            found, newest = collect_channel(channel, token, str(channel_state.get("after", "")), args.max_pages)
            for record in found:
                existing[(record["sourceMessageUrl"], record["resourceUrl"])] = record
            if newest:
                channel_state["after"] = newest
            channel_state["lastCheckedAt"] = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
        except RuntimeError as error:
            failures.append(f"{channel['guildName']} / #{channel['name']}: {error}")

    records = sorted(existing.values(), key=lambda item: (item["program"], -int(item["teamNumber"]), item["resourceUrl"]))
    dump_json(args.output, {
        "version": 1,
        "generatedAt": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "policy": "Approved channels only; no message text, usernames, member lists, or files are stored.",
        "records": records,
    })
    dump_json(args.state, state)
    print(f"Collected {len(records)} auditable public resource link(s) from {len(channels)} approved channel(s).")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
