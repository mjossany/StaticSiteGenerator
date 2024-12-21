from textnode import TextType, TextNode

class Delimiter():
    def __init__(self):
        return
    
    def split_nodes_delimiter(self, nodes, delimiter, text_type):
        nodes_splited_list = []
        for node in nodes:
            node_list = []
            if node.text_type != TextType.TEXT:
                node_list.append(node)
                nodes_splited_list.extend(node_list)
                continue
            delimiter_count = node.text.count(delimiter)
            if delimiter_count != 2:
                raise Exception("Invalid markdown syntax. Matching closing delimiter is missing.")
            node_value_splitted_list = node.text.split(delimiter)
            node_list.append(TextNode(node_value_splitted_list[0], TextType.TEXT))
            node_list.append(TextNode(node_value_splitted_list[1], text_type))
            node_list.append(TextNode(node_value_splitted_list[2], TextType.TEXT))
            nodes_splited_list.extend(node_list)
        return nodes_splited_list