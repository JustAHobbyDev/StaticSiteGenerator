import unittest
from block_markdown import block_to_block_type, markdown_to_blocks


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