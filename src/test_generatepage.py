import unittest

from generatepage import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        md = """
# Heading 1
## Heading 2"""
        self.assertEqual("Heading 1", extract_title(md))

    def test_second_line(self):
        md = """
something before the title
# Heading 1
something after the title"""
        self.assertEqual("Heading 1", extract_title(md))

    def test_hash_in_title(self):
        md = """
# Heading 1 with #
## Heading 2"""
        self.assertEqual("Heading 1 with #", extract_title(md))

    def test_error(self):
        md = """
No heading
No heading
No heading"""
        with self.assertRaises(ValueError):
            extract_title(md)
