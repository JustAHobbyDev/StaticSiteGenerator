class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_textnode):
        """Tests equality of two TextNodes"""
        s, o = self, other_textnode
        return s.text == o.text and s.text_type == o.text_type and s.url == o.url

    def __repr__(self):
        """String representation of a TextNode instance"""
        r = f"{self.__class__.__name__}({self.text}, {self.text_type}, {self.url})"
        return r
    
