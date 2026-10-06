"""Cache previews of the explicitly linked FTC Onshape tabs."""
import asyncio
import json
from datetime import datetime, timezone

import collect_cad_previews as cad


async def run(args):
    path = cad.ROOT / 'data' / 'ftc-demo-v6.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    report = {'entries': [], 'failures': []}
    # Keep the source's exact tab: guessing another assembly can mix seasons.
    original_score = cad.element_score
    cad.element_score = lambda element, requested, year: (
        original_score(element, requested, year)
        if element.get('id') == requested else -10000
    )
    jobs = []
    for record in data['openTeams']:
        links = [link['url'] for link in record.get('links', [])
                 if link.get('type') == 'cad' and cad.ONSHAPE_PATTERN.match(link['url'])]
        if not links:
            continue
        team = {'n': record['teamNumber'], 'cad': links[0]}
        year = 'ftc/' + str(record['season'])
        output, relative = cad.preview_path(year, team)
        if output.exists():
            record.update(cadPreview=relative, cadPreviewUrl=links[0])
        else:
            jobs.append((record, year, team))
    if args.limit:
        jobs = jobs[:args.limit]
    print(f'FTC CAD: {len(jobs)} missing previews', flush=True)
    async with cad.async_playwright() as playwright:
        options = {'headless': True}
        if args.executable_path:
            options['executable_path'] = args.executable_path
        browser = await playwright.chromium.launch(**options)
        async def collect(record, year, team):
            try:
                entry = await cad.collect_one(browser, year, team, args.timeout * 1000)
                record.update(cadPreview=team['cadPreview'], cadPreviewUrl=team['cad'],
                              cadPreviewElement=team['cadPreviewElement'])
                report['entries'].append(entry)
                print(f"OK {year} #{team['n']}: {entry['element']}", flush=True)
            except Exception as error:
                message = str(error).split('Call log:')[0].strip()[:300]
                report['failures'].append({'season': record['season'], 'team': team['n'],
                                           'cad': team['cad'], 'error': message})
                print(f"SKIP {year} #{team['n']}: {message}", flush=True)
        semaphore = asyncio.Semaphore(args.workers)
        async def guarded(job):
            async with semaphore:
                await collect(*job)
        await asyncio.gather(*(guarded(job) for job in jobs))
        await browser.close()
    for filename in ('ftc-demo-v6.json', 'ftc-demo.json'):
        (cad.ROOT / 'data' / filename).write_text(
            json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    report['generatedAt'] = datetime.now(timezone.utc).isoformat()
    report['totalPreviews'] = sum(bool(x.get('cadPreview')) for x in data['openTeams'])
    (cad.ROOT / 'data' / 'ftc-cad-previews-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"FTC previews available: {report['totalPreviews']}", flush=True)


if __name__ == '__main__':
    asyncio.run(run(cad.parse_args()))
