from parentnode import ParentNode
from leafnode import LeafNode

import unittest

class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child2</span></div>")

    def test_to_html_with_children_with_props(self):
        child_node = LeafNode("span", "child", {"class": "testCssClass"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span class=\"testCssClass\">child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )  

    def test_child_of_type_none(self):
        child_node = None
        parent_node = ParentNode("div", [child_node])
        with self.assertRaisesRegex(ValueError, "child element cannot be of NoneType"):
            parent_node.to_html()

    def test_none_child(self):
        child_node = None
        parent_node = ParentNode("div", child_node)
        with self.assertRaisesRegex(ValueError, "parent node needs children"):
            parent_node.to_html()

    def test_empty_child(self):
        parent_node = ParentNode("div", [])
        with self.assertRaisesRegex(ValueError, "parent node needs children"):
            parent_node.to_html()

    def test_none_tag(self):
        child_node = LeafNode("span", value="test")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, "parent node needs tag"):
            parent_node.to_html()

    def test_empty_tag(self):
        child_node = LeafNode("span", value="test")
        parent_node = ParentNode("", [child_node])
        with self.assertRaisesRegex(ValueError, "parent node needs tag"):
            parent_node.to_html()


