from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("leaf node needs a value")
        if self.tag == None:
            return self.value
        
        s = ""
        
        if self.props is not None:
            for k,v in self.props.items():
                s += f" {k}=\"{v}\""
        
        return f"<{self.tag}{s}>{self.value}</{self.tag}>"