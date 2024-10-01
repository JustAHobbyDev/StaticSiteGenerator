import re
from markdown import extract_title, block_to_block_type, markdown_to_blocks, markdown_to_html_node
from htmlnode import HTMLNode
from textnode import TextNode
from inline_markdown import text_to_textnodes

md = "## The Art of **World-Building**"
blocks = markdown_to_blocks(md)

html_nodes = HTMLNode('h1', '', [
    TextNode('text', ' The Art of '),
    TextNode('bold', 'World-Building'),
])

got = markdown_to_html_node(md)

print(f'\ngot: {got}\n')

textnodes = text_to_textnodes(md)
print(f'\n{textnodes}')

htmlnodes = markdown_to_html_node(md)
print(f'htmlnodes:\n{htmlnodes}')



ul_md = """
- **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
- **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
- **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.
"""
blocks_1 = markdown_to_blocks(ul_md)
print(blocks_1)
b = blocks_1[0]

items = re.split(r'^[\*\-] *|\n[\*\-] *', b)
print(items)
print(text_to_textnodes(items[1]))