from typing import List, Dict, Optional


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[List[HTMLNode]] = children
        self.props: Optional[Dict[str, str]] = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        output_lst = []
        if self.tag:
            output_lst.append(f"tag: {self.tag}")
        if self.value:
            output_lst.append(f"value: {self.value}")
        if self.children:
            children_list = []
            for ch in self.children:
                children_list.append(repr(ch))
            output_lst.append(f"children: {children_list}")
        if self.props:
            output_lst.append(f"props: {self.props_to_html()}")
        return " | ".join(output_lst)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.props:
            open_tag = f"<{self.tag} {self.props_to_html()}>"
        else:
            open_tag = f"<{self.tag}>"

        close_tag = f"</{self.tag}>"
        return f"{open_tag}{self.value}{close_tag}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes not have missing children")

        if self.props:
            open_tag = f"<{self.tag} {self.props_to_html()}>"
        else:
            open_tag = f"<{self.tag}>"
        close_tag = f"</{self.tag}>"
        children_html = [ch.to_html() for ch in self.children]
        return f"{open_tag}{''.join(children_html)}{close_tag}"
