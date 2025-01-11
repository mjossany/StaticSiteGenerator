import os
from block_markdown import extract_title

current_dir = os.path.dirname(os.path.abspath("src"))
index_md_path = os.path.join(current_dir, 'content/index.md')

print(index_md_path)
with open(index_md_path) as file:
    markdown = file.read()
markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""

node = extract_title(markdown)
print(node)