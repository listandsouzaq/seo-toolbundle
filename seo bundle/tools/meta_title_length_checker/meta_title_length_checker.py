"""
tools/meta_title_length_checker/meta_title_length_checker.py

Meta Title Length Checker Tool.
"""

import streamlit as st
from tools.base_tool import BaseTool
from core.utils import get_page_content

class MetaTitleLengthChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Meta Title Length Checker",
            description="Analyzes a page's meta title for optimal length (30-60 characters)."
        )

    def run(self, url: str) -> dict:
        soup = get_page_content(url)
        if not soup:
            st.error("Could not fetch page content.")
            return {"error": "Could not fetch page content."}

        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else ""
        length = len(title)

        if not title:
            status = "Missing"
        elif length < 30:
            status = "Too Short"
        elif length > 60:
            status = "Too Long"
        else:
            status = "Good"

        return {
            "title": title if title else "No <title> tag found.",
            "length": length,
            "status": status,
            "message": f"Title is {length} characters long. Recommended: 30-60 characters."
        }

# Streamlit UI (for testing or as a standalone tool page)
if __name__ == "__main__" or st._is_running_with_streamlit:
    st.title("Meta Title Length Checker")
    st.write("Analyze the meta title length of any web page for optimal SEO.")
    url = st.text_input("Enter URL to analyze")
    if st.button("Run Analysis") and url:
        tool = MetaTitleLengthChecker()
        result = tool.run(url)
        if "error" in result:
            st.error(result["error"])
        else:
            st.write("**Title:**", result["title"])
            st.write("**Length:**", result["length"])
            st.write("**Status:**", result["status"])
            st.info(result["message"])