from re import findall
from textnode import ( TextNode, TextType )

class MarkdownSearchPattern:
    # images
    images = r"!\[(.*?)\]\((.*?)\)"

    # regular links
    links = r"(?<!!)\[(.*?)\]\((.*?)\)"

def extract_markdown_images(text):
    return findall(MarkdownSearchPattern.images, text)

def extract_markdown_links(text):
    return findall(MarkdownSearchPattern.links, text)

def split_nodes_delimiter(nodes, delimiter, text_type):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.text:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        node_url = node.url
        tokens = node_text.split(delimiter)

        if len(tokens) % 2 == 0:
            raise SyntaxError("Invalid markdown syntax")

        for i, token in enumerate(tokens):
            new_node = None
            if (i % 2) == 1:
                new_node = TextNode(token, text_type, node_url)
            else:
                if token:
                    new_node = TextNode(token, TextType.text, node_url)
            if new_node:
                new_nodes.append(new_node)
        
    return new_nodes