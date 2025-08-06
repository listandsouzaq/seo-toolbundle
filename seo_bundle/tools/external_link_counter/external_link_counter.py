"""
External Link Counter Tool

This tool counts the number of external links (<a> tags pointing to different domains)
on a web page. It helps you analyze your outbound linking structure for SEO.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content
from urllib.parse import urlparse, urljoin

class ExternalLinkCounter(BaseTool):
    def __init__(self):
        super().__init__(
            name="External Link Counter",
            description="Counts the number of external links on the web page."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, parse all <a> tags, and count how many are external links.
        Returns a dict with the total external link count and a sample list.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc

        external_links = []

        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            # Ignore empty, anchor, or javascript links
            if not href or href.startswith("#") or href.lower().startswith("javascript:"):
                continue

            # Normalize link
            full_url = urljoin(url, href)
            parsed_link = urlparse(full_url)

            # External if it has a netloc and it's not the base domain
            if parsed_link.netloc and parsed_link.netloc != base_domain:
                external_links.append(full_url)

        # Remove duplicates, keep order
        seen = set()
        unique_external_links = []
        for link in external_links:
            if link not in seen:
                unique_external_links.append(link)
                seen.add(link)

        return {
            "external_link_count": len(unique_external_links),
            "sample_external_links": unique_external_links[:10],
            "message": f"Found {len(unique_external_links)} external link(s) on the page."
        }