import unittest

from block_markdown import (markdown_to_blocks)

class TestBlockMarkdown(unittest.TestCase):
    def test_mardown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])

    def test_mardown_to_blocks_stripping(self):
        markdown = """
 # This is a heading 

 This is a paragraph of text. It has some **bold** and *italic* words inside of it. 

 * This is the first list item in a list block
* This is a list item
* This is another list item 
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])

    def test_mardown_to_blocks_empty_blocks_removal(self):
        markdown = """
# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])
    
if __name__ == "__main__":
    unittest.main()