"""
Internal Link Counter Tool

This tool counts the number of internal links (<a> tags pointing to the same domain or relative URLs)
on a web page. It helps you analyze your internal linking structure for SEO.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content
from urllib.parse import urlparse, urljoin

class InternalLinkCounter(BaseTool):
    def __init__(self):
        super().__init__(
            name="Internal Link Counter",
            description="Counts the number of internal links on the web page."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, parse all <a> tags, and count how many are internal links.
        Returns a dict with the total internal link count and optionally a sample list.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc

        internal_links = []

        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            # Ignore empty, anchor, or javascript links
            if not href or href.startswith("#") or href.lower().startswith("javascript:"):
                continue

            # Normalize link
            full_url = urljoin(url, href)
            parsed_link = urlparse(full_url)

            # Compare domain: internal if domain matches or is relative
            if parsed_link.netloc == base_domain or not parsed_link.netloc:
                internal_links.append(full_url)

        # Remove duplicates, keep order
        seen = set()
        unique_internal_links = []
        for link in internal_links:
            if link not in seen:
                unique_internal_links.append(link)
                seen.add(link)

        return {
            "internal_link_count": len(unique_internal_links),
            "sample_internal_links": unique_internal_links[:10],
            "message": f"Found {len(unique_internal_links)} internal link(s) on the page."
        }