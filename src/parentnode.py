from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag, None, children, props)

        
    def to_html(self):
        if not self.tag:
            raise ValueError(f"{__class__.__name__} must have a HTML tag.")
        if not self.children:
            raise ValueError("ParentNode must have children nodes.")
        children_html = ""
        for child in self.children:
            children_html += f"{child.to_html()}"
        html = f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        return html
    
    