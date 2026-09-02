#!/usr/bin/env python3
"""Apply a reviewed 2026 FRC resource correction.

This is deliberately a narrow, repeatable correction: it removes the invalid
Team 2 record, removes Team 157's unverified CAD association, and attaches the
team-supplied Team 418 2026 CAD preview.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "js" / "data.js"
INDEX_PATH = ROOT / "index.html"
MANIFEST_PATH = ROOT / "assets" / "cad-previews" / "manifest.json"
PREVIEW = "assets/cad-previews/2026/418-team-supplied-2026.png"


def main() -> None:
    source = DATA_PATH.read_text(encoding="utf-8")
    match = re.fullmatch(r"const DATA = (.*);\s*", source, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Could not parse assets/js/data.js")
    data = json.loads(match.group(1))
    teams = data["seasons"]["2026"]["open"]

    before = len(teams)
    teams[:] = [team for team in teams if team.get("n") != 2]
    if len(teams) != before - 1:
        raise RuntimeError("Expected exactly one 2026 Team 2 record")

    team_157 = next(team for team in teams if team.get("n") == 157)
    for field in ("cad", "cadPreview", "cadPreviewElement", "cadPreviewAngle", "cadPreviewVerified"):
        team_157.pop(field, None)

    team_418 = next(team for team in teams if team.get("n") == 418)
    team_418.update({
        "cadPreview": PREVIEW,
        "cadPreviewElement": "2026 robot CAD preview (team-supplied)",
        "cadPreviewAngle": "team-supplied",
        "cadPreviewVerified": True,
    })

    DATA_PATH.write_text(
        "const DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    version = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    index = INDEX_PATH.read_text(encoding="utf-8")
    INDEX_PATH.write_text(
        re.sub(r"assets/js/data\.js\?v=[^\"']+", f"assets/js/data.js?v={version}", index),
        encoding="utf-8",
    )

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = [entry for entry in manifest["entries"] if not (entry["year"] == "2026" and entry["team"] in {2, 157, 418})]
    entries.append({
        "year": "2026",
        "team": 418,
        "cad": team_418["cad"],
        "preview": PREVIEW,
        "element": "2026 robot CAD preview (team-supplied)",
        "angle": "team-supplied",
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "status": "team-supplied",
    })
    manifest.update({"generatedAt": datetime.now(timezone.utc).isoformat(), "entries": entries})
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated 2026: removed Team 2, removed Team 157 CAD, added Team 418 preview.")


if __name__ == "__main__":
    main()
