"""
Keyword Position Estimator Tool

Estimates the position (ranking) of a keyword in the page content by order of appearance.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content
import re

class KeywordPositionEstimator(BaseTool):
    def __init__(self):
        super().__init__(
            name="Keyword Position Estimator",
            description="Estimates position of a keyword in the page's text (order of appearance)."
        )

    def run(self, url: str) -> dict:
        """
        Expects 'keyword|||url' in the url parameter for this tool.
        Returns list of positions (zero-indexed word number where keyword appears).
        """
        try:
            keyword, page_url = url.split("|||")
            keyword = keyword.strip().lower()
        except Exception:
            return {"error": "Input must be 'keyword|||url'"}

        soup = get_page_content(page_url)
        if not soup:
            return {"error": "Could not fetch page content."}

        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=" ")
        text = re.sub(r'[^\w\s]', '', text).lower()
        words = text.split()

        positions = [i for i, w in enumerate(words) if w == keyword]

        return {
            "keyword": keyword,
            "positions": positions,
            "occurrences": len(positions),
            "message": f"Keyword '{keyword}' found {len(positions)} time(s)."
        }