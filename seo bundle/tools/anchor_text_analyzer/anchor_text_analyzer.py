"""
Anchor Text Analyzer Tool

This tool extracts and analyzes all anchor (<a>) tags on a webpage, collecting their anchor text,
destination URLs, and categorizing anchor texts (empty, generic, branded, etc.).
Useful for understanding the distribution and quality of link anchor text on the page.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content
from urllib.parse import urlparse, urljoin

class AnchorTextAnalyzer(BaseTool):
    def __init__(self):
        super().__init__(
            name="Anchor Text Analyzer",
            description="Analyzes all anchor (<a>) tags' text and destination URLs on the web page."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, extract all anchor <a> tags, and analyze their anchor text.
        Returns a dict summarizing anchor text types and distribution.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        anchors = soup.find_all("a", href=True)
        total = len(anchors)
        empty_text = []
        generic = []
        branded = []
        descriptive = []
        others = []

        # Basic lists for generic and branded text
        generic_texts = {"click here", "more", "read more", "learn more", "here", "this link", "link"}
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        anchor_data = []

        for a in anchors:
            text = a.get_text(strip=True)
            href = urljoin(url, a['href'].strip())
            anchor_info = {
                "text": text,
                "href": href
            }
            anchor_data.append(anchor_info)

            clean_text = text.lower().strip()
            if not clean_text:
                empty_text.append(anchor_info)
            elif clean_text in generic_texts:
                generic.append(anchor_info)
            elif domain in clean_text:
                branded.append(anchor_info)
            elif len(clean_text.split()) > 2:
                descriptive.append(anchor_info)
            else:
                others.append(anchor_info)

        return {
            "total_anchor_tags": total,
            "empty_text_count": len(empty_text),
            "generic_text_count": len(generic),
            "branded_text_count": len(branded),
            "descriptive_text_count": len(descriptive),
            "other_text_count": len(others),
            "sample_empty_text": empty_text[:5],
            "sample_generic_text": generic[:5],
            "sample_branded_text": branded[:5],
            "sample_descriptive_text": descriptive[:5],
            "sample_others": others[:5],
            "all_anchor_data": anchor_data[:20],
            "message": (
                f"Analyzed {total} anchor tags. "
                f"Empty: {len(empty_text)}, Generic: {len(generic)}, "
                f"Branded: {len(branded)}, Descriptive: {len(descriptive)}, Other: {len(others)}."
            )
        }