import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("Invalid markdown syntax. Matching closing delimiter is missing.")
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
                            
def split_nodes_images(old_nodes):
    for node in old_nodes:
        return extract_markdown_images(node.text)

def split_nodes_links(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if len(extracted_links) == 0:
            return [node]
        new_nodes = []
        node_text_copy = node.text
        for link in extracted_links:
            sections = node_text_copy.split(f"[{link[0]}]({link[1]})")
            if sections[0] != '' and sections[1] != '':
                for i in range(len(sections)):
                    matches = extract_markdown_links(sections[i])
                    if len(matches) == 0 and i == 0:
                        new_nodes.append(TextNode(sections[i], TextType.TEXT))
                        new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                        node_text_copy = node_text_copy.replace(sections[i] + f"[{link[0]}]({link[1]})", "")
                    elif len(matches) == 0:
                        new_nodes.append(TextNode(sections[i], TextType.TEXT))
                        node_text_copy = node_text_copy.replace(sections[i], "")
                    else:
                        continue
            else:
                if sections[0] == '' and sections[1] == '':
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    node_text_copy = node_text_copy.replace(f"[{link[0]}]({link[1]})", "")
                    continue
                for section in sections:
                    matches = extract_markdown_links(section)
                    if len(matches) == 0:
                        if section != '':
                            new_nodes.append(TextNode(section, TextType.TEXT))
                            node_text_copy = node_text_copy.replace(section, "")
                        else:
                            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                            node_text_copy = node_text_copy.replace(f"[{link[0]}]({link[1]})", "")
                    else:
                        continue
        new_nodes_list.append(new_nodes)
    return new_nodes_list
            
def split_nodes_images(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if len(extracted_images) == 0:
            return [node]
        new_nodes = []
        node_text_copy = node.text
        for image in extracted_images:
            sections = node_text_copy.split(f"![{image[0]}]({image[1]})")
            if sections[0] != '' and sections[1] != '':
                for i in range(len(sections)):
                    matches = extract_markdown_images(sections[i])
                    if len(matches) == 0 and i == 0:
                        new_nodes.append(TextNode(sections[i], TextType.TEXT))
                        new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                        node_text_copy = node_text_copy.replace(sections[i] + f"![{image[0]}]({image[1]})", "")
                    elif len(matches) == 0:
                        new_nodes.append(TextNode(sections[i], TextType.TEXT))
                        node_text_copy = node_text_copy.replace(sections[i], "")
                    else:
                        continue
            else:
                if sections[0] == '' and sections[1] == '':
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    node_text_copy = node_text_copy.replace(f"![{image[0]}]({image[1]})", "")
                    continue
                for section in sections:
                    matches = extract_markdown_images(section)
                    if len(matches) == 0:
                        if section != '':
                            new_nodes.append(TextNode(section, TextType.TEXT))
                            node_text_copy = node_text_copy.replace(section, "")
                        else:
                            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                            node_text_copy = node_text_copy.replace(f"![{image[0]}]({image[1]})", "")
                    else:
                        continue
        new_nodes_list.append(new_nodes)
    return new_nodes_list