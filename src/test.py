from inline_mardown import text_to_textnodes
from textnode import TextNode, TextType

text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

text_to_textnodes(text)