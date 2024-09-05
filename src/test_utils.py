import unittest
from leafnode import LeafNode
from textnode import TextNode
from utils import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    # tests for text_node_to_html_node function
    def test_raises_value_error_for_no_text(self):
        with self.assertRaisesRegex(ValueError, "No text provided in text node"):
            text_node = TextNode(None, "text")
            text_node_to_html_node(text_node)

    def test_returns_text_leaf_node(self):
        text_node = TextNode("sample text here", "text")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "sample text here")

    def test_returns_bold_leaf_node(self):
        text_node = TextNode("sample text here", "bold")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<b>sample text here</b>")

    def test_returns_italic_leaf_node(self):
        text_node = TextNode("sample text here", "italic")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<i>sample text here</i>")

    def test_returns_code_leaf_node(self):
        text_node = TextNode("sample text here", "code")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.to_html(), "<code>sample text here</code>")

    def test_returns_link_leaf_node(self):
        text_node = TextNode("sample text here", "link", "http://hjp.gr")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(
            leaf_node.to_html(), '<a href="http://hjp.gr">sample text here</a>'
        )

    def test_returns_img_leaf_node(self):
        text_node = TextNode("sample text here", "image", "http://hjp.gr/image.png")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(
            leaf_node.to_html(),
            '<img src="http://hjp.gr/image.png" alt="sample text here"></img>',
        )

    def test_raises_exception_link_no_url(self):
        with self.assertRaisesRegex(ValueError, "No URL given for link text node"):
            text_node = TextNode("sample text here", "link", None)
            text_node_to_html_node(text_node)

    def test_raises_exception_img_no_url(self):
        with self.assertRaisesRegex(ValueError, "No URL given for image text node"):
            text_node = TextNode("sample text here", "image", None)
            text_node_to_html_node(text_node)

    def test_raises_exception_wrong_text_type(self):
        with self.assertRaisesRegex(Exception, "Invalid text node type"):
          text_node = TextNode("sample text here", "random_type")
          text_node_to_html_node(text_node)

    def test_raises_exception_no_text_type(self):
        with self.assertRaisesRegex(Exception, "Invalid text node type"):
          text_node = TextNode("sample text here", None)
          text_node_to_html_node(text_node)