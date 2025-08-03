"""
YouTube Video Tag Extractor Tool

Extracts tags from pasted YouTube video HTML (expects HTML as input).
"""

from tools.base_tool import BaseTool
from bs4 import BeautifulSoup

class YouTubeVideoTagExtractor(BaseTool):
    def __init__(self):
        super().__init__(
            name="YouTube Video Tag Extractor",
            description="Extracts tags from pasted YouTube video HTML (expects HTML as input)."
        )

    def run(self, url: str) -> dict:
        """
        Expects YouTube video HTML source in the 'url' parameter.
        Returns tags found in the HTML.
        """
        html = url
        soup = BeautifulSoup(html, "html.parser")
        # YouTube tags are usually in <meta property="og:video:tag" content="...">
        tags = []
        for meta in soup.find_all("meta", property="og:video:tag"):
            if meta.has_attr("content"):
                tags.append(meta["content"])
        return {
            "tags": tags,
            "message": f"Found {len(tags)} YouTube video tag(s)."
        }