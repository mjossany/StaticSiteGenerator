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
        list_key_value = self.props.items()
        final_string = reduce(lambda accumulator, current_tuple: accumulator + f' {current_tuple[0]}="{current_tuple[1]}"', list_key_value, "")
        print(f'FINAL STRING: {final_string}')
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
        if value is None:
            raise ValueError("LeafNode requires a non-None value.")
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a non-None value.")
        if self.tag is None:
            return self.value
        

