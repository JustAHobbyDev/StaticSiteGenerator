import unittest

from leafnode import LeafNode
from textnode import TextNode, text_types, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

        
    def test_uneq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)
        
        
    def test_uneq_missing_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "https://example.com")
        self.assertNotEqual(node, node2)

class Test_textnode_to_htmlnode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", "bold")
        got = text_node_to_html_node(node)
        text_type = text_types[node.text_type]
        tag = text_type["tag"]
        content = text_type["content"]
        want = LeafNode(tag, content)
        self.assertEqual(want, got, f"{want == got}")

    def test_image(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        node = TextNode(text, "image")
        got = text_node_to_html_node(node)
        text_type = text_types[node.text_type]
        tag = text_type["tag"]
        content = text_type["content"]
        props = text_type["props"]
        want = LeafNode(tag, content, props)
        self.assertEqual(want, got, f"{want == got}")

if __name__ == "__main__":
    unittest.main()