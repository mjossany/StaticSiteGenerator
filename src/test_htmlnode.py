import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "hello world!", None, {'href': 'https://www.google.com', 'target': '_blank',})
        node_repr = node.__repr__()
        self.assertEqual(node_repr, "HTMLNode(p, hello world!, None, {'href': 'https://www.google.com', 'target': '_blank'})")
    
    def test_props_to_html(self):
        node = HTMLNode("p", "hello world!", None, {'href': 'https://www.google.com', 'target': '_blank',})
        node_prop_html = node.props_to_html()
        self.assertEqual(node_prop_html, ' href="https://www.google.com" target="_blank"')
    
    def test_eq(self):
        node = HTMLNode("p", "hello world!", None, {'href': 'https://www.google.com', 'target': '_blank',})
        node2 = HTMLNode("p", "hello world!", None, {'href': 'https://www.google.com', 'target': '_blank',})
        self.assertEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node_html_tag = node.to_html()
        self.assertEqual(node_html_tag, "<p>This is a paragraph of text.</p>")
    
    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node_html_tag = node.to_html()
        self.assertEqual(node_html_tag, '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_node_without_value(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        self.assertRaises(ValueError, node.to_html)
    
    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")

    def test_eq(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node_repr = node.__repr__()
        self.assertEqual(node_repr, "LeafNode(a, Click me!, None, {'href': 'https://www.google.com'})")
