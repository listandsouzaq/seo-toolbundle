"""
H1 Tag Extractor Tool

This tool extracts all <h1> tag contents from a given web page. It fetches the HTML,
parses it, and returns a list of all H1 headings found.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class H1TagExtractor(BaseTool):
    def __init__(self):
        super().__init__(
            name="H1 Tag Extractor",
            description="Extracts and displays all H1 tags from the web page."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, find all <h1> tags, and return their contents.
        Returns a dict with the list of H1 tags and count.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        h1_tags = soup.find_all('h1')
        h1_texts = [tag.get_text(strip=True) for tag in h1_tags]

        return {
            "h1_tags": h1_texts,
            "count": len(h1_texts),
            "message": f"Found {len(h1_texts)} H1 tag(s) on the page."
        }