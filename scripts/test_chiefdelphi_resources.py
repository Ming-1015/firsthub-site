import io
import json
import unittest
from unittest.mock import patch

from collect_ftc_demo import collect_open_alliance
from filter_ftc_demo import enrich_team_links


class ChiefDelphiResourceTests(unittest.TestCase):
    def test_untagged_shared_thread_is_discovered(self):
        def fetch(url):
            topics = []
            if '12527+16095' in url:
                topics = [{'id': 525608, 'title': 'FTC 12527&16095 Build Thread|2027 Biobuzz',
                           'slug': 'ftc-12527-16095', 'tags': [], 'posts_count': 4},
                          {'id': 999, 'title': 'FRC 6328 Build Thread', 'slug': 'frc-thread'}]
            return json.dumps({'topics': topics})
        with patch('collect_ftc_demo.fetch', side_effect=fetch), patch('collect_ftc_demo.time.sleep'):
            records, _ = collect_open_alliance(1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['season'], '2026')
        self.assertIn('16095', records[0]['title'])

    def test_untitled_season_uses_creation_date(self):
        topic = {'id': 512955, 'title': 'FTC 3216 Build Thread', 'slug': 'ftc-3216',
                 'created_at': '2026-01-28T04:10:08.768Z'}
        def fetch(url):
            return json.dumps({'topics': [topic] if '12527+16095' in url else []})
        with patch('collect_ftc_demo.fetch', side_effect=fetch), patch('collect_ftc_demo.time.sleep'):
            records, _ = collect_open_alliance(1)
        self.assertEqual(records[0]['season'], '2025')

    def test_cad_in_late_paginated_reply_is_retained(self):
        first = {'id': 525608, 'post_stream': {'stream': [1, 2, 3], 'posts': [
            {'id': 1, 'cooked': ''.join(f'<a href="https://example.com/{i}">Site</a>' for i in range(9))},
            {'id': 2, 'cooked': '<a href="https://github.com/team/code">Code</a>'}]}}
        last = {'post_stream': {'posts': [{'id': 3, 'cooked':
            '<a href="https://cad.onshape.com/documents/robot?x=1&amp;y=2">CAD</a>'}]}}
        with patch('filter_ftc_demo.urllib.request.urlopen', side_effect=[
            io.BytesIO(json.dumps(first).encode()), io.BytesIO(json.dumps(last).encode())]) as request:
            links = enrich_team_links({'source': 'https://www.chiefdelphi.com/t/shared/525608'})
        self.assertEqual(request.call_count, 2)
        self.assertIn('post_ids%5B%5D=3', request.call_args.args[0].full_url)
        self.assertEqual(links[0], {'type': 'cad', 'url': 'https://cad.onshape.com/documents/robot?x=1&y=2'})
        self.assertEqual(links[1]['type'], 'code')


if __name__ == '__main__':
    unittest.main()
