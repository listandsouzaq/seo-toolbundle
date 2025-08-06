"""
Word Frequency Counter Tool

Counts the frequency of each word in the visible text of the page.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content
import re
from collections import Counter

class WordFrequencyCounter(BaseTool):
    def __init__(self):
        super().__init__(
            name="Word Frequency Counter",
            description="Counts the frequency of each word in the page's visible text."
        )

    def run(self, url: str) -> dict:
        """
        Returns a frequency count of words in the page text.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=" ")
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        words = text.split()
        freq = Counter(words)
        common = freq.most_common(20)

        return {
            "total_words": len(words),
            "unique_words": len(freq),
            "top_20_words": common,
            "message": "Word frequency analysis complete."
        }