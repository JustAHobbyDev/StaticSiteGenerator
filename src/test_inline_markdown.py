import unittest

from inline_markdown import extract_markdown_images, split_nodes_delimiter
from inline_markdown import extract_markdown_links
from textnode import TextNode


class TestInlineMarkdown(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        print()
        got = extract_markdown_images(text)
        want = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(want, got)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        got = extract_markdown_links(text)
        want = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(want, got)


    def test_split_nodes_delimiter_bad_node(self):
        node = TextNode("This is text with a `code block` word", "text")
        bad_node = TextNode("This is text with a `code block word", "text")
        self.assertRaises(SyntaxError, split_nodes_delimiter, [node, bad_node], "`", "code")

    def test_bold(self):
        bold = TextNode("This is a *BOLD* statement!", "text")
        want = [TextNode("This is a ", "text"), TextNode("BOLD", "bold"), TextNode(" statement!", "text")]
        got = split_nodes_delimiter([bold], '*', "bold")
        self.assertEqual(want, got)


    def test_bold_double(self):
        bold = TextNode("This is a **BOLD** statement!", "text")
        want = [TextNode("This is a ", "text"), TextNode("BOLD", "bold"), TextNode(" statement!", "text")]
        got = split_nodes_delimiter([bold], '**', "bold")
        self.assertEqual(want, got)

    def test_multi_nodes(self):
        node = TextNode("This is text with a `code block` word", "code")
        bold = TextNode("This is a *BOLD* statement!", "bold")
        want = [TextNode("This is text with a `code block` word", "text"), TextNode("This is a ", "text"), TextNode("BOLD", "bold"), TextNode(" statement!", "text")]
        got = split_nodes_delimiter([node, bold], "*", "bold")
        self.assertEqual(want, got)