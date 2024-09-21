import unittest
from markdown import block_to_block_type, markdown_to_blocks, markdown_to_html_node
from htmlnode import HTMLNode


class MarkdownToHTMLTestCase(unittest.TestCase):
    def test_markdown_to_html_node_body(self):
        markdown = ""
        html = markdown_to_html_node(markdown)
        want = HTMLNode("div", markdown)
        got = html
        self.assertDictEqual(want.__dict__, got.__dict__)

    def test_markdown_to_html_node_h(self):
        for n in range(1, 7):
            markdown = '#' * n
            h = f"h{n}"
            markdown += f" {h} header"
            h_node = HTMLNode(h, markdown[n:])
            want = HTMLNode("div", '', [h_node])
            got = markdown_to_html_node(markdown)
            self.assertDictEqual(want.__dict__, got.__dict__)

    def test_markdown_to_html_node_code(self):
        markdown = "```\nmsg = \"Hello, World!\"\n```"
        code_node = HTMLNode("code", markdown)
        pre_node = HTMLNode("pre", "", [code_node])
        html = HTMLNode("div", '', [pre_node])
        want = html
        got = markdown_to_html_node(markdown)
        self.assertDictEqual(want.__dict__, got.__dict__)

    def test_markdown_to_html_node_ul(self):
        markdown = "* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        ul_children = [
            HTMLNode("li", "This is the first list item in a list block"),
            HTMLNode("li", "This is a list item"),
            HTMLNode("li", "This is another list item"),
        ]
        ul = HTMLNode("ul", "", ul_children)
        want = HTMLNode("div", "", [ul]).__dict__
        got = markdown_to_html_node(markdown).__dict__
        self.assertEqual(want, got)

    def test_markdown_to_html_node_ol(self):
        markdown = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item\n"
        ol_children = [
            HTMLNode("li", "This is the first list item in a list block"),
            HTMLNode("li", "This is a list item"),
            HTMLNode("li", "This is another list item"),
        ]
        ol = HTMLNode("ol", "", ol_children)
        want = HTMLNode("div", "", [ol]).__dict__
        got = markdown_to_html_node(markdown).__dict__
        self.assertEqual(want, got)

class BlockMarkdownTestCase(unittest.TestCase):
    def setUp(self):
        self.blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        
    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        want = self.blocks
        got = markdown_to_blocks(markdown)
        self.assertEqual(want, got)

    def test_block_to_block_type_header(self):
        header = '# h1'
        want = 'header'
        got = block_to_block_type(header)
        self.assertEqual(want, got)
        self.assertEqual('paragraph', block_to_block_type('#h1'))
        self.assertEqual('paragraph', block_to_block_type('####### h1'))
        self.assertEqual('header', block_to_block_type('###### h1'))

    def test_block_to_block_type_code(self):
        code = '```\nsome code\nsome more code\nend of code\n```'
        want = 'code'
        got = block_to_block_type(code)
        self.assertEqual(want, got)

    def test_block_to_block_type_quote(self):
        quote = '>some code\n>some more code\n>end of code'
        want = 'quote'
        got = block_to_block_type(quote)
        self.assertEqual(want, got)

    def test_block_to_block_type_unordered(self):
        unordered_star = '* item\n* another item\n* last thing'
        want = 'unordered_list'
        got = block_to_block_type(unordered_star)
        self.assertEqual(want, got)
        unordered_dash = '- item\n- another item\n- last thing'
        want = 'unordered_list'
        got = block_to_block_type(unordered_dash)
        self.assertEqual(want, got)


        
if __name__ == "__main__":
    unittest.main()