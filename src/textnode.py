from leafnode import LeafNode


class TextType:
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_textnode):
        """Tests equality of two TextNodes"""
        s, o = self, other_textnode
        return s.text == o.text and s.text_type == o.text_type and s.url == o.url

    def __repr__(self):
        """String representation of a TextNode instance"""
        r = f"{self.__class__.__name__}({self.text}, {self.text_type}, {self.url})"
        return r
    

def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    content = text_node.text
    url = text_node.url
    
    if TextType.text == text_type:
        return LeafNode(None, content)
    if TextType.bold == text_type:
        return LeafNode("b", content)
    if TextType.italic == text_type:
        return LeafNode("i", content)
    if TextType.code == text_type:
        return LeafNode("code", content)
    if TextType.link == text_type:
        return LeafNode("a", content, { "href": url })
    if TextType.image == text_type:
        return LeafNode("img", "", {"src": url, "alt": content})