from inline_mardown import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

node = TextNode(
    "Some text [to boot dev](https://www.boot.dev), [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)

split_nodes_link([node])