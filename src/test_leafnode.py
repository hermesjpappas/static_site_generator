import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_returns_props(self):
        node = LeafNode(
            "a", "link text", {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_prints(self):
        node = LeafNode(
            "a", "link text", {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.__repr__(),
            'a: link text - props:  href="https://www.google.com" target="_blank" - children: None',
        )

    def test_gets_values_from_constructor(self):
        node = LeafNode(
            "a",
            "link text",
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual("a", node.tag)
        self.assertEqual("link text", node.value)
        self.assertEqual(
            {"href": "https://www.google.com", "target": "_blank"}, node.props
        )

    def test_returns_valid_HTML(self):
        node = LeafNode(
            "a",
            "link text",
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">link text</a>',
        )

    def test_returns_plain_text(self):
        node = LeafNode(None, "Text here.", None)
        self.assertEqual(node.to_html(), "Text here.")

    def test_raises_exception(self):
      with self.assertRaises(ValueError):
          node = LeafNode("a", None, None)


if __name__ == "__main__":
    unittest.main()
