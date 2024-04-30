from textnode import TextNode
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    text_types = {
        "text": {"tag": None, "content": text_node.text, "props": {}},
        "bold": {"tag": "b", "content": text_node.text, "props": {}},
        "italic": {"tag": "i", "content": text_node.text, "props": {}},
        "code": {"tag": "code", "content": text_node.text, "props": {}},
        "link": {"tag": "a", "content": text_node.text, "props": {}},
        "image": {
            "tag": "img",
            "content": "",
            "props": {"alt": text_node.text, "src": text_node.url},
        },
    }

    text_type = text_types[text_node.text_type]
    tag = text_type["tag"]
    content = text_type["content"]
    props = text_type["props"]

    leaf_node = LeafNode(tag, content, props)
    return leaf_node


tn = TextNode("Some random text", "italic", "https://boot.dev")

print(tn)

print(text_node_to_html_node(tn))

img_tn = TextNode("A pretty picture", "image", "http://unsplash.com/photos/a-bird-is-standing-on-a-hill-at-sunset-5AiN3pLyJLU")
img = text_node_to_html_node(img_tn)
print(img.to_html())
