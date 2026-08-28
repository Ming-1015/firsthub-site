#!/usr/bin/env python3
"""Withdraw unverified CAD preview metadata for a season.

This keeps the source CAD links intact.  It deliberately does not delete
rendered files: they may be needed while records are being audited, but are no
longer referenced by the site or the preview manifest.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "js" / "data.js"
MANIFEST_PATH = ROOT / "assets" / "cad-previews" / "manifest.json"
DATA_PATTERN = re.compile(r"^const DATA = (.*);\s*$", re.DOTALL)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("year", help="Season year whose unverified previews should be withdrawn")
    args = parser.parse_args()

    match = DATA_PATTERN.match(DATA_PATH.read_text(encoding="utf-8"))
    if not match:
        raise RuntimeError("Could not locate DATA payload")
    data = json.loads(match.group(1))
    season = data["seasons"].get(args.year)
    if not season:
        raise RuntimeError(f"Unknown season: {args.year}")

    withdrawn = 0
    for team in season.get("open", []):
        if team.get("cadPreviewVerified") is True:
            continue
        changed = False
        for key in ("cadPreview", "cadPreviewElement", "cadPreviewAngle"):
            changed = team.pop(key, None) is not None or changed
        if changed:
            team["cadPreviewVerified"] = False
            withdrawn += 1

    DATA_PATH.write_text(
        "const DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )

    manifest = {"entries": [], "failures": []}
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])
    manifest["entries"] = [entry for entry in entries if str(entry.get("year")) != args.year]
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Withdrew {withdrawn} unverified CAD previews for {args.year}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
