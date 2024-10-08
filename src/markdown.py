import re
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == 'header':
            header_level = count_header_level(block)
            if header_level == 1:
                return block.strip('# ')

    raise SyntaxError("No title found")

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == 'header':
            text_nodes = text_to_textnodes(block)
            header_text = text_nodes[0].text
            header_level = count_header_level(text_nodes[0].text)
            text_nodes[0].text = header_text[header_level+1:] 
            # TODO: text_nodes_to_html_nodes
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            node = HTMLNode(f"h{header_level}", '', html_nodes)
            nodes.append(node)
        if block_type == 'code':
            content = block[3:-3].strip()
            text_node = TextNode(content, 'code')
            code = text_node_to_html_node(text_node)
            pre = HTMLNode('pre', '', [code])
            nodes.append(pre)
        if block_type == 'quote':
            parts = re.split(r'^[\>] *|\n[\>] *', block)
            print(f'parts: {parts}')
            content = ""
            for part in parts:
                if part:
                    content += part
            text_nodes = text_to_textnodes(content)
            print(f'---\ntext_nodes: {text_nodes}\n---')
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            print(f'---\nhtml_nodes: {html_nodes}\n---')
            # p = HTMLNode("p", '', html_nodes)
            quote = HTMLNode("blockquote", '', html_nodes)
            nodes.append(quote)
        if block_type == 'unordered_list':
            ul_children = []
            items = re.split(r'^[\*\-] *|\n[\*\-] *', block)
            for item in items:
               if item:
                    print(f'item: {item}')
                    li_text_nodes = text_to_textnodes(item)
                    li_children = []
                    for ltn in li_text_nodes:
                        tn = text_node_to_html_node(ltn)
                        li_children.append(tn)
                    li_node = HTMLNode('li', '', li_children)
                    ul_children.append(li_node)
            ul = HTMLNode("ul", '', ul_children)
            nodes.append(ul)
        if block_type == 'ordered_list':
            ol_children = []
            items = re.split(r'\d+\.', block)
            for item in items:
               if item:
                    li_text_nodes = text_to_textnodes(item.strip())
                    li_children = []
                    for ltn in li_text_nodes:
                        tn = text_node_to_html_node(ltn)
                        li_children.append(tn)
                    li_node = HTMLNode('li', '', li_children)
                    ol_children.append(li_node)
            ol = HTMLNode("ol", '', ol_children)
            nodes.append(ol)
        if block and block_type == 'paragraph':
            tns = text_to_textnodes(block)
            p_children = []
            for tn in tns:
                hn = text_node_to_html_node(tn)
                p_children.append(hn)
            p = HTMLNode("p", '', p_children)
            nodes.append(p)
    html = HTMLNode("div", '', nodes)
    return html

def count_header_level(block):
    h_count = 0
    for c in block:
        if c != '#':
            return h_count
        h_count += 1
        if h_count > 6:
            h_count = 6
            break
    return h_count

class BlockPatterns:
    header = r'^#{1,6} +\S+'
    code = r'^(`{3})[^`]+(`{3})$'
    
def block_to_block_type(block):
    if re.match(BlockPatterns.header, block):
        return "header"
    if re.match(BlockPatterns.code, block):
        return "code"

    lines = block.split('\n')
    
    # blockquote
    for line in lines:
        if not line.startswith('>'):
            break
    else:
        return "quote"

    # unordered list
    for line in lines:
        if not (line.startswith('* ') or line.startswith('- ')):
            break
    else:
       return "unordered_list"
 
    # ordered list
    for n, line in enumerate(lines):
        if not line.startswith(f"{n+1}. "):
            break
    else:
        return "ordered_list"

    return "paragraph"


def markdown_to_blocks(markdown):
    blocks = []
    unstripped_blocks = re.split(r'\n\n', markdown)
    for ublock in unstripped_blocks:
        blocks.append(ublock.strip())
    return blocks
