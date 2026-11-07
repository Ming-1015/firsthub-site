import unittest

from refresh_all_cad_previews import select_element


class CadPreviewSelectionTests(unittest.TestCase):
    def test_stuy_master_sketch_uses_reviewed_robot_assembly(self):
        elements = [{'id': 'sketch', 'name': 'Mastersketch', 'elementType': 'PARTSTUDIO'},
                    {'id': 'cad47d16e6eef77b0ca7bac5', 'name': 'HAL', 'elementType': 'ASSEMBLY'}]
        selected = select_element(elements, 'sketch', 'ftc', '2026', '83de7c0663bf81a8217ff2e4')
        self.assertEqual(selected['name'], 'HAL')

    def test_field_or_layout_is_never_a_robot_preview(self):
        for name in ['BIOBUZZ field', 'Mastersketch', 'Master Sketch', 'Field Layout']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                select_element([{'id': 'tab', 'name': name, 'elementType': 'PARTSTUDIO'}], 'tab', 'ftc', '2026', 'other')

    def test_requested_mechanism_is_not_replaced_by_full_robot(self):
        elements = [{'id': 'part', 'name': 'Turret', 'elementType': 'PARTSTUDIO'},
                    {'id': 'robot', 'name': 'Full Robot', 'elementType': 'ASSEMBLY'}]
        self.assertEqual(select_element(elements, 'part', 'ftc', '2026', 'other')['id'], 'part')

    def test_missing_tab_is_not_replaced_by_unrelated_model(self):
        with self.assertRaises(ValueError):
            select_element([{'id': 'old', 'name': '2024 Full Robot', 'elementType': 'ASSEMBLY'}], 'missing', 'frc', '2026', 'other')

    def test_document_link_rejects_older_robot(self):
        with self.assertRaises(ValueError):
            select_element([{'id': 'old', 'name': '2024 Full Robot', 'elementType': 'ASSEMBLY'}], None, 'frc', '2026', 'other')

    def test_document_without_tab_does_not_guess_a_small_part(self):
        with self.assertRaises(ValueError):
            select_element([{'id': 'part', 'name': 'Assembly 7', 'elementType': 'ASSEMBLY'}], None, 'frc', '2026', 'other')

    def test_archived_named_robot_can_resolve_removed_tab(self):
        elements = [{'id': 'robot', 'name': '2024 Full Robot', 'elementType': 'ASSEMBLY'}]
        self.assertEqual(select_element(elements, 'removed', 'frc', '2024', 'other', '2024 Full Robot')['id'], 'robot')

    def test_requested_older_robot_is_rejected(self):
        with self.assertRaises(ValueError):
            select_element([{'id': 'old', 'name': '2024 Full Robot', 'elementType': 'ASSEMBLY'}], 'old', 'frc', '2026', 'other')


if __name__ == '__main__':
    unittest.main()
