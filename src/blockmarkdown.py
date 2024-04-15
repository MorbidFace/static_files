from enum import Enum
from htmlnode import ParentNode, LeafNode
from inlinemarkdown import text_to_textnodes
from textnode import text_node_to_html_node
import re


class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if (len(re.findall(r"^#{1,6}(?!#)( .+)", block)) > 0):
        return BlockTypes.HEADING
    elif (block.startswith("```") and block.endswith("```")):
        return BlockTypes.CODE
    elif block.startswith(">"):
        quote_lines = list(filter(lambda x: x.startswith(">"), lines))
        if len(quote_lines) == len(lines):
            return BlockTypes.QUOTE
    elif block.startswith("* "):
        bullet_lines = list(filter(lambda x: x.startswith("* "), lines))
        if len(bullet_lines) == len(lines):
            return BlockTypes.UNORDERED_LIST
    elif block.startswith("- "):
        bullet_lines = list(filter(lambda x: x.startswith("- "), lines))
        if len(bullet_lines) == len(lines):
            return BlockTypes.UNORDERED_LIST
    elif block.startswith("1. "):
        is_ol = True  # Assume it's an ordered list initially
        index = 1
        for line in lines:
            line_split = line.split(". ")
            if len(line_split) > 0:
                try:
                    if int(line_split[0]) == index:
                        index += 1  # Move to the next expected index
                    else:
                        is_ol = False  # Not an ordered list
                        break
                except ValueError:
                    is_ol = False  # Not an ordered list
                    break
        if is_ol:
            return BlockTypes.ORDERED_LIST
    return BlockTypes.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockTypes.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockTypes.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockTypes.CODE:
        return code_to_html_node(block)
    if block_type == BlockTypes.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockTypes.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockTypes.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

## MINE
# def heading_block_to_html(block):
#     children = []
#     for line in block:
#         count = 0
#         for char in line:
#             if char == '#':
#                 count += 1
#             else:
#                 break  
#         value = line.lstrip("# ")
#         children.append(LeafNode(f"h{count}", value))
#     parent = ParentNode("div", children)
#     return parent

# def unordered_block_to_html(block):
#     ul_children = []
#     for line in block:
#         value = ""
#         if (line.startswith("* ")):
#             value = line.lstrip("* ")
#         elif (line.startswith("- ")):
#             value = line.lstrip("- ")
#         ul_children.append(LeafNode("li", value))
#     ul_parent = ParentNode("ul", ul_children)
#     parent = ParentNode("div", [ul_parent])
#     return parent

# def ordered_block_to_html(block):
#     ol_children = []
#     for line in block:
#         line_split = line.split(". ")
#         ol_children.append(LeafNode("li", line_split[1]))
#     ul_parent = ParentNode("ol", ol_children)
#     parent = ParentNode("div", [ul_parent])
#     return parent

# def code_block_to_html(block):
#     code_children = []
#     for i in range(1, len(block)-1):
#         code_children.append(LeafNode("code", block[i]))
#     code_parent = ParentNode("pre", code_children)
#     parent = ParentNode("div", [code_parent])
#     return parent

# def quote_block_to_html(block):
#     quote_children = []
#     for line in block:
#         value = line.lstrip("> ")
#         quote_children.append(LeafNode("p", value))
#     code_parent = ParentNode("quoteblock", quote_children)
#     parent = ParentNode("div", [code_parent])
#     return parent

# def paragraph_block_to_html(block):
#     children = []
#     for line in block:
#         children.append(LeafNode("p", line))
#     parent = ParentNode("div", children)
#     return parent

# def block_to_block_type(block)
    # lines = block.split("\n")

    # if (
    #     block.startswith("# ")
    #     or block.startswith("## ")
    #     or block.startswith("### ")
    #     or block.startswith("#### ")
    #     or block.startswith("##### ")
    #     or block.startswith("###### ")
    # ):
    #     return block_type_heading
    # if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
    #     return block_type_code
    # if block.startswith(">"):
    #     for line in lines:
    #         if not line.startswith(">"):
    #             return block_type_paragraph
    #     return block_type_quote
    # if block.startswith("* "):
    #     for line in lines:
    #         if not line.startswith("* "):
    #             return block_type_paragraph
    #     return block_type_ulist
    # if block.startswith("- "):
    #     for line in lines:
    #         if not line.startswith("- "):
    #             return block_type_paragraph
    #     return block_type_ulist
    # if block.startswith("1. "):
    #     i = 1
    #     for line in lines:
    #         if not line.startswith(f"{i}. "):
    #             return block_type_paragraph
    #         i += 1
    #     return block_type_olist
    # return block_type_paragraph