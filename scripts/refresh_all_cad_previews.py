"""Audit every FRC/FTC CAD URL and cache a preview for each public model."""
import argparse
import asyncio
import base64
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import collect_cad_previews as cad

ONSHAPE = re.compile(r'https://[^/]*onshape\.com/documents/([a-f0-9]{24})/(w|v|m)/([a-f0-9]{24})(?:/e/([a-f0-9]{24}))?', re.I)
# The post links to master sketches containing the field. These are the robot
# assemblies in those exact documents, checked against the source post.
STUY_ASSEMBLIES = {
    '83de7c0663bf81a8217ff2e4': 'cad47d16e6eef77b0ca7bac5',
    '930a2d441a45b8af0626adde': '011ff7905a736e638f8a6cca',
}
STUY_TEAMS = {'83de7c0663bf81a8217ff2e4': 37244, '2133dd596725f9288a16be01': 37245,
              'e9e06fbc5658c4e596404573': 37246, '930a2d441a45b8af0626adde': 37247}
# Visual review: these public tabs are field/layout or placeholder geometry,
# and must not appear as representative team robot images.
EXCLUDED_DOCUMENTS = {
    '025c7f8286f7bc12b9a5687f': 'Field structure, not a robot model',
    '8d89565820455e63a18491d4': 'Placeholder block, not a robot model',
    '32d35195096474e63d47b95e': 'Layout geometry; robot preview cannot be identified',
}


class PageMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.image = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('property', attrs.get('name')) == 'og:image':
            self.image = attrs.get('content', '')


def select_element(elements, requested, program, year, did, prior_name=None):
    if did in EXCLUDED_DOCUMENTS:
        raise ValueError(EXCLUDED_DOCUMENTS[did])
    override = STUY_ASSEMBLIES.get(did)
    selected = next((e for e in elements if e['id'] == (override or requested)), None)
    # Some archive links point at a now-removed/drawing tab. A previously
    # recorded assembly name can resolve that exact archived model again.
    selected_name = (selected or {}).get('name', '').lower()
    selected_years = set(re.findall(r'\b20(?:1\d|2\d)\b', selected_name))
    if program == 'frc' and prior_name and (not selected or selected.get('elementType') not in ('ASSEMBLY', 'PARTSTUDIO') or any(w in selected_name for w in ('field', 'sketch', 'layout')) or selected_years - {str(year)}):
        matches = [e for e in elements if e.get('name') == prior_name and e.get('elementType') in ('ASSEMBLY', 'PARTSTUDIO')]
        if len(matches) == 1:
            selected = matches[0]
    if selected:
        name = selected.get('name', '').lower()
        if any(word in name for word in ('field', 'mastersketch', 'master sketch', 'master sk', 'layout', 'playground', 'sandbox')):
            raise ValueError('Linked tab is a field/layout or design sketch, not a robot model')
        if selected.get('elementType') in ('ASSEMBLY', 'PARTSTUDIO'):
            named_years = set(re.findall(r'\b20(?:1\d|2\d)\b', name))
            allowed = {str(year), str(int(year) + 1)} if program == 'ftc' else {str(year)}
            if named_years - allowed:
                raise ValueError('Linked model explicitly names a different season')
            return selected
    # Do not replace an unavailable linked tab with an unrelated assembly.
    if requested:
        raise ValueError('Linked CAD tab is missing or is not a renderable model')
    candidates = [e for e in elements if e.get('elementType') in ('ASSEMBLY', 'PARTSTUDIO')]
    candidates = [e for e in candidates if not any(w in e.get('name', '').lower() for w in ('field', 'sketch', 'playground', 'sandbox'))]
    candidates = [e for e in candidates if any(w in e.get('name', '').lower() for w in ('robot', 'main', 'chassis', 'drivetrain', 'turret', 'intake', 'shooter'))]
    def score(e):
        name = e.get('name', '').lower()
        years = set(re.findall(r'20(?:1\d|2\d)', name))
        allowed = {str(year), str(int(year) + 1)} if program == 'ftc' else {str(year)}
        if years - allowed:
            return -10000
        return cad.element_score({**e, 'name': re.sub(r'20(?:1\d|2\d)', '', name)}, '', str(year))
    candidates.sort(key=score, reverse=True)
    if not candidates or score(candidates[0]) < 0:
        raise ValueError('No identifiable public robot or mechanism model')
    return candidates[0]


async def preview(browser, job, timeout):
    program, year, number, url, prior = job
    result = {'url': url, 'status': 'unavailable'}
    digest = hashlib.sha256(url.encode()).hexdigest()[:12]
    relative = f'assets/cad-previews/{program}/{year}/{number}-{digest}.webp'
    output = cad.ROOT / relative
    context = await browser.new_context(user_agent='FIRSTHub public CAD preview collector')
    try:
        match = ONSHAPE.match(url)
        if match:
            did, kind, wid, eid = match.groups()
            endpoint = f'https://cad.onshape.com/api/documents/d/{did}/{kind}/{wid}/elements?withThumbnails=true'
            response = await context.request.get(endpoint, timeout=timeout)
            if not response.ok:
                raise ValueError(f'Public model access returned HTTP {response.status}')
            elements = await response.json()
            element = select_element(elements, eid, program, year, did, prior.get('element'))
            name = element.get('name', 'CAD')
            model_url = f'https://cad.onshape.com/documents/{did}/{kind}/{wid}/e/{element["id"]}'
            result.update(element=name, modelUrl=model_url)
            if did in STUY_TEAMS:
                result['label'] = f'{STUY_TEAMS[did]} · {name}'
            if output.exists():
                return {**result, 'status': 'ok', 'image': relative, 'method': 'cached-model-render'}
            # Reuse a known render only when it represents this selected tab.
            if prior.get('image') and prior.get('element') == name and (cad.ROOT / prior['image']).exists():
                return {**result, 'status': 'ok', 'image': prior['image'], 'method': 'cached-model-render'}
            route = 'assemblies' if element['elementType'] == 'ASSEMBLY' else 'partstudios'
            render = f'https://cad.onshape.com/api/v14/{route}/d/{did}/{kind}/{wid}/e/{element["id"]}/shadedviews'
            try:
                response = await context.request.get(render, params={'viewMatrix': cad.FRONT_UPPER_VIEW_MATRIX, 'outputWidth': '640', 'outputHeight': '360', 'pixelSize': '0', 'edges': 'show', 'useAntiAliasing': 'true'}, timeout=timeout)
                if not response.ok:
                    raise ValueError(f'Public renderer HTTP {response.status}')
                payload = await response.json()
                cad.encode_webp(base64.b64decode(payload['images'][0]), output)
                method = 'model-render'
            except Exception as render_error:
                sizes = element.get('thumbnailInfo', {}).get('sizes', []) if element.get('thumbnailInfo') else []
                thumbnails = sorted(sizes, key=lambda s: int(s.get('size', '0x0').split('x')[0]), reverse=True)
                if not thumbnails:
                    raise render_error
                response = await context.request.get(thumbnails[0]['href'], timeout=timeout)
                if not response.ok:
                    raise render_error
                cad.encode_webp(await response.body(), output)
                method = 'source-model-thumbnail'
            result.update(status='ok', image=relative, method=method)
        else:
            # Other platforms may expose a model-specific public social preview.
            response = await context.request.get(url, timeout=timeout)
            if not response.ok:
                raise ValueError(f'Public CAD page HTTP {response.status}')
            if response.headers.get('content-type', '').startswith('image/'):
                cad.encode_webp(await response.body(), output)
                return {**result, 'status': 'ok', 'image': relative, 'element': 'CAD', 'method': 'source-model-thumbnail'}
            if urlparse(response.url).hostname in ('github.com', 'drive.google.com'):
                raise ValueError('CAD download page does not expose a model-specific public render')
            metadata = PageMetadata()
            metadata.feed(await response.text())
            image_url = urljoin(response.url, metadata.image) if metadata.image else ''
            if not image_url or any(w in image_url.lower() for w in ('logo', 'default', 'placeholder', 'favicon', 'opengraph', 'og-image', 'social-share')):
                raise ValueError('Source does not expose a model-specific public preview')
            image_response = await context.request.get(image_url, timeout=timeout)
            if not image_response.ok:
                raise ValueError(f'Source thumbnail HTTP {image_response.status}')
            cad.encode_webp(await image_response.body(), output)
            result.update(status='ok', image=relative, element='CAD', method='source-model-thumbnail')
    except Exception as error:
        result['reason'] = str(error).split('Call log:')[0][:240]
    finally:
        await context.close()
    return result


async def main(args):
    frc = cad.load_data()
    ftc_path = cad.ROOT / 'data/ftc-demo-v6.json'
    ftc = json.loads(ftc_path.read_text(encoding='utf-8'))
    records = []
    for year, season in frc['seasons'].items():
        for record in season['open']:
            if record.get('cad'):
                records.append(('frc', year, record['n'], record, [record['cad']]))
    for record in ftc['openTeams']:
        urls = list(dict.fromkeys(l['url'] for l in record.get('links', []) if l['type'] == 'cad'))
        if urls:
            records.append(('ftc', record['season'], record['teamNumber'], record, urls))
    jobs = {}
    for program, year, number, record, urls in records:
        prior = {p['url']: p for p in record.get('cadPreviews', [])}
        if record.get('cadPreview') and record.get('cadPreviewVerified') is not False:
            source = record.get('cadPreviewUrl', record.get('cad'))
            if program == 'ftc' and not source and len(urls) == 1:
                source = urls[0]
            prior[source] = {'image': record['cadPreview'], 'element': record.get('cadPreviewElement', ''), **prior.get(source, {})}
        for url in urls:
            jobs.setdefault((program, year, url), (program, year, number, url, prior.get(url, {})))
    results = {}
    if getattr(args, 'retry_selection', False):
        for key, job in list(jobs.items()):
            previous = job[4]
            if previous.get('status') and (previous['status'] == 'ok' or not any(word in previous.get('reason', '') for word in ('Linked CAD tab', 'Linked model', 'field/layout'))):
                results[key] = previous
                del jobs[key]
    semaphore = asyncio.Semaphore(args.workers)
    total = len(jobs) + len(results)
    async with cad.async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, executable_path=args.executable_path)
        async def collect(key, job):
            async with semaphore:
                result = await preview(browser, job, args.timeout * 1000)
                # Retry transient access failures once, without another page crawl.
                if result['status'] != 'ok' and any(s in result.get('reason', '') for s in ('429', 'ECONNRESET', 'Timeout')):
                    await asyncio.sleep(3)
                    result = await preview(browser, job, args.timeout * 1000)
                results[key] = result
                print(f'{len(results)}/{total} {job[0]} {job[1]} #{job[2]} {result["status"]}: {result.get("element", result.get("reason", ""))}', flush=True)
        await asyncio.gather(*(collect(key, job) for key, job in jobs.items()))
        await browser.close()
    for program, year, number, record, urls in records:
        record['cadPreviews'] = [results[(program, year, url)] for url in urls]
        for entry in record['cadPreviews']:
            if entry['status'] != 'ok':
                entry.pop('image', None)
            match = ONSHAPE.match(entry['url'])
            if match and match[1] in STUY_TEAMS and entry.get('element'):
                entry['label'] = f'{STUY_TEAMS[match[1]]} · {entry["element"]}'
        # Retire the old single-image slot, including misleading field renders.
        for field in ('cadPreview', 'cadPreviewUrl', 'cadPreviewElement'):
            record.pop(field, None)
    cad.save_data(frc)
    for name in ('ftc-demo-v6.json', 'ftc-demo.json'):
        (cad.ROOT / 'data' / name).write_text(json.dumps(ftc, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    report = {'generatedAt': datetime.now(timezone.utc).isoformat(), 'total': total, 'ok': sum(r['status'] == 'ok' for r in results.values()), 'unavailable': [{'program': k[0], 'year': k[1], **r} for k, r in results.items() if r['status'] != 'ok']}
    (cad.ROOT / 'data/all-cad-previews-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'total': total, 'ok': report['ok'], 'unavailable': len(report['unavailable'])}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--timeout', type=int, default=25)
    parser.add_argument('--retry-selection', action='store_true')
    parser.add_argument('--executable-path', default='C:/Program Files/Google/Chrome/Application/chrome.exe' if sys.platform == 'win32' else None)
    asyncio.run(main(parser.parse_args()))
