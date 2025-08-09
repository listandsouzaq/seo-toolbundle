"""
Canonical Tag Checker Tool

This tool checks for the presence and value of the <link rel="canonical"> tag on a given web page.
It helps ensure canonicalization is set for SEO best practices.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class CanonicalTagChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Canonical Tag Checker",
            description="Checks for the presence and value of the canonical link tag."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, extract the canonical tag, and provide its value.
        Returns a dict with the canonical URL (if any) and a status message.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        tag = soup.find("link", rel="canonical")
        canonical_url = tag["href"].strip() if tag and tag.has_attr("href") else ""

        if canonical_url:
            status = "Found"
            message = f"Canonical tag found: {canonical_url}"
        else:
            status = "Missing"
            message = "No canonical tag found on the page."

        return {
            "canonical_url": canonical_url,
            "status": status,
            "message": message
        }