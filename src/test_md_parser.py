import unittest

from md_parser import MD_Parser


class TestMD_Parser(unittest.TestCase):
    def test_parse_01(self):
        text = "This is **bold** text."
        md_parser = MD_Parser("**", "bold")
        got = md_parser.parse(text)
        want = [("This is ", "text"), ("bold", "bold"), (" text.", "text")]
        self.assertEqual(want, got)