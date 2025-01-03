from block_markdown import block_to_block_type, markdown_to_html_node

markdown = """
> This is a
> blockquote block

this is paragraph text

"""

node = markdown_to_html_node(markdown)
print(node.to_html())

# block = """1. First item
# 2. Second item
# 3. Third item'
# """
# block_to_block_type(block)