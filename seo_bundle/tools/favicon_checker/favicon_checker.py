"""
Favicon Checker Tool

This tool checks for the presence of favicon on a web page by looking for <link rel="icon">,
<link rel="shortcut icon">, and other common favicon link tags in the HTML header.
It also tries common fallback file locations if no tag is found.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content, fetch_url
from urllib.parse import urljoin, urlparse

class FaviconChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Favicon Checker",
            description="Checks for the presence and accessibility of favicon on the web page."
        )

    def run(self, url: str) -> dict:
        """
        Checks HTML for favicon link tags, and tests typical fallback favicon locations.
        Returns a dict with favicon URLs found and their HTTP status.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        favicon_urls = []

        # Most common favicon link rel values
        rels = [
            "icon",
            "shortcut icon",
            "apple-touch-icon",
            "apple-touch-icon-precomposed",
            "mask-icon"
        ]
        # Extract favicon URLs from <link rel=...> tags
        for rel in rels:
            tag = soup.find("link", rel=lambda x: x and rel in x.lower())
            if tag and tag.has_attr("href"):
                favicon_url = urljoin(url, tag["href"].strip())
                if favicon_url not in favicon_urls:
                    favicon_urls.append(favicon_url)

        # If no favicon found in HTML, try the default /favicon.ico
        if not favicon_urls:
            parsed = urlparse(url)
            root = f"{parsed.scheme}://{parsed.netloc}"
            favicon_urls.append(urljoin(root, "/favicon.ico"))

        # Check accessibility for each favicon URL
        results = []
        for favicon_url in favicon_urls:
            response = fetch_url(favicon_url)
            status_code = response.status_code if response else None
            is_ok = status_code and 200 <= status_code < 400
            results.append({
                "favicon_url": favicon_url,
                "status_code": status_code,
                "accessible": is_ok
            })

        # Compose message
        if any(f["accessible"] for f in results):
            message = "Favicon found and accessible."
        else:
            message = "Favicon not found or not accessible."

        return {
            "favicons_checked": results,
            "message": message
        }