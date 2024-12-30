from inline_mardown import split_nodes_images, split_nodes_links
from textnode import TextNode, TextType

node = TextNode(
    "Some text [to boot dev](https://www.boot.dev), [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)

split_nodes_links([node])