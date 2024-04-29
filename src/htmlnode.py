from __future__ import annotations
from typing import Mapping, List, ForwardRef


class HTMLNode:
    def __init__(self, 
                 tag: str = "", 
                 content: str = "", 
                 children: List[HTMLNode] = [], 
                 props: Mapping[str, str] = {}) -> None:
        self.tag = tag
        self.content = content
        self.children = children
        self.props = props

        
    def to_html(self) -> str:
        html = f"<{self.tag}{self.props_to_html()}>{self.content}</{self.tag}>"
        return html
    

    def props_to_html(self) -> str:
        props_str = ""
        for prop in self.props:
            props_str += " "
            props_str += f"{prop}=\"{self.props[prop]}\""
        return props_str 

    def __repr__(self) -> str:
        r = f"<{__class__.__name__}:\ntag: {self.tag}\ncontent: {self.content}\nchildren: {self.children}\nprops: {self.props}\n>"
        return r