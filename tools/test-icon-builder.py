#!/usr/bin/env python3
"""Exercise icon builder publication failures in disposable /tmp fixtures."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('nobara_icon_builder', Path(__file__).with_name('build-icons.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nobara-icons-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'icons/Nobara'
        self.output.mkdir(parents=True)
        (self.output / 'index.theme').write_text('previous working theme\n')
        self.target = self.root / 'violet.svg'
        self.target.write_text('<svg/>')
        (self.output / 'previous.svg').symlink_to(self.target)
        self.index = '[Icon Theme]\nName=Nobara\n'
        self.links = {'folder.svg': str(self.target)}
        self.enterContext(patch.object(builder, 'OUTPUT', self.output))
        self.enterContext(patch.object(builder, 'expected', return_value=(self.index, self.links)))
        self.enterContext(patch.object(sys, 'argv', ['build-icons.py', '--build']))
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))

    def assert_previous_intact(self):
        self.assertEqual((self.output / 'index.theme').read_text(), 'previous working theme\n')
        self.assertEqual((self.output / 'previous.svg').readlink(), self.target)

    def test_missing_dependency_preserves_previous_theme(self):
        self.target.unlink()
        with self.assertRaisesRegex(ValueError, 'missing icon dependency'):
            builder.main()
        self.assert_previous_intact()
        self.assertEqual(list(self.output.parent.glob('.nobara-icons-*')), [])

    def test_publish_failure_restores_previous_theme(self):
        original = Path.rename
        output = self.output
        def fail_publish(path, destination):
            if path.name == 'Nobara' and path.parent.name.startswith('.nobara-icons-') and destination == output:
                raise OSError('simulated publish failure')
            return original(path, destination)
        with patch.object(Path, 'rename', fail_publish):
            with self.assertRaisesRegex(OSError, 'simulated publish failure'):
                builder.main()
        self.assert_previous_intact()
        self.assertEqual(list(self.output.parent.glob('.nobara-icons-*')), [])

    def test_failed_restore_keeps_recoverable_backup(self):
        original = Path.rename
        output = self.output
        def fail_publish_and_restore(path, destination):
            if path.parent.name.startswith('.nobara-icons-') and destination == output:
                raise OSError('simulated publish/restore failure')
            return original(path, destination)
        with patch.object(Path, 'rename', fail_publish_and_restore), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(OSError):
                builder.main()
        backups = list(self.output.parent.glob('.nobara-icons-*/old'))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'index.theme').read_text(), 'previous working theme\n')
        self.assertEqual((backups[0] / 'previous.svg').readlink(), self.target)

    def test_successful_rebuild_replaces_only_generated_theme(self):
        builder.main()
        self.assertEqual((self.output / 'index.theme').read_text(), self.index)
        self.assertEqual((self.output / 'folder.svg').readlink(), self.target)
        self.assertFalse((self.output / 'previous.svg').exists())
        self.assertEqual(self.target.read_text(), '<svg/>')
        self.assertEqual(list(self.output.parent.glob('.nobara-icons-*')), [])


if __name__ == '__main__':
    unittest.main()
