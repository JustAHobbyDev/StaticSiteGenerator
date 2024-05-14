from inline_markdown import split_nodes_delimiter
from textnode import TextNode


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)


main()