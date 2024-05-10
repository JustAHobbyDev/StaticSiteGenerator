from leafnode import LeafNode


text_types = {
    "text": {"tag": None, "content": "", "props": {}},
    "bold": {"tag": "b", "content": "", "props": {}},
    "italic": {"tag": "i", "content": "", "props": {}},
    "code": {"tag": "code", "content": "", "props": {}},
    "link": {"tag": "a", "content": "", "props": {}},
    "image": {
        "tag": "img",
        "content": "",
        "props": {"alt": "", "src": ""},
    },
}

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
    text_type = text_types[text_node.text_type]
    text_type["content"] = text_node.text
    tag = text_type["tag"]
    content = text_type["content"]
    props = text_type["props"]

    leaf_node = LeafNode(tag, content, props)
    return leaf_node
