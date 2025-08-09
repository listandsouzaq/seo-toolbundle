"""
Twitter Card Preview Tool

Returns the core Twitter Card tags for visual preview in a card-style interface.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class TwitterCardPreview(BaseTool):
    def __init__(self):
        super().__init__(
            name="Twitter Card Preview",
            description="Returns key Twitter Card tags for visual preview."
        )

    def run(self, url: str) -> dict:
        """
        Extracts twitter:title, twitter:description, twitter:image, and twitter:card for preview.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        tw_data = {}
        for prop in ["twitter:title", "twitter:description", "twitter:image", "twitter:card"]:
            tag = soup.find("meta", attrs={"name": prop})
            if tag and tag.has_attr("content"):
                tw_data[prop] = tag["content"]
            else:
                tw_data[prop] = ""

        return {
            "twitter_title": tw_data["twitter:title"],
            "twitter_description": tw_data["twitter:description"],
            "twitter_image": tw_data["twitter:image"],
            "twitter_card": tw_data["twitter:card"],
            "message": "Twitter Card preview data ready."
        }