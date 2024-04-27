from __future__ import annotations
from typing import Mapping, List, ForwardRef


class HTMLNode:
    def __init__(self, tag: str, content: str, children: List[HTMLNode], props: Mapping[str, str]) -> None:
        self.tag = tag
        self.content = content
        self.children = children
        self.props = props

        
    def to_html(self):
        raise NotImplemented
    

    def props_to_html(self):
        raise NotImplemented
    

    def __repr__(self):
        raise NotImplemented