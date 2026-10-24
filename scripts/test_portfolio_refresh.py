import copy
import json
import unittest
from unittest.mock import patch

from collect_ftc_demo import parse_portfolio_lab, collect_portfolio_lab
from filter_ftc_demo import merge_portfolios


class PortfolioRefreshTests(unittest.TestCase):
    def page(self, rows):
        return '<script>self.__next_f.push(' + json.dumps([1, 'x:' + json.dumps({'portfolios': rows}, ensure_ascii=False)]) + ')</script>'

    def row(self, **changes):
        return dict({'id': 'test-1', 'program': 'FTC', 'teamName': 'Türkçe 日本語',
                     'teamNumber': 12345, 'season': '2026 DECODE', 'pdf': '/files/a.pdf'}, **changes)

    def test_order_extra_fields_unicode_and_relative_link(self):
        row = dict(reversed(list(self.row(extra='value').items())))
        parsed = parse_portfolio_lab(self.page([row]))
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['teamName'], row['teamName'])
        self.assertEqual(parsed[0]['season'], '2025')
        self.assertEqual(parsed[0]['pdf'], 'https://www.ftcportfoliolab.org/files/a.pdf')

    def test_ending_year_does_not_override_game(self):
        for label, expected in [('2026 DECODE', '2025'), ('2027 BIOBUZZ', '2026'), ('2025 INTO THE DEEP', '2024')]:
            self.assertEqual(parse_portfolio_lab(self.page([self.row(season=label)]))[0]['season'], expected)

    def test_exclude_frc_and_bad_records(self):
        self.assertEqual(parse_portfolio_lab(self.page([self.row(program='FRC'), self.row(pdf=None)])), [])

    def test_slash_prefixed_absolute_url(self):
        url = 'https://drive.google.com/file/d/example/view'
        self.assertEqual(parse_portfolio_lab(self.page([self.row(pdf='/' + url)]))[0]['pdf'], url)

    def test_failure_and_empty_are_reported(self):
        for value in ['', '<html>Unavailable</html>']:
            with patch('collect_ftc_demo.fetch', return_value=value):
                rows, audit = collect_portfolio_lab()
                self.assertEqual(rows, [])
                self.assertEqual(audit['status'], 'failed')
        with patch('collect_ftc_demo.fetch', side_effect=TimeoutError('test')):
            self.assertEqual(collect_portfolio_lab()[1]['status'], 'failed')

    def test_preserve_every_old_field_and_missing_records(self):
        old = [self.row(custom='manual correction')]
        snapshot = copy.deepcopy(old)
        rows, conflicts = merge_portfolios(old, [self.row(season='2027', pdf='https://changed.example')])
        self.assertEqual(rows, snapshot)
        self.assertEqual(old, snapshot)
        self.assertTrue(conflicts)
        self.assertEqual(merge_portfolios(old, [])[0], snapshot)

    def test_additions_and_idempotence(self):
        old = [self.row()]
        new = [self.row(id='new')]
        rows, _ = merge_portfolios(old, new)
        self.assertEqual(len(rows), 2)
        self.assertEqual(merge_portfolios(rows, new)[0], rows)


if __name__ == '__main__':
    unittest.main()
