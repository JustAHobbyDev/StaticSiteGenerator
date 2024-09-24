from dataclasses import dataclass


@dataclass
class HTMLNode:
    def __init__(self, 
                 tag = None, 
                 content = None, 
                 children = [], 
                 props = {}):
        self.tag = tag
        self.content = content
        self.children = children
        self.props = props

        
    def to_html(self):
        props_html = ''
        if self.props:
            for prop in self.props:
                props_html += f' {prop}="{self.props[prop]}"'

        children_html = ''
        if self.children:
            for child in self.children:
                children_html += child.to_html()

        html_preformat = '<{tag}{props_html}>{content}{children_html}</{tag}>'
        return html_preformat.format_map({
            'tag': self.tag,
            'props_html': props_html,
            'children_html': children_html,
            'content': self.content,
        })

    def props_to_html(self):
        if not self.tag:
            return self.content
        
        props_str = ""
        for prop in self.props:
            props_str += " "
            props_str += f"{prop}=\"{self.props[prop]}\""
        return props_str 

    def __repr__(self, _self=None):
        self = _self or self
        r = f"<{self.__class__.__name__}:\ntag: {self.tag}\ncontent: {self.content}\nchildren: {self.children}\nprops: {self.props}\n>"
        return r

        