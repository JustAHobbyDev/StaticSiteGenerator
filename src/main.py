import re
from textnode import TextNode

# TODO: Move into own file
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_nodes = []
    delimiter_jump = len(delimiter)
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
                    i = j + delimiter_jump
                    j = i + delimiter_jump
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


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
print(extract_markdown_images(text))
# [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

def extract_markdown_links(text):
    matches = re.findall(r"(?:[^!])\[(.*?)\]\((.*?)\)", text)
    return matches

# TODO: Move into own test file    
text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
print(extract_markdown_links(text))
# [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]

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



bold = TextNode("This is a **BOLD** statement!", "text")
try:
    new_nodes = split_nodes_delimiter([node, bold], "**", "bold")
    print(new_nodes)
except Exception as e:
    print(f"Error: {e}")