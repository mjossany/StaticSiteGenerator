import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_italic(self):
        node = TextNode("Test", TextType.ITALIC, "https://google.com")
        node2 = TextNode("Test", TextType.ITALIC, "https://google.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Test", TextType.BOLD, "https://google.com")
        node2 = TextNode("Test", TextType.ITALIC, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_normal_text(self):
        text_node = TextNode("Testando", TextType.TEXT)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.__repr__(), 'LeafNode(None, Testando, None, None)')
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Testando")

    def test_text_node_to_html_node_bold_text(self):
        text_node = TextNode("Testando", TextType.BOLD)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.__repr__(), 'LeafNode(b, Testando, None, None)')
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "Testando")

    def test_text_node_to_html_node_italic_text(self):
        text_node = TextNode("Testando", TextType.ITALIC)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.__repr__(), 'LeafNode(i, Testando, None, None)')
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "Testando")
    
    def test_text_node_to_html_node_code_text(self):
        text_node = TextNode("Testando", TextType.CODE)
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.__repr__(), 'LeafNode(code, Testando, None, None)')
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "Testando")

    def test_text_node_to_html_node_link_text(self):
        text_node = TextNode("Testando", TextType.LINK, "https://google.com")
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.__repr__(), "LeafNode(a, Testando, None, {'href': 'https://google.com'})")
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "Testando")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_text_node_to_html_node_images_text(self):
        text_node = TextNode("Testando", TextType.IMAGES, "https://google.com")
        html_node = text_node.text_node_to_html_node()
        self.assertEqual(html_node.__repr__(), "LeafNode(img, "", None, {'src': 'https://google.com', 'alt': 'Testando'})")
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://google.com", "alt": "Testando"})

if __name__ == "__main__":
    unittest.main()