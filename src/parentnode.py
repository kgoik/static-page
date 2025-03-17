from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("parent node needs tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("parent node needs children")
        
        for child in self.children:
            if child == None:
                raise ValueError("child element cannot be of NoneType")
        
        prop_string = ""

        if self.props is not None:
            for k,v in self.props.items():
                prop_string += f" {k}=\"{v}\""

        s = f"<{self.tag}{prop_string}>"

        for child in self.children:
            s += f"{child.to_html()}"
        
        s += f"</{self.tag}>"

        return s
