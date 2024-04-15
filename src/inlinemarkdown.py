import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if (len(sections) % 2 == 0):
            raise ValueError("Invalid, markdown item not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            elif i % 2 == 0:
                split_nodes.append(
                    TextNode(sections[i], TextType.text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    image_matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return image_matches


def extract_markdown_links(text):
    link_matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return link_matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if node.text_type != TextType.text_type_text:
            new_nodes.append(node)
            continue
        elif (len(extracted_images) <= 0):
            new_nodes.append(node)
            continue
        split_nodes = []
        working_text = node.text
        index = 0
        for image in extracted_images:
            split_text = working_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_text[0] != "":
                split_nodes.append(
                    TextNode(split_text[0], TextType.text_type_text))
            split_nodes.append(TextNode(image[0], TextType.text_type_image, image[1]))
            if (index < len(extracted_images)):
                working_text = split_text[index+1]
        if working_text != "":
            split_nodes.append(TextNode(working_text, TextType.text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if node.text_type != TextType.text_type_text:
            new_nodes.append(node)
            continue
        elif (len(extracted_links) <= 0):
            new_nodes.append(node)
            continue
        split_nodes = []
        working_text = node.text
        index = 0
        for link in extracted_links:
            split_text = working_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split_text[0] != "":
                split_nodes.append(TextNode(split_text[0], TextType.text_type_text))
            split_nodes.append(TextNode(link[0], TextType.text_type_link, link[1]))
            if (index < len(extracted_links)):
                working_text = split_text[index+1]
        if working_text != "":
            split_nodes.append(TextNode(working_text, TextType.text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", TextType.text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", TextType.text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes