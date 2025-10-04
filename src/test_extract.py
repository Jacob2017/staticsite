import unittest

from extract import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)

        self.assertEqual(
            result,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_empty_alt_text(self):
        """Test image with empty alt text"""
        text = "Image with no alt: ![](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("", "https://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_no_images_in_text(self):
        """Test text with no images returns empty list"""
        text = "This is just plain text with no images"
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

    def test_images_with_special_characters(self):
        """Test images with special characters in alt text and URL"""
        text = "![Image with spaces & symbols!](https://example.com/path/to/image.png?query=value&size=large)"
        result = extract_markdown_images(text)
        expected = [
            (
                "Image with spaces & symbols!",
                "https://example.com/path/to/image.png?query=value&size=large",
            )
        ]
        self.assertEqual(result, expected)

    def test_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_links_not_images(self):
        """Test that image syntax is not matched as a link"""
        text = "This is ![an image](https://example.com/img.png) and [a link](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("a link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_empty_link_text(self):
        """Test link with empty text"""
        text = "Empty link text: [](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertEqual(result, expected)

    def test_no_links_in_text(self):
        """Test text with no links returns empty list"""
        text = "Plain text with no markdown links"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)
