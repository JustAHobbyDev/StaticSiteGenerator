import re


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
