import unittest

from textnode import TextNode, TextType
from inline_mardown import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_links, split_nodes_images)

class TestInlineMarkdown(unittest.TestCase):
    def test_old_node_not_text_type(self):
        node = TextNode("This is text with a `code block` word", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes[0].__repr__(), "TextNode(This is text with a `code block` word, bold, None)")
    
    def test_old_node_does_not_have_matching_closing_delimeter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid markdown syntax. Matching closing delimiter is missing.")
    
    def test_split_nodes_delimiter_with_one_old_node_code_type(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_code_type_starting_the_string(self):
        node = TextNode("`code block` word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_code_type_ending_the_string(self):
        node = TextNode("word `code block`", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("word ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_bold_type_doubled(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_bold_and_italic_type(self):
        node = TextNode("This is text with a **bolded** word and *another*", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.ITALIC),
            ]
        )

    def test_split_nodes_delimiter_with_one_old_node_bold_type(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
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
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
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
        nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
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
        nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a code block word", TextType.BOLD)
            ]
        )

class TestImageAndLinkMardown(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

class TestSplitNodesLinks(unittest.TestCase):

    def test_split_node_with_no_link(self):
        node = TextNode("This is just a text.",TextType.TEXT)
        list_new_nodes = split_nodes_links([node])
        self.assertEqual(list_new_nodes, [node])

    def test_split_node_with_no_text_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev)",TextType.TEXT)
        list_new_nodes = split_nodes_links([node])
        self.assertEqual(list_new_nodes, [[TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]])

    def test_split_node_with_text_before_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)",TextType.TEXT)
        list_new_nodes = split_nodes_links([node])
        self.assertEqual(list_new_nodes, [[TextNode("This is text with a link ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]])

    def test_split_node_with_text_after_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev) This is text with a link",TextType.TEXT)
        list_new_nodes = split_nodes_links([node])
        self.assertEqual(list_new_nodes, [[TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" This is text with a link", TextType.TEXT)]])

    def test_split_node_with_no_text_and_two_links(self):
        node = TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        list_new_nodes = split_nodes_links([node])
        self.assertEqual(list_new_nodes, [[TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")]])

    def test_split_node_with_two_links_and_text_before_middle_after(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) the end.",TextType.TEXT)
        list_new_nodes = split_nodes_links([node])
        self.assertEqual(list_new_nodes, [[TextNode("This is text with a link ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), TextNode(" the end.", TextType.TEXT)]])

    def test_split_node_receiving_two_nodes(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)",TextType.TEXT)
        node2 = TextNode(" and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        list_new_nodes = split_nodes_links([node, node2])
        self.assertEqual(list_new_nodes, [[TextNode("This is text with a link ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")], [TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")]])

class TestSplitNodesImages(unittest.TestCase):

    def test_split_node_with_no_image(self):
        node = TextNode("This is just a text.",TextType.TEXT)
        list_new_nodes = split_nodes_images([node])
        self.assertEqual(list_new_nodes, [node])

    def test_split_node_with_no_text_image(self):
        node = TextNode("![to boot dev](https://www.boot.dev)",TextType.TEXT)
        list_new_nodes = split_nodes_images([node])
        self.assertEqual(list_new_nodes, [[TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")]])

    def test_split_node_with_text_before_image(self):
        node = TextNode("This is text with a image ![to boot dev](https://www.boot.dev)",TextType.TEXT)
        list_new_nodes = split_nodes_images([node])
        self.assertEqual(list_new_nodes, [[TextNode("This is text with a image ", TextType.TEXT), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")]])

    def test_split_node_with_text_after_image(self):
        node = TextNode("![to boot dev](https://www.boot.dev) This is text with a image",TextType.TEXT)
        list_new_nodes = split_nodes_images([node])
        self.assertEqual(list_new_nodes, [[TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"), TextNode(" This is text with a image", TextType.TEXT)]])

    def test_split_node_with_no_text_and_two_images(self):
        node = TextNode("![to boot dev](https://www.boot.dev)![to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        list_new_nodes = split_nodes_images([node])
        self.assertEqual(list_new_nodes, [[TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"), TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")]])

    def test_split_node_with_two_images_and_text_before_middle_after(self):
        node = TextNode("This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) the end.", TextType.TEXT)
        list_new_nodes = split_nodes_images([node])
        self.assertEqual(list_new_nodes, [[TextNode("This is text with a image ", TextType.TEXT), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"), TextNode(" the end.", TextType.TEXT)]])

    def test_split_node_receiving_two_nodes(self):
        node = TextNode("This is text with a image ![to boot dev](https://www.boot.dev)",TextType.TEXT)
        node2 = TextNode(" and ![to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        list_new_nodes = split_nodes_images([node, node2])
        self.assertEqual(list_new_nodes, [[TextNode("This is text with a image ", TextType.TEXT), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")], [TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")]])

if __name__ == "__main__":
    unittest.main()