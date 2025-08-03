# tools/readability_score_calculator/readability_score_calculator.py

import streamlit as st
from tools.base_tool import BaseTool
from core.utils import get_page_content, get_text_from_html
import textstat
from typing import Dict, Any

class ReadabilityScoreCalculator(BaseTool):
    """
    Analyzes a webpage's text content and calculates its readability score.
    Uses the Flesch-Kincaid reading ease formula via the textstat library.
    """
    def __init__(self):
        super().__init__(
            name="Readability Score Calculator",
            description="Analyzes text content for readability using the Flesch-Kincaid formula."
        )

    def run(self, url: str) -> Dict[str, Any]:
        """
        Fetches the webpage content, extracts clean text, and calculates the readability score.
        
        Args:
            url (str): The URL of the page to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing the readability score and a message.
        """
        try:
            soup = get_page_content(url)
            if not soup:
                return {"error": "Could not fetch page content."}
            
            # Extract clean, readable text from the HTML
            text = get_text_from_html(soup)

            if not text:
                return {"error": "Could not extract readable text from the page."}

            # Use the textstat library to calculate the Flesch-Kincaid reading ease score
            flesch_reading_ease = textstat.flesch_reading_ease(text)
            flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
            
            # Determine a message based on the score
            if flesch_reading_ease >= 60:
                message = "The text is relatively easy to read and understand for a general audience."
            else:
                message = "The text may be somewhat difficult to read. Consider simplifying sentences."

            return {
                "url": url,
                "flesch_reading_ease": flesch_reading_ease,
                "flesch_kincaid_grade": flesch_kincaid_grade,
                "message": message
            }
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
