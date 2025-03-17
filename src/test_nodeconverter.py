from node_converter import *
from textnode import TextNode, TextType
from leafnode import LeafNode
import unittest

class NodeConverter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "http://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "http://boot.dev"})
    
    def test_img(self):
        node = TextNode("This is 1st image", TextType.IMAGE, "http://boot.dev/1.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://boot.dev/1.jpg", "alt": "This is 1st image"})

    def test_split_node_text(self):
        text_node1 = TextNode("This is text with a ", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node1], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [text_node1])

    def test_split_node_bold(self):
        text_node1 = TextNode("This is **text** with a bold", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node1], "**", TextType.BOLD)

        expected_text_node1 = TextNode("This is ", TextType.NORMAL)
        expected_bold_node1 = TextNode("text", TextType.BOLD)
        expected_text_node2 = TextNode(" with a bold", TextType.NORMAL)

        self.assertEqual(new_nodes, [expected_text_node1, expected_bold_node1, expected_text_node2])

    def test_split_node_bold_2(self):
        text_node1 = TextNode("This is **text** with a bold and **bold** test", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node1], "**", TextType.BOLD)

        expected_text_node1 = TextNode("This is ", TextType.NORMAL)
        expected_bold_node1 = TextNode("text", TextType.BOLD)
        expected_text_node2 = TextNode(" with a bold and ", TextType.NORMAL)
        expected_bold_node2 = TextNode("bold", TextType.BOLD)
        expected_text_node3 = TextNode(" test", TextType.NORMAL)

        self.assertEqual(new_nodes, [expected_text_node1, expected_bold_node1, expected_text_node2, expected_bold_node2, expected_text_node3])

    def test_split_node_bold_starts_with(self):
        text_node1 = TextNode("**text** with a bold", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node1], "**", TextType.BOLD)

        expected_bold_node1 = TextNode("text", TextType.BOLD)
        expected_text_node1 = TextNode(" with a bold", TextType.NORMAL)

        self.assertEqual(new_nodes, [expected_bold_node1, expected_text_node1])

    def test_split_node_bold_ends_with(self):
        text_node1 = TextNode("This is text with a **bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node1], "**", TextType.BOLD)

        expected_text_node1 = TextNode("This is text with a ", TextType.NORMAL)
        expected_bold_node1 = TextNode("bold", TextType.BOLD)

        self.assertEqual(new_nodes, [expected_text_node1, expected_bold_node1])

    def test_delimiter_not_closed(self):
        text_node1 = TextNode("This is **text with a bold", TextType.NORMAL)

        with self.assertRaisesRegex(Exception, "delimiter closing not found"):
            split_nodes_delimiter([text_node1], "**", TextType.BOLD)

    def test_delimiter_not_closed_2(self):
        text_node1 = TextNode("This is **text** **with a bold", TextType.NORMAL)

        with self.assertRaisesRegex(Exception, "delimiter closing not found"):
            split_nodes_delimiter([text_node1], "**", TextType.BOLD)

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode(
            "This is text without an image",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/) and another [second link](https://boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode(
            "This is text without a link",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without a link", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_split_links_start_with(self):
        node = TextNode(
            "[link](https://i.imgur.com/) and another [second link](https://boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_end_with_text(self):
        node = TextNode(
            "[link](https://i.imgur.com/) and another [second link](https://boot.dev) extra text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://boot.dev"
                ),
                TextNode(" extra text", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_split_links_only(self):
        node = TextNode(
            "[link](https://i.imgur.com/)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/")
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], new_nodes
        )
