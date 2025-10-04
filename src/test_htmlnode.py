import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr_basic(self):
        node = HTMLNode(tag="p", value="This is a paragraph")
        expected_value = "tag: p | value: This is a paragraph"
        self.assertEqual(repr(node), expected_value)

    def test_repr_children(self):
        child1 = HTMLNode(tag="p", value="Child p 1")
        child2 = HTMLNode(tag="p", value="Child p 2")
        node = HTMLNode("div", children=[child1, child2])
        expected_value = "tag: div | children: ['tag: p | value: Child p 1', 'tag: p | value: Child p 2']"
        self.assertEqual(repr(node), expected_value)

    def test_repr_props(self):
        node = HTMLNode(
            tag="a", value="google", props={"href": "www.google.com", "prop": "p2"}
        )
        expected_value = (
            'tag: a | value: google | props: href="www.google.com" prop="p2"'
        )
        self.assertEqual(repr(node), expected_value)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "google", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">google</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_children_props(self):
        child_node = LeafNode("a", "child", {"href": "www.google.com"})
        child2_node = LeafNode("p", "child 2", {"size": "10"})
        parent_node = ParentNode("div", [child_node, child2_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="www.google.com">child</a><p size="10">child 2</p></div>',
        )
