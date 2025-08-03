"""
HTML Minifier Tool

Minifies HTML by removing extra whitespace, comments, and line breaks.
"""

from tools.base_tool import BaseTool

import re

class HTMLMinifier(BaseTool):
    def __init__(self):
        super().__init__(
            name="HTML Minifier",
            description="Minifies HTML code by removing whitespace and comments. (Pass HTML in URL parameter)"
        )

    def run(self, url: str) -> dict:
        """
        Expects raw HTML in the 'url' parameter.
        Returns minified HTML.
        """
        html = url
        # Remove comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        # Remove leading/trailing whitespace and multiple spaces
        html = re.sub(r'>\s+<', '><', html)
        html = re.sub(r'\s+', ' ', html)
        html = html.strip()
        return {
            "minified_html": html,
            "message": "HTML minified."
        }