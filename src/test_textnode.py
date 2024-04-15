import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.text_type_bold, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.text_type_bold, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.text_type_bold, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.text_type_bold, "https://boot.dev")
        self.assertEqual(node, node2)
   
    def test_not_eq(self):
        node = TextNode("This is a text noe", TextType.text_type_code, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.text_type_code, "https://boot.dev")
        self.assertNotEqual(node, node2)

    # def test_text_to_text(self):
    #     node = TextNode("This is a text node", None, None)
    #     leaf = node.text_node_to_html_node(node)
    #     self.assertEqual(leaf.tag, None)
    #     self.assertEqual(leaf.value, "This is a text node")
    #     self.assertEqual(leaf.children, None)
    #     self.assertEqual(leaf.props, None)
        

    # def test_text_to_bold(self):


    # def test_text_to_italic(self):


    # def test_text_to_code(self):


    # def test_text_to_link(self):


    # def test_text_to_image(self):

if __name__ == "__main__":
    unittest.main()
