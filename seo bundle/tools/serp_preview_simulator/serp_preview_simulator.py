"""
SERP Preview Simulator Tool

Simulates a Google SERP preview. Since this is for Streamlit, this tool just returns data for preview rendering.
"""

from tools.base_tool import BaseTool

class SERPPreviewSimulator(BaseTool):
    def __init__(self):
        super().__init__(
            name="SERP Preview Simulator",
            description="Simulates a SERP preview from provided title, description, and URL (use Streamlit to render)."
        )

    def run(self, url: str) -> dict:
        """
        Expects a string like: 'TITLE|||DESCRIPTION|||URL'
        Returns dict for preview rendering.
        """
        try:
            title, desc, page_url = url.split("|||")
        except Exception:
            return {"error": "Input must be 'TITLE|||DESCRIPTION|||URL'"}
        return {
            "title": title.strip(),
            "description": desc.strip(),
            "url": page_url.strip(),
            "message": "SERP preview data ready."
        }