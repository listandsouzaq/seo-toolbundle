"""
CSS Minifier Tool

Minifies CSS code by removing whitespace and comments.
"""

from tools.base_tool import BaseTool
import re

class CSSMinifier(BaseTool):
    def __init__(self):
        super().__init__(
            name="CSS Minifier",
            description="Minifies CSS code by removing whitespace and comments. (Pass CSS in URL parameter)"
        )

    def run(self, url: str) -> dict:
        """
        Expects raw CSS in the 'url' parameter.
        Returns minified CSS.
        """
        css = url
        # Remove comments
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        # Remove whitespace around symbols
        css = re.sub(r'\s*([{}:;,])\s*', r'\1', css)
        css = re.sub(r';+\}', '}', css)
        # Remove unnecessary whitespace
        css = re.sub(r'\s+', ' ', css).strip()
        return {
            "minified_css": css,
            "message": "CSS minified."
        }