from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        node = LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        node = LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        node = LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        node = LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        node = LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise ValueError("Invalid text node type")
    return node
