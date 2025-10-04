import unittest

from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_bold_single_delimiter(self):
        """Test splitting a single TEXT node with bold delimiter"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_code_multiple_delimiters(self):
        """Test splitting with multiple code delimiters in one node"""
        node = TextNode("Use `print()` and `input()` functions", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("input()", TextType.CODE),
            TextNode(" functions", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_nodes_passed_through(self):
        """Test that non-TEXT nodes are not split and are passed through unchanged"""
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("*italic text*", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter_in_text(self):
        """Test node without delimiter returns unchanged"""
        node = TextNode("Plain text with no special formatting", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("Plain text with no special formatting", TextType.TEXT)]
        self.assertEqual(result, expected)


class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![and another second image](https://i.imgur.com/3elNhQu.png) and [a link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "and another second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" and [a link](https://www.google.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This is text with no image", TextType.TEXT),
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and nothing else.",
                TextType.TEXT,
            ),
            TextNode(
                "This is text with a ![second image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)",
                TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing else.", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and a [link](https://www.google.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_empty_node(self):
        nodes = [
            TextNode("", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([], new_nodes)


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This is text with no image", TextType.TEXT),
            TextNode(
                "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and nothing else.",
                TextType.TEXT,
            ),
            TextNode(
                "This is text with a [second image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)",
                TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing else.", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_images_then_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_empty_node(self):
        nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual([], new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_basic(self):
        input_str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input_str)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
