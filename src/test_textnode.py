import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_texttype_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "http://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertEqual(str(node), f"TextNode({node.text}, {node.text_type.value}, {node.url})" )

    def test_repr_empty_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node), f"TextNode({node.text}, {node.text_type.value}, {node.url})" )


if __name__ == "__main__":
    unittest.main()