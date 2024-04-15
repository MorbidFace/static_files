import unittest
from blockmarkdown import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
