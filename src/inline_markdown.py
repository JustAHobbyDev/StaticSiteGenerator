from re import findall
from textnode import ( TextNode, TextType )

class MarkdownSearchPattern:
    # images
    images = r"!\[(.*?)\]\((.*?)\)"

    # regular links
    links = r"(?<!!)\[(.*?)\]\((.*?)\)"

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    return nodes

def split_nodes_by(nodes, extract_inject, split_target_inject, text_type_inject):
    new_nodes = []
    for node in nodes:
        if node.text_type is not TextType.text:
            new_nodes.append(node)
            continue

        links = extract_inject(node.text)
        if not links:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        for link in links:
            text, url = link
            parts = node_text.split(split_target_inject(text, url), 1)
            if parts[0]:
                tnode = TextNode(parts[0], TextType.text)
                new_nodes.append(tnode)

            if len(parts) > 1:
                lnode = TextNode(text, text_type_inject, url)
                new_nodes.append(lnode)
            
                node_text = parts[1]
        else:
            if node_text:
                tnode = TextNode(node_text, TextType.text)
                new_nodes.append(tnode)
                

    return new_nodes

def split_nodes_link(nodes):
    return split_nodes_by(nodes, extract_markdown_links, create_markdown_link, TextType.link)

def split_nodes_image(nodes):
    return split_nodes_by(nodes, extract_markdown_images, create_markdown_image, TextType.image)

def create_markdown_link(text, url):
    return f"[{text}]({url})"

def create_markdown_image(text, url):
    return f"![{text}]({url})"
     
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
        
        bullet = ''
        node_text = ''
        node_url = node.url
        if node.text.startswith("* ") or node.text.startswith("- "):
            bullet = node.text[:2]
            node_text = node.text[2:]
        else:
            node_text = node.text

        tokens = node_text.split(delimiter)

        if len(tokens) % 2 == 0:
            msg = f"""
                node_text: {node_text}
                tokens: {tokens}
                length: {len(tokens)}
            """
            raise SyntaxError(msg.strip())

        for i, token in enumerate(tokens):
            if bullet and i == 0:
               token = bullet + token 

            new_node = None
            if (i % 2) == 1:
                new_node = TextNode(token, text_type, node_url)
            else:
                if token:
                    new_node = TextNode(token, TextType.text, node_url)
            if new_node:
                new_nodes.append(new_node)
        
    return new_nodes