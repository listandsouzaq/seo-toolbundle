"""
Alt Tag Missing Finder Tool

Finds all <img> tags missing the alt attribute or with empty alt text.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class AltTagMissingFinder(BaseTool):
    def __init__(self):
        super().__init__(
            name="Alt Tag Missing Finder",
            description="Finds all images missing alt attribute or with empty alt text."
        )

    def run(self, url: str) -> dict:
        """
        Returns a list of image tags missing alt or with empty alt.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        missing = []
        for img in soup.find_all("img"):
            if not img.has_attr("alt") or not img["alt"].strip():
                src = img.get("src", "")
                missing.append({"src": src, "alt": img.get("alt", "")})

        return {
            "missing_alt_count": len(missing),
            "missing_images": missing,
            "message": f"Found {len(missing)} image(s) missing alt attribute."
        }