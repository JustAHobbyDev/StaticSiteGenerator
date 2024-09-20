import re

def markdown_to_blocks(markdown):
    blocks = []
    unstripped_blocks = re.split(r'\n\n', markdown)
    for ublock in unstripped_blocks:
        blocks.append(ublock.strip())
    return blocks
