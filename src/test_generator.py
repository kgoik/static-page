import unittest

from block import BlockType
from generator import extract_title

class TestGenerator(unittest.TestCase):

    def test_markdown_heading(self):
        md = """
# This is h1 heading 

This is a paragraph
"""
        title = extract_title(md)
        self.assertEqual(title, "This is h1 heading")


    def test_markdown_heading_2(self):
        md = """
## This is h2 heading 

This is a paragraph

# This is an actual h1 heading
"""
        title = extract_title(md)
        self.assertEqual(title, "This is an actual h1 heading")

    def test_markdown_heading_error(self):
        md = """

"""
        with self.assertRaisesRegex(Exception, "markdown cannot be empty"):
            extract_title(md)

    def test_markdown_heading_error_2(self):
        md = None
        with self.assertRaisesRegex(Exception, "markdown cannot be empty"):
            extract_title(md)

    def test_markdown_heading_error(self):
        md = """
## This is h2 heading 

This is a paragraph

### This is an h3 heading
"""
        with self.assertRaisesRegex(ValueError, "No title in the markdown file"):
            extract_title(md)


