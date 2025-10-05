from typing import List
import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from block_split import markdown_to_blocks
from block import block_to_block_type, BlockType
from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node
from split_nodes import text_to_textnodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        new_nodes = []
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            code_text = block[3:-3].lstrip()
            text_node = TextNode(code_text, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            new_nodes = [ParentNode("pre", children=[html_node])]
        else:
            new_nodes = text_to_children(block)
        children.extend(new_nodes)
    return ParentNode("div", children=children)


def text_to_children(text: str) -> List[HTMLNode]:
    block_type = block_to_block_type(text)
    if block_type == BlockType.HEADING:
        # pattern = r"^(#{1, 6})\s+(.+)"
        # hashes, heading = re.findall(pattern, text)[0]
        text_split = text.split(" ", maxsplit=1)
        hashes, heading = text_split[0], text_split[1]
        tag = f"h{len(hashes)}"
        return [LeafNode(tag, heading)]
    elif block_type == BlockType.QUOTE:
        clean_quote = text.replace(">", "").strip()
        return [LeafNode("blockquote", clean_quote)]
    elif block_type == BlockType.ULIST:
        list_items = []
        for li in text.split("\n"):
            list_items.append(create_list_item(li, "- "))
        return [ParentNode("ul", children=list_items)]
    elif block_type == BlockType.OLIST:
        list_items = []
        for idx, li in enumerate(text.split("\n"), 1):
            list_items.append(create_list_item(li, f"{idx}. "))
        return [ParentNode("ol", children=list_items)]
    elif block_type == BlockType.PARA:
        text = text.replace("\n", " ")
        text_nodes = text_to_textnodes(text)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        return [ParentNode("p", children=html_nodes)]
        # return [text_node_to_html_node(node) for node in text_nodes]
    return []


def create_list_item(raw_line: str, delimiter: str) -> HTMLNode:
    item_text = raw_line.split(delimiter, maxsplit=1)[-1]
    item_nodes = text_to_textnodes(item_text)
    item_html_nodes = [text_node_to_html_node(node) for node in item_nodes]
    return ParentNode("li", children=item_html_nodes)
