# FirstHub

FRC Knowledge Hub: https://firsthub.site

## Data workflow

The deployed site is static, but its source data is maintained separately:

- `data/seasons_data.json` is the canonical season/team dataset.
- `scripts/deep_mine_github.py` discovers public season repositories, verifies
  teams against FIRST Event Web, derives machine/program tags, and writes an
  audit report before applying changes.
- `scripts/validate_data.py` checks duplicates, tag limits, and malformed URLs.
- `scripts/rebuild_site.py` replaces the inline `DATA` payload in `index.html`.

Example maintenance run:

```powershell
python scripts/deep_mine_github.py --year 2026
python scripts/deep_mine_github.py --year 2026 --apply
python scripts/validate_data.py
python scripts/rebuild_site.py
```

Review `data/github_candidates_2026.json` before publishing. Git commits and
deployment are intentionally separate steps.
