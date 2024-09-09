from leafnode import LeafNode
from textnode import TextNode
import re


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


# NOTE: Current implementations rely on the string not beginning with
# a delimiter or with an image/link. Could be improved further


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], "text"))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return_list = []
    matches = re.findall(r"!\[.+?\]\(.+?\)", text)
    for image in matches:
        alt_text = re.findall(r"\!\[(.*?)\]", image)[0]
        image_link = re.findall(r"\((.*?)\)", image)[0]
        return_list.append((alt_text, image_link))

    return return_list


def extract_markdown_links(text):
    return_list = []
    matches = re.findall(r"(?<!!)\[.+?\]\(.+?\)", text)
    for mlink in matches:
        link_text = re.findall(r"\[(.*?)\]", mlink)[0]
        link = re.findall(r"\((.*?)\)", mlink)[0]
        return_list.append((link_text, link))

    return return_list


def split_nodes_image(old_nodes):
    new_nodes = []
    image_regex = r"(!\[.+?\]\(.+?\))"
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        if old_node.text == "":
            continue
        matches = re.findall(image_regex, old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(image_regex, old_node.text)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], "text"))
            else:
                image_list = extract_markdown_images(sections[i])
                split_nodes.append(
                    TextNode(image_list[0][0], "image", image_list[0][1])
                )
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    link_regex = r"((?<!!)\[.+?\]\(.+?\))"
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        if old_node.text == "":
            continue
        matches = re.findall(link_regex, old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(link_regex, old_node.text)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], "text"))
            else:
                image_list = extract_markdown_links(sections[i])
                split_nodes.append(TextNode(image_list[0][0], "link", image_list[0][1]))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    old_nodes = [TextNode(text, "text")]

    bold_nodes = split_nodes_delimiter(old_nodes, "**", "bold")
    italic_nodes = split_nodes_delimiter(bold_nodes, "*", "italic")
    code_nodes = split_nodes_delimiter(italic_nodes, "`", "code")
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)

    return link_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    return blocks
