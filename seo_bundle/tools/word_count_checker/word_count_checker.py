"""
Word Count Checker Tool

This tool counts the total number of words on a given web page.
It fetches the HTML content, extracts visible text, and returns the word count.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content, get_text_from_html

class WordCountChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Word Count Checker",
            description="Counts the total number of words on the web page."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, extract visible text, and count the number of words.
        Returns a dict with the total word count and a message.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        text = get_text_from_html(soup)
        words = text.split()
        count = len(words)

        return {
            "word_count": count,
            "message": f"The page contains {count} words."
        }