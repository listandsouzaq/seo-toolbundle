"""
Mobile Responsive Check Tool

This tool checks for the presence of the viewport meta tag in the HTML, which is a key indicator
of mobile responsiveness.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class MobileResponsiveCheck(BaseTool):
    def __init__(self):
        super().__init__(
            name="Mobile Responsive Check",
            description="Checks if the page includes a viewport meta tag for mobile responsiveness."
        )

    def run(self, url: str) -> dict:
        """
        Checks for the viewport meta tag in the page's <head>.
        Returns a dict indicating presence and the tag's content value.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        meta = soup.find("meta", attrs={"name": "viewport"}) or soup.find("meta", attrs={"name": "Viewport"})
        if meta and meta.has_attr("content"):
            content = meta["content"]
            message = f"Viewport meta tag found: {content}"
            is_responsive = True
        else:
            content = ""
            message = "No viewport meta tag found. This page may not be mobile responsive."
            is_responsive = False

        return {
            "is_responsive": is_responsive,
            "viewport_content": content,
            "message": message
        }