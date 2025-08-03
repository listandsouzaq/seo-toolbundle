"""
Readability Score Calculator Tool

Calculates the Flesch-Kincaid readability score for the page content.
"""

from tools.base_tool import BaseTool
from core.utils import get_page_content
import re

class ReadabilityScoreCalculator(BaseTool):
    def __init__(self):
        super().__init__(
            name="Readability Score Calculator",
            description="Calculates the Flesch-Kincaid readability score for the page."
        )

    def run(self, url: str) -> dict:
        """
        Fetches visible text from the page and calculates Flesch-Kincaid score.
        """
        soup = get_page_content(url)
        if not soup:
            return {"error": "Could not fetch page content."}

        # Extract visible text
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=" ")
        text = re.sub(r'\s+', ' ', text).strip()

        # Sentence, word, and syllable count
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        words = re.findall(r'\w+', text)
        syllable_count = sum(self.count_syllables(word) for word in words)

        num_sentences = max(1, len(sentences))
        num_words = max(1, len(words))
        num_syllables = max(1, syllable_count)

        # Flesch-Kincaid formula
        fk_score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
        fk_score = round(fk_score, 2)

        return {
            "readability_score": fk_score,
            "num_sentences": num_sentences,
            "num_words": num_words,
            "num_syllables": num_syllables,
            "message": f"Flesch-Kincaid score: {fk_score} (higher is easier to read)"
        }

    def count_syllables(self, word):
        word = word.lower()
        syllables = re.findall(r'[aeiouy]+', word)
        return max(1, len(syllables))