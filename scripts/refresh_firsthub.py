"""Run FIRSTHub public-data collectors and rebuild search pages."""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'data/firsthub-refresh-state.json'
REPORT = ROOT / 'data/firsthub-refresh-report.json'


def due(now, state):
    last = state.get('lastSuccessfulRefresh')
    return not last or (now - datetime.fromisoformat(last)).total_seconds() >= 259200


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-due', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    state = json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {}
    if args.check_due:
        print('true' if due(now, state) else 'false')
        return
    seasons = json.loads(re.fullmatch(r'const DATA = (.*);\s*', (ROOT / 'assets/js/data.js').read_text(encoding='utf-8'), re.S)[1])['seasons']
    steps = [['collect_frc_youtube.py', '--limit-per-query', '50'], ['enrich_impact_teams.py']]
    for year in sorted(seasons):
        if int(year) >= 2022:
            steps.append(['collect_award_scripts.py', '--year', year, '--all-events', '--workers', '8'])
    steps += [['clean_award_scripts.py'],
              ['collect_ftc_demo.py', '--years', '2023', '2024', '2025', '2026', '--chief-pages', '4', '--merge'],
              ['collect_ftc_youtube.py', '--limit-per-query', '50'],
              ['filter_ftc_demo.py', '--output', 'data/ftc-demo-v6.json', '--check-links'],
              ['collect_cad_previews.py', '--workers', '2', '--limit', '30', '--retries', '2'],
              ['collect_ftc_cad_previews.py', '--timeout', '45', '--workers', '2'],
              ['generate_seo_pages.py']]
    if args.dry_run:
        for step in steps:
            print(' '.join(step))
        return
    report = {'startedAt': now.isoformat(), 'status': 'running', 'steps': []}
    ftc_before = json.loads((ROOT / 'data/ftc-demo-v6.json').read_text(encoding='utf-8'))
    award_counts = {}
    for path in (ROOT / 'data/award-scripts').glob('*.json'):
        award_counts[path.stem] = len(json.loads(path.read_text(encoding='utf-8')).get('records', []))
    try:
        for step in steps:
            print('Running ' + step[0], flush=True)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts' / step[0]), *step[1:]], cwd=ROOT, timeout=5400)
            report['steps'].append({'command': step, 'returnCode': result.returncode})
            if result.returncode:
                raise RuntimeError(f'{step[0]} failed ({result.returncode})')
            if step[0] == 'collect_award_scripts.py':
                year = step[step.index('--year') + 1]
                payload = json.loads((ROOT / 'data/award-scripts' / f'{year}.json').read_text(encoding='utf-8'))
                if payload.get('failures') or not payload.get('records'):
                    raise RuntimeError(f'{year} official awards incomplete; publication stopped')
                if len(payload['records']) < award_counts.get(year, 0) * 0.9:
                    raise RuntimeError(f'{year} awards dropped over 10%; publication stopped for review')
            if step[0] == 'filter_ftc_demo.py':
                ftc_after = json.loads((ROOT / 'data/ftc-demo-v6.json').read_text(encoding='utf-8'))
                for key in ('awards', 'portfolios', 'openTeams', 'resources', 'sites'):
                    if len(ftc_after.get(key, [])) < len(ftc_before.get(key, [])) * 0.9:
                        raise RuntimeError(f'FTC {key} dropped over 10%; publication stopped for review')
        report.update(status='success', finishedAt=datetime.now(timezone.utc).isoformat())
        STATE.write_text(json.dumps({'lastSuccessfulRefresh': report['finishedAt']}, indent=2) + '\n', encoding='utf-8')
    except Exception as error:
        report.update(status='failed', error=str(error))
        raise
    finally:
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
