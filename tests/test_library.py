import unittest
from pathlib import Path
from library import catalog, export_workflow, read_part


class WorkflowLibraryTests(unittest.TestCase):
    def test_catalog_has_three_actual_files(self):
        items = catalog()
        self.assertEqual([x['id'] for x in items], ['ES', 'CR', 'DC'])
        for item in items:
            self.assertGreater(item['bytes'], 1000)
            self.assertGreater(item['parts'], 1)
            self.assertEqual(len(item['sha256']), 64)

    def test_parts_restore_exact_file_with_unique_markers(self):
        for item in catalog():
            content = []
            for part in range(1, item['parts'] + 1):
                text = read_part(item['id'], part)
                marker = f'PART_END=TOMJ-{item["id"]}-{part:03d}-END'
                self.assertTrue(text.endswith(marker))
                self.assertEqual(text.count(marker), 1)
                self.assertLess(len(text.encode()), 5000)
                content.append(text.split('BEGIN_ORIGINAL\n', 1)[1].rsplit('\nEND_ORIGINAL\n', 1)[0])
            filename, blob = export_workflow(item['id'])
            self.assertEqual(''.join(content).encode(), blob)
            self.assertEqual(filename, f'TomJ-{item["id"]}.yml')
            self.assertEqual(blob, (Path('_assets/workflows') / filename).read_bytes())

    def test_invalid_id_and_part_report_errors(self):
        for workflow in ['../manifest.yaml', 'UNKNOWN']:
            with self.assertRaises(ValueError):
                export_workflow(workflow)
        for part in [0, -1, 1.5, '1.5', 'abc', True, 99999]:
            with self.subTest(part=part), self.assertRaises(ValueError):
                read_part('ES', part)

    def test_numeric_ui_values(self):
        self.assertEqual(read_part('ES', '1'), read_part('ES', 1.0))


if __name__ == '__main__':
    unittest.main()
