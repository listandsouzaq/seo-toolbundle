"""
Schema Markup Presence Checker Tool

Checks if the page contains any schema.org markup via Microdata, RDFa, or JSON-LD.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content

class SchemaMarkupPresenceChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Schema Markup Presence Checker",
            description="Checks for the presence of schema.org markup (Microdata, RDFa, or JSON-LD)."
        )

    def run(self, url: str) -> dict:
        """
        Checks for schema.org in microdata, RDFa, or JSON-LD.
        Returns a dict indicating presence and examples.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        found = False
        details = []

        # Check for microdata or RDFa
        for tag in soup.find_all(attrs={"itemtype": True}):
            if "schema.org" in tag["itemtype"]:
                found = True
                details.append({"itemtype": tag["itemtype"], "tag": str(tag)[:100]})

        # Check for JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            if script.string and "schema.org" in script.string:
                found = True
                details.append({"jsonld": script.string[:100]})

        message = "Schema.org markup found." if found else "No schema.org markup found."
        return {
            "schema_markup_found": found,
            "examples": details[:3],
            "message": message
        }