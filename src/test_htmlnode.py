import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), f" href=\"https://www.google.com\"")

    def test_props_to_html_multiple_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertTrue(' href="https://www.google.com"' in node.props_to_html())
        self.assertTrue(' target="_blank"' in node.props_to_html())

    def test_empty_leaf(self):
        node = LeafNode("","")
        self.assertRaises(ValueError)

    def test_leaf_no_tag(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Google!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Google!</a>")

    def test_parent_to_html_one_child(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b></p>")

    def test_parent_to_html_multiple_children(self):
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

    def test_parent_to_html_child_with_props(self):
        node = ParentNode(
            "div",
            [
                LeafNode("a", "Google", {"href": "https://www.google.com", "target": "_blank"})
            ]
        )
        self.assertEqual(node.to_html(), "<div><a href=\"https://www.google.com\" target=\"_blank\">Google</a></div>")

    def test_parent_to_html_child_with_child(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "span",
                    [
                        LeafNode("a", "Google", {
                            "href": "https://www.google.com", 
                            "target": "_blank"
                            }
                        ),
                    ]
                )
            ]
        )
        self.assertEqual(node.to_html(), "<div><span><a href=\"https://www.google.com\" target=\"_blank\">Google</a></span></div>")

    def test_parent_to_html_child_with_multiple_children(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "span",
                    [
                        LeafNode("a", "Google", {
                            "href": "https://www.google.com", 
                            "target": "_blank"
                            }
                        ),
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                            ]
                        )
                    ]
                )
            ]
        )
        self.assertEqual(node.to_html(), "<div><span><a href=\"https://www.google.com\" target=\"_blank\">Google</a><p><b>Bold text</b>Normal text</p></span></div>")


if __name__ == "__main__":
    unittest.main()