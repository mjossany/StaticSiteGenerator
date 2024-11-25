from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS_TEXT = "links"
    IMAGES_TEXT = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(text_node):
        if self.text == text_node.text
        and self.text_type == text_node.text_type
        and self.url == text_node.url:
            return True
        else:
            return False
    
    def __repr__(text_node):
        return f"TextNode({text_node.text}, {text_node.text_type.value}, {text_node.url})"
