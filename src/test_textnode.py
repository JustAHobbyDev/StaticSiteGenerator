# type: ignore
import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

        
    def test_uneq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_italic)
        self.assertNotEqual(node, node2)
        
        
    def test_uneq_missing_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "https://example.com")
        self.assertNotEqual(node, node2)


class testTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type(self):
        text_node = TextNode("Some text content", text_type_text)
        html_node = text_node_to_html_node(text_node)
<<<<<<< HEAD
        self.assertEqual(html_node.tag, None)
=======
        self.assertEqual(html_node.tag, None)type: ignore
>>>>>>> 5d82327 (Ch.2: Nodes - 6: TextNode to HTMLNode)
        self.assertEqual(html_node.content, "Some text content")


    def test_text_bold(self):
        text_node = TextNode("Some text content", text_type_bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.content, "Some text content")


    def test_text_italic(self):
        text_node = TextNode("Some text content", text_type_italic)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.content, "Some text content")


    def test_text_code(self):
        text_node = TextNode("Some text content", text_type_code)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.content, "Some text content")


    def test_text_link(self):
        text_node = TextNode("Some text content", text_type_link, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.content, "Some text content")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})


    def test_text_image(self):
        text_node = TextNode("Some text content", text_type_image, "https://boot.dev/logo.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.content, "")
        self.assertEqual(html_node.props, {"alt": "Some text content", "src": "https://boot.dev/logo.jpg"})


if __name__ == "__main__":
    unittest.main()