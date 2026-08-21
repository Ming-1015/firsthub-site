# FirstHub

FRC Community Resource Hub: https://firsthub.site

## Data workflow

The deployed site is static. The current data source is embedded in the page:

- `/index.html`, under `const DATA`, is the canonical season/team dataset.
- `data/award-scripts/*.json` stores the award-script datasets.
- `scripts/generate_seo_pages.py` regenerates the crawlable SEO directories.

After editing `const DATA`, rebuild the crawlable directories:

```powershell
python scripts/generate_seo_pages.py
```

`generate_seo_pages.py` rebuilds the crawlable English and Chinese season,
Impact, Open Alliance, and award-script indexes, plus `sitemap.xml` and
`robots.txt`. Run it after changing the inline season data or award-script JSON.

## Contributing

- Report incorrect or missing data with a [GitHub issue](https://github.com/Ming-1015/firsthub-site/issues/new).
- Season and team records are maintained in `/index.html` under `const DATA`.
- Submit code or data changes through a pull request; public visitors do not have direct write access to the repository.
