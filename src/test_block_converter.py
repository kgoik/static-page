import unittest
from block_converter import *

class BlockConverter(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_muliple_empty_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_1(self):
        md = "### this is heading text"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)

    def test_heading_6(self):
        md = "###### this is heading text"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.HEADING)

    def test_heading_incorrect(self):
        md = "####### this is heading text"
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_code_1(self):
        md = """```
this is code block
```"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.CODE)

    def test_code_2(self):
        md = """````
this is code block
```"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.CODE)

    def test_code_incorrect2(self):
        md = """``
this is code block
```"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)
    
    def test_code_incorrect3(self):
        md = """```
this is code block
``"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_quote(self):
        md = """> test1
> test2"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.QUOTE)

    def test_quote_incorrect(self):
        md = """> test1
asfasf
> test2
"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_unorderd(self):
        md = """- test1
- test2"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.UNORDERD_LIST)

    def test_unorderd_incorrect(self):
        md = """- test1
asfasf
- test2
"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_orderd(self):
        md = """1. test1
2. test2"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.ORDERD_LIST)

    def test_orderd_incorrect(self):
        md = """1. test1
asfasf
2. test2
"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_orderd_incorrect2(self):
        md = """1. test1
2. asfasf
2. test2
"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_orderd_incorrect3(self):
        md = """3. test1
"""
        type = block_to_block_type(md)
        self.assertEqual(type, BlockType.PARAGRAPH)