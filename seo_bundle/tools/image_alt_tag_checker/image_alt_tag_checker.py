"""
Image Alt Tag Checker Tool

This tool checks all <img> tags on a given web page to determine which images are missing
alt attributes or have empty alt attributes. Useful for accessibility and SEO.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class ImageAltTagChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Image Alt Tag Checker",
            description="Checks all images for missing or empty alt attributes."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, extract all <img> tags, and report images missing alt attributes
        or with empty alt attributes.
        Returns a dict summarizing the results.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}
        
        img_tags = soup.find_all('img')
        total_imgs = len(img_tags)
        missing_alt = []
        empty_alt = []
        for img in img_tags:
            src = img.get('src', '')
            alt = img.get('alt')
            if alt is None:
                missing_alt.append(src)
            elif alt.strip() == "":
                empty_alt.append(src)
        
        return {
            "total_images": total_imgs,
            "missing_alt_count": len(missing_alt),
            "empty_alt_count": len(empty_alt),
            "missing_alt_images": missing_alt,
            "empty_alt_images": empty_alt,
            "message": (
                f"Out of {total_imgs} images: "
                f"{len(missing_alt)} missing alt, {len(empty_alt)} have empty alt."
            )
        }