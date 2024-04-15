from textnode import TextNode, TextType
from htmlnode import HtmlNode


def main():
    node = TextNode("This is a text node",
                    TextType.text_type_link, "https://www.boot.dev")
    htmlNode = HtmlNode("h1", "Test H1", [], {
                        "href": "https://www.google.com",
                        "target": "_blank"
                        })


main()
