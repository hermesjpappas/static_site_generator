import unittest
from leafnode import LeafNode
from textnode import TextNode
from utils import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
)


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

    # tests for split_nodes_delimiter function
    def test_returns_split_code_nodes(self):
        node = TextNode("This is a text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(
            [
                TextNode("This is a text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )

    def test_returns_split_bold_nodes(self):
        node = TextNode("This is a text with a **bold block** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(
            [
                TextNode("This is a text with a ", "text"),
                TextNode("bold block", "bold"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )

    def test_returns_split_italic_nodes(self):
        node = TextNode("This is a text with an *italic block* word", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(
            [
                TextNode("This is a text with an ", "text"),
                TextNode("italic block", "italic"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )

    def test_handles_more_than_one_inner_block(self):
        node = TextNode("This is a text with **two** bold **words**", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(
            [
                TextNode("This is a text with ", "text"),
                TextNode("two", "bold"),
                TextNode(" bold ", "text"),
                TextNode("words", "bold"),
            ],
            new_nodes,
        )

    def test_raises_exception_more_than_two_delimiters(self):
        node = TextNode(
            "This is a text with *italic block* unmatched * delimiters", "italic"
        )
        split_nodes_delimiter([node], "*", "italic")
        self.assertRaises(Exception)

    def test_raises_exception_less_than_two_delimiters(self):
        node = TextNode(
            "This is a text with *italic block unmatched delimiters", "italic"
        )
        split_nodes_delimiter([node], "*", "italic")
        self.assertRaises(Exception)

    # test extract_markdown_images
    def test_returns_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(
            result,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_returns_empty_array_for_no_images(self):
        text = "This is some text with no images. ![] blah ()"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    # test extract_markdown_links
    def test_returns_list_of_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) blah"
        result = extract_markdown_links(text)
        self.assertEqual(
            result,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_does_not_extract_images(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev/blah.png) and [to youtube](https://www.youtube.com/@bootdotdev) blah"
        result = extract_markdown_links(text)
        self.assertEqual(
            result, [("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    # test split_nodes_image
    def test_img_split_works_with_images(self):
        node = TextNode(
            "This is text with an image link ![to boot dev](https://www.boot.dev/image.png) and ![to youtube](https://www.youtube.com/@bootdotdev/something.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image link ", "text"),
                TextNode("to boot dev", "image", "https://www.boot.dev/image.png"),
                TextNode(" and ", "text"),
                TextNode(
                    "to youtube",
                    "image",
                    "https://www.youtube.com/@bootdotdev/something.png",
                ),
            ],
        )

    def test_img_split_works_with_no_image_links(self):
        node = TextNode("This is text with no links.", "text")
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("This is text with no links.", "text")])

    def test_img_split_doesnt_add_empty_text_nodes(self):
        node = TextNode("", "text")
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [])

    # test split_nodes_link

    def test_link_split_works_with_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            "text",
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", "text"),
                TextNode("to boot dev", "link", "https://www.boot.dev"),
                TextNode(" and ", "text"),
                TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_link_works_with_no_links(self):
        node = TextNode("This is text with no links.", "text")
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This is text with no links.", "text")])

    def test_link_split_doesnt_add_empty_text_nodes(self):
        node = TextNode("", "text")
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])

    # test text_to_textnodes
    def test_txt_to_nodes_works_with_everything(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ],
        )

    def test_txt_to_nodes_works_with_only_text(self):
        text = "This is just plain text."
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [TextNode("This is just plain text.", "text")])

    # test markdown to blocks
    def test_mkd_to_blk_splits_strings(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_mkd_to_blk_splits_strings_and_strips(self):
        text = """# This is a heading        

   This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
* This is a list item
* This is another list item     """
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_mkd_to_blk_one_block(self):
        text = "       This is only one line."
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, ["This is only one line."])

    # test block to block type
    def test_block_to_block_recognizes_heading(self):
        heading1 = "# I am a heading"
        self.assertEqual(block_to_block_type(heading1), "heading")
        heading2 = "## I am a heading"
        self.assertEqual(block_to_block_type(heading2), "heading")
        heading3 = "### I am a heading"
        self.assertEqual(block_to_block_type(heading3), "heading")
        heading4 = "#### I am a heading"
        self.assertEqual(block_to_block_type(heading4), "heading")
        heading5 = "##### I am a heading"
        self.assertEqual(block_to_block_type(heading5), "heading")
        heading6 = "###### I am a heading"
        self.assertEqual(block_to_block_type(heading6), "heading")

    def test_block_to_block_recognizes_code(self):
        code = "```something```"
        self.assertEqual(block_to_block_type(code), "code")
        code2 = """```
          code here
          ```"""
        self.assertEqual(block_to_block_type(code2), "code")
    

    def test_block_to_block_recognizes_quote(self):
        quote = ">Hello this is a quote."
        self.assertEqual(block_to_block_type(quote), "quote")
        quote2 = """>Hello this is a 
        >multiline quote.
        >blah"""
        self.assertEqual(block_to_block_type(quote2), "quote")
    
    def test_block_to_block_recognizes_unordered_list(self):
        ul = "* Something"
        self.assertEqual(block_to_block_type(ul), "unordered_list")
        ul2 = "- Something"
        self.assertEqual(block_to_block_type(ul2), "unordered_list")
        ul3 = """* Something
        * Something else
        """
        self.assertEqual(block_to_block_type(ul3), "unordered_list")
        ul4 = """- Something
        - Something else
        """
        self.assertEqual(block_to_block_type(ul4), "unordered_list")
    
    def test_block_to_block_recognizes_ordered_list(self):
        ol = """1. Something
        2. Something else"""
        self.assertEqual(block_to_block_type(ol), "ordered_list")
        ol2 = "1. Something"
        self.assertEqual(block_to_block_type(ol2), "ordered_list")

    def test_block_to_block_rejects_bad_examples(self):
        heading = "#nospace"
        self.assertEqual(block_to_block_type(heading), "paragraph") 
        code = "``code bad code `"
        self.assertEqual(block_to_block_type(code), "paragraph") 
        quote = """>Bad quote starts
        but does not continue"""
        self.assertEqual(block_to_block_type(quote), "paragraph")
        ul = """* Something here
        not here
        * something here again"""
        self.assertEqual(block_to_block_type(ul), "paragraph")
        ol = """1. Something here
        2. Something here as well
        but not here
        4. And then here"""
        self.assertEqual(block_to_block_type(ol), "paragraph")
        ol2 = """1. Something here
        3. Suddenly three!"""
        self.assertEqual(block_to_block_type(ol2), "paragraph")