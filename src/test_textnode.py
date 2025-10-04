import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode(
            "This is a text node with URL", TextType.LINK, "https://www.boot.dev"
        )
        node2 = TextNode(
            "This is a text node with URL", TextType.LINK, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is also a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text ndoe", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", TextType.IMAGE, "https://www.google.com"
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
