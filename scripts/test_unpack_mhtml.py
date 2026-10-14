"""Run with: python3 -m unittest discover -s scripts -p 'test_*.py'."""

from email.message import EmailMessage
from pathlib import Path
import tempfile
import unittest

from unpack_mhtml import unpack


class UnpackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def archive(self):
        message = EmailMessage()
        message['Snapshot-Content-Location'] = 'https://example.test/'
        message.make_related()
        for location, text, subtype in [
            ('https://example.test/frame', '<p>Frame</p>', 'html'),
            ('https://example.test/', '<h1>Café</h1>', 'html'),
            ('../../escape.css', ':root { --brand: #123456; }', 'css'),
        ]:
            part = EmailMessage()
            part.set_content(text, subtype=subtype, charset='utf-8', cte='quoted-printable')
            part['Content-Location'] = location
            message.attach(part)
        binary = EmailMessage()
        binary.set_content(b'\x00\xff\x10', maintype='font', subtype='woff2')
        binary['Content-Location'] = 'https://example.test/font.woff2'
        message.attach(binary)
        path = self.root / 'page.mhtml'
        path.write_bytes(message.as_bytes())
        return path

    def test_resources_main_document_and_safe_filenames(self):
        output = self.root / 'out'
        result = unpack(self.archive(), output)
        self.assertEqual((output / 'index.html').read_text().strip(), '<h1>Café</h1>')
        self.assertEqual(len(result['resources']), 4)
        for item in result['resources']:
            file = output / item['path']
            self.assertTrue(file.resolve().is_relative_to(output.resolve()))
            self.assertEqual(file.stat().st_size, item['bytes'])
        self.assertEqual((output / result['resources'][-1]['path']).read_bytes(), b'\x00\xff\x10')
        self.assertFalse((self.root / 'escape.css').exists())

    def test_existing_output_is_preserved(self):
        output = self.root / 'out'
        output.mkdir()
        marker = output / 'keep.txt'
        marker.write_text('keep')
        with self.assertRaises(FileExistsError):
            unpack(self.archive(), output)
        self.assertEqual(marker.read_text(), 'keep')

    def test_plain_html_is_rejected_without_partial_output(self):
        source = self.root / 'plain.mhtml'
        source.write_text('<html>Not an archive</html>')
        output = self.root / 'out'
        with self.assertRaises(ValueError):
            unpack(source, output)
        self.assertFalse(output.exists())

    def test_missing_html_is_rejected(self):
        source = self.root / 'missing.mhtml'
        message = EmailMessage()
        message.make_related()
        part = EmailMessage()
        part.set_content('body {}', subtype='css')
        message.attach(part)
        source.write_bytes(message.as_bytes())
        with self.assertRaises(ValueError):
            unpack(source, self.root / 'out')


if __name__ == '__main__':
    unittest.main()
