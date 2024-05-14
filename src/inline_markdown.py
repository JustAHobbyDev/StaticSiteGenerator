import re
from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_nodes = []
    delimiter_jump = len(delimiter)
    for node in old_nodes:
        if node.__class__.__name__ == "TextNode":
            future_textnodes = []
            delimited = False
            i, j = 0, 0
            while j < len(node.text):
                character = node.text[j:j+len(delimiter)]
                # print(character)
                if character == delimiter:
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


def extract_markdown_links(text):
    matches = re.findall(r"(?:[^!])\[(.*?)\]\((.*?)\)", text)
    return matches
