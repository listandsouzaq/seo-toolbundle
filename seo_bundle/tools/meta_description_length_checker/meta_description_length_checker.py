"""
Meta Description Length Checker Tool

This tool analyzes a page's meta description for optimal length (120-155 characters).
It fetches the HTML, locates the <meta name="description"> tag, and evaluates
the length and quality of the description.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content
from bs4 import BeautifulSoup
from typing import Optional

class MetaDescriptionLengthChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Meta Description Length Checker",
            description="Analyzes a page's meta description for optimal length (120-155 characters)."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, find the meta description, and check its length.
        Returns a dict with the description, its length, and a status message.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        meta_desc_tag: Optional[BeautifulSoup] = soup.find('meta', attrs={'name': 'description'})
        description: str = ""
        if meta_desc_tag:
            description = meta_desc_tag.get('content', '').strip()

        length: int = len(description)

        # Determine status based on length
        if length == 0:
            status = "Missing"
        elif length < 120:
            status = "Too Short"
        elif length > 155:
            status = "Too Long"
        else:
            status = "Good"

        return {
            "description": description,
            "length": length,
            "status": status,
            "message": f"Description is {length} characters long. Recommended: 120-155 characters."
        }