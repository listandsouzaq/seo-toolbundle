"""
Social Meta Tag Extractor Tool

Extracts Open Graph (OG) and Twitter Card meta tags for social sharing optimization.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class SocialMetaTagExtractor(BaseTool):
    def __init__(self):
        super().__init__(
            name="Social Meta Tag Extractor",
            description="Extracts Open Graph and Twitter Card meta tags from the page."
        )

    def run(self, url: str) -> dict:
        """
        Extracts OG and Twitter Card meta tags from the HTML.
        Returns a dict with all found social meta tags and their values.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        og_tags = {}
        twitter_tags = {}

        for tag in soup.find_all("meta"):
            prop = tag.get("property") or tag.get("name")
            if not prop:
                continue
            content = tag.get("content", "")
            if prop.startswith("og:"):
                og_tags[prop] = content
            elif prop.startswith("twitter:"):
                twitter_tags[prop] = content

        return {
            "og_tags": og_tags,
            "twitter_tags": twitter_tags,
            "message": f"Found {len(og_tags)} Open Graph and {len(twitter_tags)} Twitter Card tags."
        }