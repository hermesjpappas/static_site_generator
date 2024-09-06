from leafnode import LeafNode
from textnode import TextNode


def text_node_to_html_node(text_node):
    if text_node.text == None:
        raise ValueError("No text provided in text node")

    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    elif text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    elif text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    elif text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    elif text_node.text_type == "link":
        if text_node.url == None:
            raise ValueError("No URL given for link text node")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == "image":
        if text_node.url == None:
            raise ValueError("No URL given for image text node")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Invalid text node type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != "text":
            new_list.append(node)
        else:
            if node.text.count(delimiter) != 2:
                raise Exception("More or less than two delimiters given")
            else:
                text_list = node.text.split(delimiter)
                new_list.append(TextNode(text_list[0], "text"))
                new_list.append(TextNode(text_list[1], text_type))
                new_list.append(TextNode(text_list[2], "text"))
    return new_list
