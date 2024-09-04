import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_returns_props(self):
        node = ParentNode(
            "a", None, {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_returns_valid_HTML(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_returns_valid_HTML_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "someClass"},
        )

        self.assertEqual(
            node.to_html(), '<p class="someClass"><b>Bold text</b>Normal text</p>'
        )

    def test_returns_valid_HTML_with_children_parents(self):
        node = ParentNode(
            "p", [
                ParentNode("span", [LeafNode(None, "Inner span text")]),
                LeafNode(None, "Outer text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            '<p><span>Inner span text</span>Outer text</p>'
        )

    def test_raises_exception_for_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(
                None, [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")], None
            ).to_html()

    def test_raises_exception_for_no_children(self):
        with self.assertRaisesRegex(ValueError, "No children given"):
            ParentNode("a", None, None).to_html()


if __name__ == "__main__":
    unittest.main()
