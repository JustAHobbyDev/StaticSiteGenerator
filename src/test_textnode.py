# type: ignore
import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

        
    def test_uneq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.italic)
        self.assertNotEqual(node, node2)
        
        
    def test_uneq_missing_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "https://example.com")
        self.assertNotEqual(node, node2)


class testTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type(self):
        text_node = TextNode("Some text content", TextType.text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.content, "Some text content")


    def test_text_bold(self):
        text_node = TextNode("Some text content", TextType.bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.content, "Some text content")


    def test_text_italic(self):
        text_node = TextNode("Some text content", TextType.italic)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.content, "Some text content")


    def test_text_code(self):
        text_node = TextNode("Some text content", TextType.code)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.content, "Some text content")


    def test_text_link(self):
        text_node = TextNode("Some text content", TextType.link, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.content, "Some text content")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})


    def test_text_image(self):
        text_node = TextNode("Some text content", TextType.image, "https://boot.dev/logo.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.content, "")
        self.assertEqual(html_node.props, {"alt": "Some text content", "src": "https://boot.dev/logo.jpg"})

    # TODO: More unit tests!!!
    # def test_mixed(self):
    #     tn = [
    #         TextNode("I like Tolkien", TextType.bold),
    #         TextNode(". Read my ", TextType.text),
    #         TextNode("first post here", TextType.link, "/majesty"),
    #         TextNode(" (sorry the link doesn't work yet)", TextType.text),
    #     ]

if __name__ == "__main__":
    unittest.main()