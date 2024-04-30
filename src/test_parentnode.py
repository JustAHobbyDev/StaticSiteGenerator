import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_flat_tree(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(html, node.to_html())

    
    def test_branched_tree(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
            ],
        )

        html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>"
        self.assertEqual(html, node.to_html())


if __name__ == "__main__":
    unittest.main()
