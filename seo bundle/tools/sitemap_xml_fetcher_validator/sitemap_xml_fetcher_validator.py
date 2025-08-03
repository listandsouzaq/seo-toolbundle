"""
Sitemap.xml Fetcher & Validator Tool

This tool fetches a website's sitemap.xml file, checks if it exists, and validates its XML structure.
It also counts the number of <url> entries and reports any parsing errors.
"""

from tools.base_tool import BaseTool
from core.utils import fetch_url
import xml.etree.ElementTree as ET

class SitemapXMLFetcherValidator(BaseTool):
    def __init__(self):
        super().__init__(
            name="Sitemap.xml Fetcher & Validator",
            description="Fetches and validates the sitemap.xml file, counts URLs, and checks for XML errors."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the sitemap.xml, check its existence and validity, and count <url> entries.
        Returns a dict summarizing the results.
        """
        # Build the sitemap.xml URL from the root domain
        if "://" not in url:
            return {"error": "Invalid URL format."}

        try:
            # Extract the domain root (e.g., https://example.com)
            proto, rest = url.split("://", 1)
            domain = rest.split("/", 1)[0]
            sitemap_url = f"{proto}://{domain}/sitemap.xml"
        except Exception:
            return {"error": "Unable to parse URL for sitemap.xml location."}

        response = fetch_url(sitemap_url)
        if not response or response.status_code != 200:
            return {
                "sitemap_url": sitemap_url,
                "status_code": getattr(response, "status_code", None),
                "error": f"Sitemap.xml not found or not accessible at {sitemap_url}."
            }

        xml_content = response.text
        try:
            root = ET.fromstring(xml_content)
            url_count = len(root.findall(".//url"))
            status = "Valid"
            message = f"Sitemap.xml is valid and contains {url_count} <url> entries."
        except ET.ParseError as e:
            url_count = 0
            status = "Invalid"
            message = f"Sitemap.xml is not valid XML: {e}"

        return {
            "sitemap_url": sitemap_url,
            "status": status,
            "url_count": url_count,
            "message": message
        }