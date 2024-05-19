import unittest

from inline_markdown import (
    extract_markdown_images,
    parse_links_and_images,
    scan_until_not_text,
    split_nodes_delimiter,
    split_nodes_image,
)
from inline_markdown import extract_markdown_links
from textnode import TextNode


class TestInlineMarkdown(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        print()
        got = extract_markdown_images(text)
        want = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(want, got)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        got = extract_markdown_links(text)
        want = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(want, got)

    def test_split_nodes_delimiter_bad_node(self):
        node = TextNode("This is text with a `code block` word", "text")
        bad_node = TextNode("This is text with a `code block word", "text")
        self.assertRaises(
            SyntaxError, split_nodes_delimiter, [node, bad_node], "`", "code"
        )

    def test_bold(self):
        bold = TextNode("This is a *BOLD* statement!", "text")
        want = [
            TextNode("This is a ", "text"),
            TextNode("BOLD", "bold"),
            TextNode(" statement!", "text"),
        ]
        got = split_nodes_delimiter([bold], "*", "bold")
        self.assertEqual(want, got)

    def test_bold_double(self):
        bold = TextNode("This is a **BOLD** statement!", "text")
        want = [
            TextNode("This is a ", "text"),
            TextNode("BOLD", "bold"),
            TextNode(" statement!", "text"),
        ]
        got = split_nodes_delimiter([bold], "**", "bold")
        self.assertEqual(want, got)

    def test_multi_nodes(self):
        node = TextNode("This is text with a `code block` word", "code")
        bold = TextNode("This is a *BOLD* statement!", "bold")
        want = [
            TextNode("This is text with a `code block` word", "text"),
            TextNode("This is a ", "text"),
            TextNode("BOLD", "bold"),
            TextNode(" statement!", "text"),
        ]
        got = split_nodes_delimiter([node, bold], "*", "bold")
        self.assertEqual(want, got)


class TestSplitImageNodes(unittest.TestCase):
    def test_parse_links_and_images(self):
        text = "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        got = parse_links_and_images(text)
        want = [( "text", "This is text with an " ),
                ( "url", "[image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"),
                ("text", " and another " ),
                ("image", "![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"),
                ]
        self.assertEqual(want, got)

    def test_scan_until_not_text(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        got = scan_until_not_text(text)
        want = ("This is text with an ", 21)
        # want = ("This is text with an ", "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)")
        self.assertEqual(want, got)

    def test_scan_until_not_text_bad_unclosed_square(self):
        text = "This is text with an ![image(https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        got = scan_until_not_text(text)
        want = (
            "This is text with an ![image(https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            -1,
        )
        self.assertEqual(want, got)

    def test_scan_until_not_text_bad_unclosed_round(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        got = scan_until_not_text(text)
        want = (
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            -1,
        )
        self.assertEqual(want, got)

    def test_scan_until_not_text_bad_unopened_round(self):
        text = "This is text with an ![image]https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        got = scan_until_not_text(text)
        want = (
            "This is text with an ![image]https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            -1,
        )
        self.assertEqual(want, got)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "image",
        )

        got = split_nodes_image([node])
        want = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(want, got)

    def test_split_nodes_image_mixed(self):
        node = TextNode(
            "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "url",
        )

        got = split_nodes_image([node])
        want = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "url",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(want, got)
