from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(self):
        list_enum_names = [enum.value for enum in TextType]
        if self.text_type.value not in list_enum_names:
            raise Exception("Invalid Text Type")
        mapping = {
            "text": lambda: LeafNode(None, self.text),
            "bold": lambda: LeafNode("b", self.text),
            "italic": lambda: LeafNode("i", self.text),
            "code": lambda: LeafNode("code", self.text),
            "link": lambda: LeafNode("a", self.text, {"href": self.url}),
            "image": lambda: LeafNode("img", "", {"src": self.url, "alt": self.text}),
        }
        try:
            return mapping[self.text_type.value]()
        except KeyError:
            raise Exception(f"Unhandled text type: {self.text_type.value}")

    def __eq__(self, text_node):
        if self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url:
            return True
        else:
            return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
