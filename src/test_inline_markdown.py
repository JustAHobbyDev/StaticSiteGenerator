import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType

class SplitNodesLinksAndImagesTestCase(unittest.TestCase):
    def test_split_nodes_only_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.text,
        )
        got = split_nodes_link([node])
        want = [
            TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
        ]
        self.assertEqual(want, got)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.text,
        )
        got = split_nodes_link([node])
        self.assertEqual(4, len(got))
        want = [
            TextNode("This is text with a link ", TextType.text),
            TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
            TextNode(" and ", TextType.text),
            TextNode(
                "to youtube", TextType.link, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(want, got)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.text,
        )
        got = split_nodes_image([node])
        want = [
            TextNode("This is text with a link ", TextType.text),
            TextNode("to boot dev", TextType.image, "https://www.boot.dev"),
            TextNode(" and ", TextType.text),
            TextNode(
                "to youtube", TextType.image, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(want, got)


class ExtractMarkdownLinksAndImagesTestCase(unittest.TestCase):
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        got = extract_markdown_links(text)
        want = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(want, got)

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        got = extract_markdown_images(text)
        want = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")] 
        self.assertEqual(want, got)

class SplitNodesDelimiterTestCase(unittest.TestCase):
    def test_single_text_node(self):
        text_node = TextNode("A plain old text type textnode", "text")
        got = split_nodes_delimiter([text_node], "*", "bold")
        want = [text_node]
        self.assertEqual(want, got)

    
    def test_multiple_text_node(self):
        text_nodes = [TextNode("A plain old text type textnode", "text"), TextNode("A plain old text type textnode", "text")]
        got = split_nodes_delimiter(text_nodes, "*", "bold")
        want = text_nodes
        self.assertEqual(want, got)

    
    def test_bold_text_node(self):
        text_node = TextNode("A **bold** text type textnode", "text")
        got = split_nodes_delimiter([text_node], "**", "bold")
        want = [
            TextNode("A ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text type textnode", "text")
        ]
        self.assertEqual(want, got)

    def test_multiple_bold_text_nodes(self):
        text_node = TextNode("**1** 2 3", "text")
        got = split_nodes_delimiter([text_node], "**", "bold")
        want = [
            TextNode("1", "bold"),
            TextNode(" 2 3", "text"),
        ]
        self.assertEqual(want, got)

    def test_multiple_italic_text_nodes(self):
        text_node = TextNode("*1* *2* 3", "text")
        got = split_nodes_delimiter([text_node], "*", "italic")
        want = [
            TextNode("1", "italic"),
            TextNode(" ", "text"),
            TextNode("2", "italic"),
            TextNode(" 3", "text"),
        ]
        self.assertEqual(want, got)

    def test_markdown_error(self):
        text_node = TextNode("here is a *markdown error", "text")
        self.assertRaises(SyntaxError, split_nodes_delimiter, [text_node], "*", "italic")
    
if __name__ == '__main__':
    unittest.main()