import unittest

from textnode import TextNode, TextType
from delimiter import Delimiter

class TestDelimiter(unittest.TestCase):
    def test_old_node_not_text_type(self):
        node = TextNode("This is text with a `code block` word", TextType.BOLD)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes[0].__repr__(), "TextNode(This is text with a `code block` word, bold, None)")
    
    def test_old_node_does_not_have_matching_closing_delimeter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        delimiter = Delimiter()
        with self.assertRaises(Exception) as context:
            delimiter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid markdown syntax. Matching closing delimiter is missing.")
    
    def test_split_nodes_delimiter_with_one_old_node_code_type(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_code_type_II(self):
        node = TextNode("`code block` word", TextType.TEXT)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_code_type_III(self):
        node = TextNode("word `code block`", TextType.TEXT)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("word ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode("", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_bold_type(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_italic_type(self):
        node = TextNode("This is text with a *code block* word", TextType.TEXT)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_with_two_old_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a code block word", TextType.BOLD)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a code block word", TextType.BOLD)
            ]
        )

    def test_split_nodes_delimiter_with_three_old_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a code block word", TextType.BOLD)
        delimiter = Delimiter()
        nodes = delimiter.split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a code block word", TextType.BOLD)
            ]
        )

if __name__ == "__main__":
    unittest.main()