import unittest

from htmlnode import HTMLNode

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