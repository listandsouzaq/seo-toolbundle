"""
Open Graph Preview Tool

Returns the core OG tags for visual preview in a card-style interface.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class OpenGraphPreview(BaseTool):
    def __init__(self):
        super().__init__(
            name="Open Graph Preview",
            description="Returns key OG tags for visual preview card."
        )

    def run(self, url: str) -> dict:
        """
        Extracts og:title, og:description, og:image, and og:url for preview.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        og_data = {}
        for prop in ["og:title", "og:description", "og:image", "og:url"]:
            tag = soup.find("meta", property=prop)
            if tag and tag.has_attr("content"):
                og_data[prop] = tag["content"]
            else:
                og_data[prop] = ""

        return {
            "og_title": og_data["og:title"],
            "og_description": og_data["og:description"],
            "og_image": og_data["og:image"],
            "og_url": og_data["og:url"],
            "message": "Open Graph preview data ready."
        }