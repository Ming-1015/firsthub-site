import unittest

from collect_ftc_demo import infer_ftc_season


class ThreadSeasonTests(unittest.TestCase):
    def test_full_and_short_year_ranges(self):
        for start in range(2023, 2027):
            for separator in ('-', '–', '/'):
                for end in (str(start + 1), str(start + 1)[2:]):
                    title = f'FTC 30358 | {start}{separator}{end} Build Thread'
                    with self.subTest(title=title):
                        self.assertEqual(infer_ftc_season(title, '2023'), str(start))

    def test_calendar_year_and_fallback(self):
        self.assertEqual(infer_ftc_season('FTC 30358 2026 Build Thread', '2023'), '2025')
        self.assertEqual(infer_ftc_season('FTC 30358 Build Thread', '2026'), '2026')

    def test_two_digit_season_range(self):
        self.assertEqual(infer_ftc_season('Stuy FTC 37244 | Build Blog 26-27', '2025'), '2026')
        self.assertEqual(infer_ftc_season('FTC 12345 Build Blog 25/26', '2026'), '2025')


if __name__ == '__main__':
    unittest.main()
