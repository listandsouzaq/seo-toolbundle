"""
Heading Tag Structure Analyzer (H1–H6) Tool

This tool analyzes the structure and usage of heading tags (H1 to H6) on a web page.
It helps you identify heading hierarchy issues, missing headings, and provides a summary of heading usage for SEO and accessibility.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class HeadingTagStructureAnalyzer(BaseTool):
    def __init__(self):
        super().__init__(
            name="Heading Tag Structure Analyzer (H1–H6)",
            description="Analyzes and summarizes the usage and structure of H1–H6 tags on a web page."
        )

    def run(self, url: str) -> dict:
        """
        Fetch the page, extract all H1–H6 tags, and analyze their structure.
        Returns a dict with counts, structure order, and potential issues.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
        heading_counts = {tag.upper(): 0 for tag in heading_tags}
        heading_order = []
        headings_detail = []

        # Collect heading counts, order, and text
        for tag in heading_tags:
            for el in soup.find_all(tag):
                text = el.get_text(strip=True)
                heading_counts[tag.upper()] += 1
                heading_order.append(tag.upper())
                headings_detail.append({"level": tag.upper(), "text": text})

        # Analyze for issues
        issues = []
        if heading_counts["H1"] == 0:
            issues.append("No H1 tag found. Every page should have one H1 heading.")
        elif heading_counts["H1"] > 1:
            issues.append(f"Multiple ({heading_counts['H1']}) H1 tags found. Use only one H1 per page.")

        # Check for jumps in heading levels (e.g., H1 to H3 with no H2 in between)
        last_level = 0
        for tag in heading_order:
            level = int(tag[1])
            if last_level and (level > last_level + 1):
                issues.append(f"Heading level jumps from H{last_level} to {tag}. Consider using sequential heading levels.")
            last_level = level

        # Prepare summary
        summary = ", ".join([f"{k}: {v}" for k, v in heading_counts.items()])
        message = f"Heading summary: {summary}."
        if not issues:
            message += " Heading structure looks good."
        else:
            message += " Issues detected: " + "; ".join(issues)

        return {
            "heading_counts": heading_counts,
            "heading_order": heading_order,
            "headings_detail": headings_detail,
            "issues": issues,
            "message": message
        }