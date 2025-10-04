from typing import List
from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_lst = node.text.split(delimiter)
            new_type = False
            for sub_node_text in split_lst:
                new_node = TextNode(
                    text=sub_node_text,
                    text_type=text_type if new_type else TextType.TEXT,
                )
                new_nodes.append(new_node)
                new_type = not new_type
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            img_matches = extract_markdown_images(node.text)
            current_text = node.text
            while len(img_matches) > 0:
                alt, src = img_matches.pop(0)
                img_match = f"![{alt}]({src})"
                prefix, current_text = current_text.split(img_match, maxsplit=1)
                new_node = TextNode(
                    text=prefix,
                    text_type=TextType.TEXT,
                )
                if len(new_node.text) > 0:
                    new_nodes.append(new_node)
                img_node = TextNode(text=alt, text_type=TextType.IMAGE, url=src)
                new_nodes.append(img_node)
            if len(current_text) > 0:
                new_node = TextNode(text=current_text, text_type=TextType.TEXT)
                new_nodes.append(new_node)
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            link_matches = extract_markdown_links(node.text)
            current_text = node.text
            while len(link_matches) > 0:
                anchor, url = link_matches.pop(0)
                link_match = f"[{anchor}]({url})"
                prefix, current_text = current_text.split(link_match, maxsplit=1)
                # prefix = current_text.split(link_match, maxsplit=1)[0]
                new_node = TextNode(
                    text=prefix,
                    text_type=TextType.TEXT,
                )
                if len(new_node.text) > 0:
                    new_nodes.append(new_node)
                link_node = TextNode(text=anchor, text_type=TextType.LINK, url=url)
                new_nodes.append(link_node)
            if len(current_text) > 0:
                new_node = TextNode(text=current_text, text_type=TextType.TEXT)
                new_nodes.append(new_node)
        else:
            new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
