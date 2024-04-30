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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_nodes = []
    for node in old_nodes:
        if node.__class__.__name__ == "TextNode":
            future_textnodes = []
            delimited = False
            i, j = 0, 0
            while j < len(node.text):
                character = node.text[j]
                # print(character)
                if character is delimiter:
                    content = node.text[i:j]
                    future_textnodes.append({"content": content, "delimited": delimited})
                    delimited = not delimited
                    i = j + 1
                    j = i + 1
                else:
                    if j < len(node.text):
                        j += 1
            else:
                # delimited should be False after iterating through the text
                if delimited:
                    raise SyntaxError("Invalid Markdown: Unclosed delimiter found.") 
                print(node.text[i:j])
                content = node.text[i:j]
                future_textnodes.append({"content": content, "delimited": delimited})

                for future_textnode in future_textnodes:
                    if not future_textnode["delimited"]:
                        future_textnode_type = "text"
                    else:
                        future_textnode_type = text_type
                    final_nodes.append(TextNode(future_textnode["content"], future_textnode_type, node.url))

        else:
            final_nodes.append(node)

    return final_nodes


# tn = TextNode("Some random text", "italic", "https://boot.dev")

# print(tn)

# print(text_node_to_html_node(tn))

# img_tn = TextNode("A pretty picture", "image", "http://unsplash.com/photos/a-bird-is-standing-on-a-hill-at-sunset-5AiN3pLyJLU")
# img = text_node_to_html_node(img_tn)
# print(img.to_html())

node = TextNode("This is text with a `code block` word", "text")
print(f"type of node: {type(node)}")
new_nodes = split_nodes_delimiter([node], "`", "code")
print(new_nodes)


bad_node = TextNode("This is text with a `code block word", "text")
try:
    new_nodes = split_nodes_delimiter([node, bad_node], "`", "code")
except Exception as e:
    print(f"Error: {e}")