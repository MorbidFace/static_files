import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq_1(self):
        htmlNode = HtmlNode("h1", "Test H1", [], {
                        "href": "https://www.google.com", 
                        "target": "_blank",
                        "style": "width:100%"
                        })
        self.assertEqual(htmlNode.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\" style=\"width:100%\"")

    def test_eq_2(self):
        htmlNode = HtmlNode("h1", "Test H1", [], {
                        "href": "https://www.google.com", 
                        "target": "_blank"
                        })
        self.assertEqual(htmlNode.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_eq_3(self):
        htmlNode = HtmlNode("h1", "Test H1", [], {
                        "href": "https://www.google.com", 
                        })
        self.assertEqual(htmlNode.props_to_html(), " href=\"https://www.google.com\"")

    def test_eq_4(self):
        htmlNode = HtmlNode("h1", "Test H1", [])
        self.assertEqual(htmlNode.props_to_html(), "")

    def test_leaf_1(self):
        leafNode = LeafNode(None, "test")
        self.assertEqual(leafNode.to_html(), "test")

    def test_leaf_2(self):
        leafNode = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leafNode.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_3(self):
        leafNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leafNode.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        
    def test_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()
