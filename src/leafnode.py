from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, content, props = {}):
        self.tag = tag,
        self.content = content
        self.props = props
        super().__init__(tag, content, None, props)

        
    def to_html(self):
        if not self.content:
            raise ValueError
        if not self.tag:
            return self.content
    
        html = f"<{self.tag}{self.props_to_html()}>{self.content}</{self.tag}>"
        return html