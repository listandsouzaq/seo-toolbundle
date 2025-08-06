"""
Keyword Case Converter Tool

Converts keywords to upper, lower, snake, or kebab case.
"""

from tools.base_tool import BaseTool

class KeywordCaseConverter(BaseTool):
    def __init__(self):
        super().__init__(
            name="Keyword Case Converter",
            description="Converts keywords to upper, lower, snake, or kebab case. (Pass keyword in URL parameter)"
        )

    def run(self, url: str) -> dict:
        """
        Expects the keyword string as the 'url' parameter.
        Returns the keyword in different cases.
        """
        keyword = url.strip()
        lower = keyword.lower()
        upper = keyword.upper()
        snake = lower.replace(" ", "_").replace("-", "_")
        kebab = lower.replace(" ", "-").replace("_", "-")

        return {
            "original": keyword,
            "lower": lower,
            "upper": upper,
            "snake_case": snake,
            "kebab_case": kebab,
            "message": "Keyword case conversions."
        }