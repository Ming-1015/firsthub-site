"""Normalize collected award-script files and enforce the public scope."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "award-scripts"
EXCLUDED_AWARD_TERMS = ("dean's list", "woodie flowers", "volunteer of the year", "wildcard")


def main() -> None:
    for path in sorted(DATA_DIR.glob("20??.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        clean: list[dict] = []
        seen: set[tuple] = set()
        removed_scope = 0
        removed_duplicate = 0
        for record in payload.get("records", []):
            if any(term in record["awardName"].lower() for term in EXCLUDED_AWARD_TERMS):
                removed_scope += 1
                continue
            key = (record["year"], record["eventCode"], record["awardId"], record["teamNumber"])
            if key in seen:
                removed_duplicate += 1
                continue
            seen.add(key)
            clean.append(record)
        payload["records"] = clean
        payload["scope"] = "team judged awards with a published official script"
        payload["excluded"] = ["competitive advancement/results", "individual awards", "empty scripts"]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{path.name}: {len(clean)} kept, {removed_scope} out-of-scope, {removed_duplicate} duplicates")


if __name__ == "__main__":
    main()
