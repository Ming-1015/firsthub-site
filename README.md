# FirstHub

FIRSTHub · FRC Open Resource Library: https://firsthub.site

## How the data is collected

The deployed site is static: it does not crawl other websites when a visitor
opens the page. Data is collected during maintenance, reviewed, saved in the
repository, and then published as static HTML/JSON.

FIRSTHub uses a mixed workflow rather than a general-purpose web crawler:

1. **Targeted collection from public FIRST pages.** Scripts request known FIRST
   Event Web season, event, award, and team pages. They do not bypass logins or
   collect private information.
2. **Normalization and filtering.** Collected records are cleaned and
   deduplicated. Individual awards, competitive advancement/results, empty
   citations, and unrelated records are excluded from the award-script archive.
3. **Source-preserving enrichment.** Impact entries are matched to the official
   event where the award was won. Team names are refreshed from the newest
   available FIRST team page, while the original season and event are retained.
4. **Human review for community resources.** Chief Delphi Build Threads,
   GitHub repositories, Onshape documents, videos, portfolios, and technical
   tools have inconsistent formats. These are discovered with machine assistance
   but reviewed before publication. Every accepted record should link back to
   its public source.

The important files are:

- `index.html`: lightweight page structure and SEO metadata.
- `assets/css/app.css`: shared FRC/FTC presentation styles.
- `assets/js/app.js`: shared application behavior and FRC/FTC rendering logic.
- `assets/js/data.js` → `const DATA`: canonical FRC season, Impact, Open
  Alliance, Hall of Fame, and resource data.
- `assets/js/i18n.js`: interface translations, isolated from application logic.
- `data/ftc-demo-raw.json`: public FTC records as returned by the collectors.
- `data/ftc-demo.json`: normalized FTC browser dataset, loaded only after a
  visitor switches to FTC.
- `data/ftc-demo-v*.json`: versioned deployment copies used to avoid stale CDN
  data after catalogue updates.
- `scripts/collect_ftc_demo.py`: collects public FTC awards, portfolios, build
  threads, and directory links without bypassing authentication.
- `scripts/filter_ftc_demo.py`: de-duplicates and classifies the raw records,
  rejects obvious false team-number matches, and builds the website/resource
  filter fields used by the demo.
- `data/award-scripts/YYYY.json`: collected official team award citations.
- `scripts/collect_award_scripts.py`: reads public FIRST Event Web award pages.
- `scripts/clean_award_scripts.py`: applies the public scope, normalization, and
  deduplication rules.
- `scripts/enrich_impact_teams.py`: verifies Impact-winning events and refreshes
  team names from official FIRST team-season pages.
- `scripts/generate_seo_pages.py`: rebuilds the crawlable Chinese and English
  directories, structured pages, `sitemap.xml`, and `robots.txt`.

## Reproducing the maintenance workflow

Python 3.10 or newer is recommended. The scripts use the Python standard
library and do not require browser automation.

Refresh the FTC demo in two explicit stages:

```powershell
python scripts/collect_ftc_demo.py --years 2023 2024 2025
python scripts/filter_ftc_demo.py --check-links
```

The first command writes `data/ftc-demo-raw.json`; the second writes the
browser-facing `data/ftc-demo.json`. Link checks are advisory because some
working sites reject HTTP `HEAD` requests. Review the generated diff and audit
list before publishing.

Collect one or more known events for a reviewable run:

```powershell
python scripts/collect_award_scripts.py CODE CADA --year 2026
```

Collect all events listed by FIRST for a season, with a polite delay between
requests:

```powershell
python scripts/collect_award_scripts.py --year 2026 --all-events --delay 0.25
```

Then clean the collected award records and refresh Impact metadata when needed:

```powershell
python scripts/clean_award_scripts.py
python scripts/enrich_impact_teams.py
```

Finally rebuild the static search directories:

```powershell
python scripts/generate_seo_pages.py
```

Before publishing, review the Git diff and spot-check several generated links
against their official or team-published source. A successful script run is not
by itself proof that every record is correct.

## Contributing

- Report incorrect or missing data with a [GitHub issue](https://github.com/Ming-1015/firsthub-site/issues/new).
- In an issue or pull request, include the season, team number, proposed change,
  and a public source URL.
- For Open Alliance resources, specify whether the link is CAD, code, video,
  website, portfolio, or Build Thread. Please link to the team's own publication
  whenever possible.
- Season and team records are currently maintained in `assets/js/data.js` under
  `const DATA`; award citations are stored separately under
  `data/award-scripts/`.
- Do not submit private documents, access-controlled files, scraped personal
  information, or material whose team has not chosen to publish.
- Submit code or data changes through a pull request. Public visitors do not
  have direct write access to the repository.

## Known limitations

- FIRST Event Web is the source of truth for official event results and team
  names, but its page structure can change; collectors may therefore require
  maintenance.
- Open Alliance and portfolio data is not available through one uniform official
  API, so coverage is incomplete and partly curated by hand.
- Labels such as CAD, code, vision, intake, or scouting describe the public
  resource, not an endorsement or technical ranking of the team.
- FIRSTHub is an independent community archive and is not an official FIRST
  website.
