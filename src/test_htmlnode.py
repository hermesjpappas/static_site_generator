import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_returns_props(self):
        node = HTMLNode("a", "link text", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_prints(self):
        node = HTMLNode("a", "link text", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), 'a: link text - props:  href="https://www.google.com" target="_blank" - children: None')
    
    def test_inherits_values(self):
        node = HTMLNode("a", "link text", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("a", node.tag)
        self.assertEqual("link text", node.value)
        self.assertEqual({"href": "https://www.google.com", "target": "_blank"}, node.props)


if __name__ == "__main__":
    unittest.main()
