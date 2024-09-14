from leafnode import LeafNode


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

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
    
    if text_type_text == text_type:
        return LeafNode(None, content)
    if text_type_bold == text_type:
        return LeafNode("b", content)
    if text_type_italic == text_type:
        return LeafNode("i", content)
    if text_type_code == text_type:
        return LeafNode("code", content)
    if text_type_link == text_type:
        return LeafNode("a", content, { "href": url })
    if text_type_image == text_type:
        return LeafNode("img", "", {"src": url, "alt": content})