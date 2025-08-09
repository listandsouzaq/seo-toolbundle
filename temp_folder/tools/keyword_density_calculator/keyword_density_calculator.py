"""
Keyword Density Calculator Tool

This tool calculates the density of each word (or a user-supplied keyword)
on a given web page. It fetches the HTML content, extracts visible text,
tokenizes, and computes word frequencies and density percentages.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content, get_text_from_html
import re
from collections import Counter

class KeywordDensityCalculator(BaseTool):
    def __init__(self):
        super().__init__(
            name="Keyword Density Calculator",
            description="Calculates the frequency and density of words (or a keyword) on a page."
        )

    def run(self, url: str, keyword: str = None) -> dict:
        """
        Analyze the page for keyword density.

        Args:
            url (str): The URL of the webpage to analyze.
            keyword (str, optional): A specific keyword to check density for. If None, returns density for all words.

        Returns:
            dict: Results including word counts, total words, and density percentage.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        text = get_text_from_html(soup).lower()
        # Basic tokenization: split on non-alphanumeric, ignore very short words (<2 chars)
        words = [w for w in re.findall(r'\b\w+\b', text) if len(w) > 1]
        total_words = len(words)

        if total_words == 0:
            return {"error": "No text found on the page."}

        word_counts = Counter(words)

        if keyword:
            k = keyword.lower()
            count = word_counts.get(k, 0)
            density = (count / total_words) * 100
            return {
                "keyword": k,
                "count": count,
                "total_words": total_words,
                "density_percent": round(density, 2),
                "message": f"'{k}' appears {count} times ({density:.2f}%) out of {total_words} words."
            }
        else:
            # Top 10 most frequent words for summary
            most_common = word_counts.most_common(10)
            density_list = [
                {"word": w, "count": c, "density_percent": round((c / total_words) * 100, 2)}
                for w, c in most_common
            ]
            return {
                "total_words": total_words,
                "top_words": density_list,
                "message": "Top 10 most frequent words and their density on the page."
            }