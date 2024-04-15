import unittest
from blockmarkdown import markdown_to_blocks, block_to_block_type, BlockTypes, markdown_to_html_node
from htmlnode import ParentNode, LeafNode


class TestBlockMarkdown(unittest.TestCase):
    def test_block_split(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"
        blocks = markdown_to_blocks(text)
        self.assertListEqual(
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '* This is a list item\n* This is another list item'
            ],
            blocks
        )

    def test_block_split_two(self):
        text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        blocks = markdown_to_blocks(text)
        self.assertListEqual(
            [
                'This is **bolded** paragraph',
                'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
                '* This is a list\n* with items'
            ],
            blocks
        )

    def test_heading_block(self):
        test = "# This is a heading\n## Thest"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockTypes.HEADING)

    def test_code_block(self):
        test = "```This is a heading\nThest```"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockTypes.CODE)

    def test_quote_block(self):
        test = ">test\n>test"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockTypes.QUOTE)

    def test_unordered_block_one(self):
        test = "* test\n* test"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockTypes.UNORDERED_LIST)

    def test_unordered_block_two(self):
        test = "- test\n- test"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockTypes.UNORDERED_LIST)

    def test_ordered_block(self):
        test = "1. test\n2. test"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockTypes.ORDERED_LIST)

    def test_paragraph_block(self):
        test = "1. test\n test"
        block_type = block_to_block_type(test)
        self.assertEqual(block_type, BlockTypes.PARAGRAPH)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockTypes.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockTypes.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockTypes.QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockTypes.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockTypes.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockTypes.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    # def test_heading_block_html(self):
    #     test_block = ["# Test", "### Test"]
    #     parent = heading_to_html_node(test_block)
    #     node = ParentNode(
    #         "div",
    #         [
    #             LeafNode("h1", "Test"),
    #             LeafNode("h3", "Test"),
    #         ],
    #     )
    #     self.assertEqual(parent.tag, node.tag)
    #     self.assertEqual(parent.children[0].tag, node.children[0].tag)
    #     self.assertEqual(parent.children[0].value, node.children[0].value)
    #     self.assertEqual(parent.children[1].tag, node.children[1].tag)
    #     self.assertEqual(parent.children[1].value, node.children[1].value)

    # def test_ul_block_html_one(self):
    #     test_block = ["* Test", "* Test"]
    #     parent = ulist_to_html_node(test_block)
    #     node = ParentNode(
    #         "div",
    #         [
    #             ParentNode("ul", [
    #                 LeafNode("li", "Test"),
    #                 LeafNode("li", "Test"),
    #             ])
    #         ],
    #     )
    #     self.assertEqual(parent.tag, node.tag)
    #     self.assertEqual(parent.children[0].tag, node.children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].tag, node.children[0].children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].value, node.children[0].children[0].value)
    #     self.assertEqual(
    #         parent.children[0].children[1].tag, node.children[0].children[1].tag)
    #     self.assertEqual(
    #         parent.children[0].children[1].value, node.children[0].children[1].value)

    # def test_ul_block_html_two(self):
    #     test_block = ["- Test", "- Test"]
    #     parent = ulist_to_html_node(test_block)
    #     node = ParentNode(
    #         "div",
    #         [
    #             ParentNode("ul", [
    #                 LeafNode("li", "Test"),
    #                 LeafNode("li", "Test"),
    #             ])
    #         ],
    #     )
    #     self.assertEqual(parent.tag, node.tag)
    #     self.assertEqual(parent.children[0].tag, node.children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].tag, node.children[0].children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].value, node.children[0].children[0].value)
    #     self.assertEqual(
    #         parent.children[0].children[1].tag, node.children[0].children[1].tag)
    #     self.assertEqual(
    #         parent.children[0].children[1].value, node.children[0].children[1].value)

    # def test_ol_block_html_two(self):
    #     test_block = ["1. Test", "2. Test"]
    #     parent = olist_to_html_node(test_block)
    #     node = ParentNode(
    #         "div",
    #         [
    #             ParentNode("ol", [
    #                 LeafNode("li", "Test"),
    #                 LeafNode("li", "Test"),
    #             ])
    #         ],
    #     )
    #     self.assertEqual(parent.tag, node.tag)
    #     self.assertEqual(parent.children[0].tag, node.children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].tag, node.children[0].children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].value, node.children[0].children[0].value)
    #     self.assertEqual(
    #         parent.children[0].children[1].tag, node.children[0].children[1].tag)
    #     self.assertEqual(
    #         parent.children[0].children[1].value, node.children[0].children[1].value)

    # def test_code_block_html(self):
    #     test_block = ["```", "def test():", "   print('test')", "```"]
    #     parent = code_to_html_node(test_block)
    #     node = ParentNode(
    #         "div",
    #         [
    #             ParentNode("pre", [
    #                 LeafNode("code", "def test():"),
    #                 LeafNode("code", "   print('test')"),
    #             ])
    #         ],
    #     )
    #     self.assertEqual(parent.tag, node.tag)
    #     self.assertEqual(parent.children[0].tag, node.children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].tag, node.children[0].children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].value, node.children[0].children[0].value)
    #     self.assertEqual(
    #         parent.children[0].children[1].tag, node.children[0].children[1].tag)
    #     self.assertEqual(
    #         parent.children[0].children[1].value, node.children[0].children[1].value)

    # def test_quote_block_html(self):
    #     test_block = ["> Test", "> Test"]
    #     parent = quote_to_html_node(test_block)
    #     node = ParentNode(
    #         "div",
    #         [
    #             ParentNode("quoteblock", [
    #                 LeafNode("p", "Test"),
    #                 LeafNode("p", "Test"),
    #             ])
    #         ],
    #     )
    #     self.assertEqual(parent.tag, node.tag)
    #     self.assertEqual(parent.children[0].tag, node.children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].tag, node.children[0].children[0].tag)
    #     self.assertEqual(
    #         parent.children[0].children[0].value, node.children[0].children[0].value)
    #     self.assertEqual(
    #         parent.children[0].children[1].tag, node.children[0].children[1].tag)
    #     self.assertEqual(
    #         parent.children[0].children[1].value, node.children[0].children[1].value)

    # def test_paragraph_block_html(self):
    #     test_block = ["Test", "Test"]
    #     parent = paragraph_to_html_node(test_block)
    #     node = ParentNode(
    #         "div",
    #         [
    #             LeafNode("p", "Test"),
    #             LeafNode("p", "Test"),
    #         ],
    #     )
    #     self.assertEqual(parent.tag, node.tag)
    #     self.assertEqual(parent.children[0].tag, node.children[0].tag)
    #     self.assertEqual(parent.children[0].value, node.children[0].value)
    #     self.assertEqual(parent.children[1].tag, node.children[1].tag)
    #     self.assertEqual(parent.children[1].value, node.children[1].value)


if __name__ == "__main__":
    unittest.main()
