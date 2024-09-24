import unittest
from htmlnode import HTMLNode


class HTMLNodeTestCase(unittest.TestCase):
    def test_to_html_00(self):
        h = HTMLNode('div', '')
        html = "<div></div>"
        want = html
        got = h.to_html()
        self.assertEqual(want, got)

    def test_to_html_01(self):
        h = HTMLNode(
            'div',
            '',
            [
                HTMLNode('p', 'First paragraph', [], {"id": 2}),
                HTMLNode('p', 'Second paragraph', [], {"id": 3})
            ],
            {"id": 1, "class": "root"}
        )
        html = '<div id="1" class="root"><p id="2">First paragraph</p><p id="3">Second paragraph</p></div>'
        want = html
        got = h.to_html()
        self.assertEqual(want, got)