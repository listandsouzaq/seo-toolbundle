"""
Text-to-Keyword Generator Tool

Extracts the most frequent keywords from the given text (expects text in the URL parameter).
"""

from tools.base_tool import BaseTool
import re
from collections import Counter

class TextToKeywordGenerator(BaseTool):
    def __init__(self):
        super().__init__(
            name="Text-to-Keyword Generator",
            description="Extracts most frequent keywords from the given text (pass text in URL parameter)."
        )

    def run(self, url: str) -> dict:
        """
        Expects text in the 'url' parameter.
        Returns the most frequent keywords.
        """
        text = url
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        words = text.split()
        # Remove common stopwords
        stopwords = set([
            "the", "and", "a", "an", "of", "to", "for", "in", "on", "at", "with", "is", "it", "by", "this", "that",
            "as", "are", "was", "were", "be", "or", "from", "but", "not", "can", "has", "have", "had"
        ])
        keywords = [w for w in words if w not in stopwords]
        freq = Counter(keywords)
        common = freq.most_common(15)
        return {
            "top_keywords": common,
            "message": "Keyword extraction complete."
        }