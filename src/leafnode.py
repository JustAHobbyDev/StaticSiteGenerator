from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, content, props = {}):
        self.tag = tag,
        self.content = content
        self.props = props
        super().__init__(tag, content, None, props)


    def __eq__(self, other):
        """Tests equality of two LeafNodes"""
        s, o = self, other
        return s.tag == o.tag and s.content == o.content and s.props == o.props
        
        
    def __repr__(self):
        return super().__repr__(self)
    
    
    def to_html(self):
        if self.content is None:
            raise ValueError
        if not self.tag:
            return self.content
    
        html = f"<{self.tag}{self.props_to_html()}>{self.content}</{self.tag}>"
        return html