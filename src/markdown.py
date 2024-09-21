import re
from htmlnode import HTMLNode


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == 'header':
            header_level = count_header_level(block)
            node = HTMLNode(f"h{header_level}", block[header_level+1:])
            nodes.append(node)
        if block_type == 'code':
            content = block.strip('```')
            code = HTMLNode('code', content)
            pre = HTMLNode('pre', '', [code])
            nodes.append(pre)
        if block_type == 'quote':
            parts = re.split(r'^>|\n>', block)
            content = ""
            for part in parts:
                if part:
                    content += part
            p = HTMLNode("p", block)
            quote = HTMLNode("quote", "", [p])
            nodes.append(quote)
        if block_type == 'unordered_list':
            ul_children = []
            items = block.split('*')
            for item in items:
               if item:
                   li = HTMLNode("li", item.strip())
                   ul_children.append(li) 
            ul = HTMLNode("ul", '', ul_children)
            nodes.append(ul)
        # TODO ordered_list
        if block_type == 'ordered_list':
            ol_children = []
            items = re.split(r'\d+\.', block)
            for item in items:
               if item:
                   li = HTMLNode("li", item.strip())
                   ol_children.append(li) 
            ol = HTMLNode("ol", '', ol_children)
            nodes.append(ol)
        if block and block_type == 'paragraph':
            p = HTMLNode("p", block)
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
