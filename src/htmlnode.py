class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        s = f"<{self.tag}>"

        if self.value != None:
            s = f"{s}{self.value}"

        for child in self.children:
            s = f"{s}{child.to_html()}"
        
        s = f"{s}</{self.tag}>"
        return s

    
    def props_to_html(self):
        s = ""

        if self.props is not None:
            for k,v in self.props.items():
                s += f" {k}=\"{v}\""

        return s
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
