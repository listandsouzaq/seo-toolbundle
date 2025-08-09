"""
Keyword Suggestions from Related Words Tool

Suggests related keywords using a static list and synonyms module if available.
"""

from tools.base_tool import BaseTool

try:
    from synonyms import synonyms
except ImportError:
    synonyms = None

class KeywordSuggestionsFromRelatedWords(BaseTool):
    def __init__(self):
        super().__init__(
            name="Keyword Suggestions from Related Words",
            description="Suggests related keywords using synonyms or static lists."
        )
        # Basic static related words for demonstration
        self.static_related = {
            "seo": ["search engine optimization", "google ranking", "organic traffic", "site optimization"],
            "website": ["site", "webpage", "portal", "web presence"],
            "speed": ["performance", "load time", "latency", "response time"]
        }

    def run(self, url: str) -> dict:
        """
        Returns related keywords for a keyword extracted from URL or user input.
        For this tool, expects a keyword in URL parameter.
        """
        keyword = url.strip().lower()
        suggestions = set()
        # Static suggestions
        suggestions.update(self.static_related.get(keyword, []))
        # Synonyms module
        if synonyms:
            try:
                syns = synonyms(keyword)
                suggestions.update(syns)
            except Exception:
                pass
        suggestions = list(suggestions)
        message = f"Found {len(suggestions)} suggestions." if suggestions else "No suggestions found."
        return {
            "keyword": keyword,
            "suggestions": suggestions,
            "message": message
        }