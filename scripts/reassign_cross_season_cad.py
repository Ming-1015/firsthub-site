#!/usr/bin/env python3
"""Remove known incorrect 2026 CAD previews and retain verified 2025 models.

The listed source documents were checked as either a component/non-robot model
or a 2025 full-robot model that had been attached to a 2026 team record.
Public CAD links remain available where they belong; only the mistaken 2026
association is removed.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "js" / "data.js"
MANIFEST_PATH = ROOT / "assets" / "cad-previews" / "manifest.json"
DATA_PATTERN = re.compile(r"^const DATA = (.*);\s*$", re.DOTALL)

# 1485 was reported as 2485; FIRSTHub has no 2026 team 1485 CAD record, while
# #2485 is the listed TPU tread model and is therefore included here.
INCORRECT_2026 = {
    95, 135, 195, 353, 451, 1360, 1732, 1806, 2019, 2485, 3501, 4276,
    4607, 4795, 4930, 6418, 6423, 8230, 9312, 9551, 9751,
}
MOVE_TO_2025 = {353, 1360, 1732, 4276, 4795, 4930, 6423}
CAD_FIELDS = ("cad", "cadPreview", "cadPreviewElement", "cadPreviewAngle", "cadPreviewVerified")


def main() -> int:
    match = DATA_PATTERN.match(DATA_PATH.read_text(encoding="utf-8"))
    if not match:
        raise RuntimeError("Could not locate DATA payload")
    data = json.loads(match.group(1))
    source = {team["n"]: team for team in data["seasons"]["2026"].get("open", [])}
    target = data["seasons"]["2025"].setdefault("open", [])
    target_by_number = {team["n"]: team for team in target}

    moved = 0
    for number in sorted(MOVE_TO_2025):
        team = source[number]
        destination = target_by_number.get(number)
        if destination is None:
            destination = {"n": number, "nm": team.get("nm", "")}
            target.append(destination)
            target_by_number[number] = destination
        # Do not overwrite a 2025 CAD record that is already present.  For
        # missing 2025 cards, carry only the CAD information — never 2026 code,
        # videos, tags, or popularity values.
        if not destination.get("cad"):
            for field in CAD_FIELDS:
                if field in team:
                    destination[field] = team[field]
            moved += 1

    removed = 0
    for number in sorted(INCORRECT_2026):
        team = source.get(number)
        if not team:
            continue
        changed = False
        for field in CAD_FIELDS:
            changed = team.pop(field, None) is not None or changed
        removed += int(changed)

    target.sort(key=lambda team: int(team["n"]))
    DATA_PATH.write_text(
        "const DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["entries"] = [
        entry
        for entry in manifest.get("entries", [])
        if not (str(entry.get("year")) == "2026" and int(entry.get("team", -1)) in INCORRECT_2026)
    ]
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Removed {removed} incorrect 2026 CAD associations; added {moved} missing 2025 CAD cards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
