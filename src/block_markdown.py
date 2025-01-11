import re
from htmlnode import (ParentNode, LeafNode)
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in blocks]
    filtered_blocks = [block for block in stripped_blocks if block]
    return filtered_blocks

def block_to_block_type(block):
    if is_heading(block):
        return 'heading'
    if is_code(block):
        return 'code'
    if is_quote(block):
        return 'quote'
    if is_unordered_list(block):
        return 'unordered_list'
    if is_ordered_list(block):
        return 'ordered_list'
    return 'paragraph'
    
def is_heading(block):
    heading_regex = r'^#{1,6} '
    return re.match(heading_regex, block) is not None

def is_code(block):
    first_three_characters = block[:3]
    last_three_characters = block[-3:]
    if first_three_characters == '```' and last_three_characters == '```':
        return 'code'

def is_quote(block):
    block_lines = block.split('\n')
    for line in block_lines:
        if line[0] != '>':
            return False
    return True

def is_unordered_list(block):
    list_lines = block.split("\n")
    for line in list_lines:
        if line[:2] != "* " and line[:2] != "- ":
            return False
    return True

def is_ordered_list(block):
    list_lines = block.split("\n")
    for i in range(len(list_lines)):
        if list_lines[i][:3] != f"{i + 1}. ":
            return False
    return True

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes_list = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            tag, value = set_heading_info(block)
            html_nodes_list.append(LeafNode(tag, value))
            continue
        if block_type == "code":
            block = block.replace('```', '')
            code_leaf_node = LeafNode('code', block)
            code_parent_node = ParentNode('pre', [code_leaf_node])
            html_nodes_list.append(code_parent_node)
        if block_type == "quote":
            block = block.replace('\n', ' ')
            block = block.replace('> ', '')
            html_nodes_list.append(LeafNode('blockquote', block))
        if block_type == "unordered_list":
            block_lines = block.split('\n')
            for i in range(len(block_lines)):
                block_lines[i] = block_lines[i][2:]
            unordered_list_node_children = []
            for line in block_lines:
                line_nodes = []
                line_nodes.extend(text_to_textnodes(line))
                line_children_nodes = []
                for node in line_nodes:
                    line_children_nodes.append(node.text_node_to_html_node())
                line_parent_node = ParentNode('li', line_children_nodes)
                unordered_list_node_children.append(line_parent_node)
            html_nodes_list.append(ParentNode('ul', unordered_list_node_children))
        if block_type == "ordered_list":
            block_lines = block.split('\n')
            for i in range(len(block_lines)):
                block_lines[i] = block_lines[i][3:]
            unordered_list_node_children = []
            for line in block_lines:
                line_nodes = []
                line_nodes.extend(text_to_textnodes(line))
                line_children_nodes = []
                for node in line_nodes:
                    line_children_nodes.append(node.text_node_to_html_node())
                line_parent_node = ParentNode('li', line_children_nodes)
                unordered_list_node_children.append(line_parent_node)
            html_nodes_list.append(ParentNode('ol', unordered_list_node_children))
        if block_type == "paragraph":
            block = block.replace('\n', ' ')
            text_nodes = text_to_textnodes(block)
            children_nodes = []
            for node in text_nodes:
                children_nodes.append(node.text_node_to_html_node())
            html_nodes_list.append(ParentNode('p', children_nodes))
            continue
    parent_html_node = ParentNode('div', html_nodes_list)
    return parent_html_node

def set_heading_info(block):
    block_parts = block.split(' ', 1)
    return f"h{len(block_parts[0])}", block_parts[1]

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith('# '):
            return block[2:]
    raise Exception("Markdown must at least one h1 block")