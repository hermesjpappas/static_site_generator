import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq_no_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("Hello", "bold", "http://google.com")
        node2 = TextNode("Hello", "bold", "http://google.com")
        self.assertEqual(node, node2)
    
    def test_uneq_text(self):
        node = TextNode("This is one text node", "bold")
        node2 = TextNode("This is another text node", "bold")
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode("Hello", "bold", "http://hjp.gr")
        node2 = TextNode("Hello", "bold", "http://google.com")
        self.assertNotEqual(node, node2)

    def test_uneq_url_none(self):
        node = TextNode("Hello", "bold", "http://hjp.gr")
        node2 = TextNode("Hello", "bold")

    def test_uneq_text_type(self):
        node = TextNode("Hello", "italic", "http://hjp.gr")
        node2 = TextNode("Hello", "bold", "http://hjp.gr")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()