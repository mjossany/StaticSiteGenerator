from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        list_key_value = self.props.items()
        final_string = reduce(lambda accumulator, current_tuple: accumulator + f' {current_tuple[0]}="{current_tuple[1]}"', list_key_value, "")
        return final_string
    

    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
        
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a non-None value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
        
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.children}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a non-None tag") 
        if self.children is None:
            raise ValueError("ParentNode requires at least one child")
        nested_html = ""
        for node in self.children:
            nested_html += node.to_html()
        return f'<{self.tag}{self.props_to_html()}>{nested_html}</{self.tag}>'

    def __repr__(self):
        return f'ParentNode({self.tag}, {self.value}, {self.children}, {self.props})'