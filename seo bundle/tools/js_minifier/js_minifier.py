"""
JS Minifier Tool

Minifies JavaScript code by removing whitespace and comments. (Very basic, not a full JS parser.)
"""

from tools.base_tool import BaseTool
import re

class JSMinifier(BaseTool):
    def __init__(self):
        super().__init__(
            name="JS Minifier",
            description="Minifies JS code by removing whitespace and comments. (Pass JS in URL parameter)"
        )

    def run(self, url: str) -> dict:
        """
        Expects raw JS in the 'url' parameter.
        Returns minified JS.
        """
        js = url
        # Remove single-line comments
        js = re.sub(r'//.*', '', js)
        # Remove multi-line comments
        js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
        # Remove unnecessary whitespace
        js = re.sub(r'\s+', ' ', js)
        js = re.sub(r'\s*([=+\-*/%{};:,()<>])\s*', r'\1', js)
        js = js.strip()
        return {
            "minified_js": js,
            "message": "JS minified."
        }