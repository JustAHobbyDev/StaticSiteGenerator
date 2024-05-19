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
                character = node.text[j : j + len(delimiter)]
                # print(character)
                if character == delimiter:
                    content = node.text[i:j]
                    future_textnodes.append(
                        {"content": content, "delimited": delimited}
                    )
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
                    final_nodes.append(
                        TextNode(
                            future_textnode["content"], future_textnode_type, node.url
                        )
                    )

        else:
            final_nodes.append(node)

    return final_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?:[^!])\[(.*?)\]\((.*?)\)", text)
    return matches


def scan_until_not_text(t):
    i, j, k = 0, 0, 0
    open_square, open_round = False, False
    parsing_text = True
    while j < len(t):
        if t[j] == "[":
            if not parsing_text:
                break
            parsing_text = False
            open_square = True
            if j - 1 > 0 and t[j - 1] == "!":
                k = j - 1
            else:
                k = j
        if not parsing_text:
            if open_square:
                if t[j] == "]" and t[j + 1] == "(":
                    open_square = False
                    open_round = True
            if open_round and not open_square:
                if t[j] == ")":
                    open_square = False
                    return t[i:k], k
        j += 1
    return t, -1

def parse_links_and_images(t):
    chunks = []
    i, j, k = 0, 0, 0
    open_square, open_round = False, False
    parsing_text = True
    is_image = False
    while j < len(t):
        if t[j] == "[":
            if not parsing_text:
                break
            parsing_text = False
            open_square = True
            if j - 1 > 0 and t[j - 1] == "!":
                is_image = True
                k = j - 1
            else:
                k = j
        if not parsing_text:
            if open_square:
                if t[j] == "]" and t[j + 1] == "(":
                    open_square = False
                    open_round = True
            if open_round and not open_square:
                if t[j] == ")":
                    open_round = False
                    parsing_text = True
                    text_type = "image" if is_image else "url"
                    text_chunk = ("text", t[i:k])
                    image_or_url_chunk = (text_type, t[k:j+1])
                    chunks.append(text_chunk)
                    chunks.append(image_or_url_chunk)
                    t = t[j+1:]
                    i = 0
                    j = 0
        j += 1
    if len(t) > 0:
        chunks.append(("text", t))
    return chunks

def split_nodes_image(text_nodes):
    final_split_nodes = []
    for text_node in text_nodes:
        text = text_node.text
        parsed_nodes = parse_links_and_images(text)
        for parsed_node in parsed_nodes:
            text_type, text = parsed_node
            if text_type == "image":
                alt = text[2:text.find("]")]
                url = text[text.find("](")+2:-1]
                tn = TextNode(alt, text_type, url)
                final_split_nodes.append(tn)
            if text_type == "url":
                a = text[1:text.find("]")]
                url = text[text.find("](")+2:-1]
                tn = TextNode(a, text_type, url)
                final_split_nodes.append(tn)
            if text_type == "text":
                tn = TextNode(text, text_type)
                final_split_nodes.append(tn)
    return final_split_nodes