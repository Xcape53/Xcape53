"""Behavior checks for the public project activity panel."""

import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / 'scripts' / 'activity.py'


def load_activity():
    if not SCRIPT.exists():
        raise AssertionError('Public activity generator has not been implemented')
    spec = importlib.util.spec_from_file_location('activity', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def commit(title='Improve transcription', author='Xcape53', date='2026-09-30T12:00:00Z'):
    return {'sha': 'abc123', 'html_url': 'https://github.com/Xcape53/Yapper/commit/abc123',
            'author': {'login': author},
            'commit': {'message': title, 'author': {'email': 'private@example.invalid', 'date': date}}}


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.activity = load_activity()
        self.now = datetime(2026, 10, 1, tzinfo=timezone.utc)
        self.metadata = {'name': 'Yapper', 'private': False,
                         'html_url': 'https://github.com/Xcape53/Yapper'}

    def test_private_repository_is_excluded(self):
        private = {**self.metadata, 'private': True}
        self.assertIsNone(self.activity.normalize_repository(private, [commit()], None))

    def test_bot_changes_do_not_count_as_project_work(self):
        records = [commit(), commit('Refresh generated cards', 'github-actions[bot]')]
        result = self.activity.normalize_repository(self.metadata, records, None)
        self.assertEqual(len(result['commits']), 1)
        self.assertEqual(result['commits'][0]['title'], 'Improve transcription')

    def test_subject_is_single_line_and_private_email_is_not_persisted(self):
        result = self.activity.normalize_repository(self.metadata, [commit('Add channel\n\nPrivate details')], None)
        encoded = json.dumps(result)
        self.assertEqual(result['commits'][0]['title'], 'Add channel')
        self.assertNotIn('private@example.invalid', encoded)
        self.assertNotIn('Private details', encoded)

    def test_snapshot_excludes_changes_outside_the_90_day_window(self):
        records = [commit(date='2026-09-30T12:00:00Z'), commit('Old work', date='2026-05-01T12:00:00Z')]
        repo = self.activity.normalize_repository(self.metadata, records, None)
        snapshot = self.activity.build_snapshot([repo], self.now)
        self.assertEqual(snapshot['commit_count'], 1)
        self.assertEqual(len(snapshot['recent']), 1)

    def test_failed_fetch_preserves_last_valid_files(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            marker = output / 'activity-dark.svg'
            marker.write_text('last valid graphic')
            def unavailable(_path):
                raise OSError('Service unavailable')
            self.assertFalse(self.activity.refresh(output, unavailable, self.now))
            self.assertEqual(marker.read_text(), 'last valid graphic')
            self.assertFalse((output / 'data' / 'activity.json').exists())

    def test_empty_activity_has_an_honest_empty_state(self):
        snapshot = self.activity.build_snapshot([], self.now)
        self.assertEqual(snapshot['commit_count'], 0)
        svg = self.activity.render(snapshot, 'dark')
        self.assertIn('No public project changes in this period', svg)

    def test_untrusted_commit_title_is_xml_escaped(self):
        repo = self.activity.normalize_repository(self.metadata, [commit('Fix <script> & audio')], None)
        snapshot = self.activity.build_snapshot([repo], self.now)
        svg = self.activity.render(snapshot, 'light')
        self.assertIn('&lt;script&gt; &amp;', svg)
        import xml.etree.ElementTree as ET
        ET.fromstring(svg)


if __name__ == '__main__':
    unittest.main()
