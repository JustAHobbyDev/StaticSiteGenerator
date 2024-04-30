class HTMLNode:
    def __init__(self, 
                 tag = None, 
                 content = None, 
                 children = [], 
                 props = {}):
        self.tag = tag
        self.content = content
        self.children = children
        self.props = props

        
    def to_html(self):
        raise NotImplementedError
    

    def props_to_html(self):
        if not self.tag:
            return self.content
        
        props_str = ""
        for prop in self.props:
            props_str += " "
            props_str += f"{prop}=\"{self.props[prop]}\""
        return props_str 

    def __repr__(self):
        r = f"<{__class__.__name__}:\ntag: {self.tag}\ncontent: {self.content}\nchildren: {self.children}\nprops: {self.props}\n>"
        return r