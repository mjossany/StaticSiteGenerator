import unittest

from block_markdown import (markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title)

class TestBlockMarkdownSplitting(unittest.TestCase):
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

class TestBlockMardownType(unittest.TestCase):

    def test_block_type_heading(self):
        block = '# Heading 1'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'heading')
    
    def test_block_type_heading_two(self):
        block = '## Heading 2'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'heading')
    
    def test_block_type_heading_with_no_space(self):
        block = '##Heading 2'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'paragraph')
    
    def test_block_type_code(self):
        block = '```This is code```'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'code')
        
    def test_block_type_code_with_two_lines(self):
        block = '```This is code\nThis too```'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'code')
    
    def test_block_type_code_not_3_backticks(self):
        block = '```This is code\nThis too``'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'paragraph')

    def test_block_type_quote(self):
        block = '> This is a quote.\n>This is another quote'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'quote')

    def test_block_type_quote_line_starting_wrong(self):
        block = '> This is a quote.\n- This is another quote'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'paragraph')

    def test_block_type_unordered_list(self):
        block = '* Item 1\n* Item 2\n* Item 3'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'unordered_list')

    def test_block_type_unordered_list_two(self):
        block = '* Item 1\n- Item 2\n* Item 3'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'unordered_list')
    
    def test_block_type_unordered_list_wrong_start(self):
        block = '* Item 1\n+ Item 2\n* Item 3'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'paragraph')
    
    def test_block_type_ordered_list(self):
        block = '1. Item 1\n2. Item 2\n3. Item 3'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'ordered_list')

    def test_block_type_ordered_list(self):
        block = '1.Item 1\n2. Item 2\n3. Item 3'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'paragraph')

    def test_block_type_ordered_list(self):
        block = '1. Item 1\n1. Item 2\n3. Item 3'
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, 'paragraph')

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_markdown_to_html_node_paragraph(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )
    
    def test_markdown_to_html_paragraphs(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_markdown_to_html_lists(self):
        markdown = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_markdown_to_html_headings(self):
        markdown = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )
    
    def test_markdown_to_html_blockquote(self):
        markdown = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

class TestExtractTile(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertEqual(extract_title(markdown), "This is a heading")

    def test_extract_title_two(self):
        markdown = """
## This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Markdown must at least one h1 block")

        
if __name__ == "__main__":
    unittest.main()