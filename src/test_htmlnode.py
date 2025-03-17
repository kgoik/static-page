import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        tag = "a"
        value = "value"
        children = None
        props = {"href": "http://boot.dev"}

        node = HTMLNode(tag, value, children, props)
        text = f"HTMLNode({tag}, {value}, {children}, {props})"
        self.assertEqual(str(node), text)

    def test_empty_children_eq(self):
        tag = "a"
        value = "value"
        props = {"href": "http://boot.dev"}

        node = HTMLNode(tag, value, props=props)
        text = f"HTMLNode({tag}, {value}, None, {props})"
        self.assertEqual(str(node), text)

    def test_empty_children_not_eq(self):
        tag = "a"
        value = "value"
        props = {"href": "http://boot.dev"}

        node = HTMLNode(tag, value, props=props)
        text = f"HTMLNode({tag}, {value}, children , {props})"
        self.assertNotEqual(node, text)



# if __name__ == "__main__":
#     unittest.main()