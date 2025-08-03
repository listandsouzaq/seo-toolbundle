"""
Structured Data (JSON-LD) Finder Tool

This tool extracts all JSON-LD structured data blocks from a web page.
It is useful for checking if the page contains schema.org markup and for validating
the presence and count of structured data for SEO purposes.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class StructuredDataJSONLDFinder(BaseTool):
    def __init__(self):
        super().__init__(
            name="Structured Data (JSON-LD) Finder",
            description="Finds and returns all JSON-LD structured data blocks from the web page."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page and extract all <script type="application/ld+json"> blocks.
        Returns a dict containing the count and content of all JSON-LD blocks found.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        json_ld_blocks = []
        for script in soup.find_all("script", type="application/ld+json"):
            if script.string:
                json_ld_blocks.append(script.string.strip())

        count = len(json_ld_blocks)
        message = f"Found {count} JSON-LD structured data block(s) on the page." if count else "No JSON-LD structured data found on the page."

        return {
            "json_ld_count": count,
            "json_ld_blocks": json_ld_blocks,
            "message": message
        }