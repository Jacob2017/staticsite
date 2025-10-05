import unittest

from block import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block_md = "This is just a normal paragraph"
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.PARA, block_type)

    def test_heading(self):
        block_md = "#### Heading 4"
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_invalid_heading(self):
        block_md = "####### Heading 7"
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.PARA, block_type)

    def test_code(self):
        block_md = """```
# This is commented code
```"""
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.CODE, block_type)

    def test_quote(self):
        block_md = """> Line 1 of the quote
> Line 2 of the quote"""
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_ulist(self):
        block_md = """- Cabbage
- Lettuce
- Tomatoes
- Chicken Breast"""
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.ULIST, block_type)

    def test_olist(self):
        block_md = """1. Cabbage
2. Lettuce
3. Tomatoes
4. Chicken Breast"""
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.OLIST, block_type)

    def test_invalid_olist(self):
        block_md = """1. Cabbage
3. Skipped a few
99. Ninety Nine
100. One Hundred"""
        block_type = block_to_block_type(block_md)
        self.assertEqual(BlockType.PARA, block_type)
