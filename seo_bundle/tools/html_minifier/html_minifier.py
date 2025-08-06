"""
tools/html_minifier/html_minifier.py

HTML Minifier Tool.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from tools.base_tool import BaseTool

class HtmlMinifier(BaseTool):
    def __init__(self):
        super().__init__(
            name="HTML Minifier",
            description="Minifies HTML content to reduce file size and improve page load time."
        )

    def run(self, url: str) -> dict:
        """
        Minifies the HTML content of a given URL.
        """
        st.text("HtmlMinifier tool is running...")
        try:
            st.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # Use BeautifulSoup to parse the HTML and then get the minified version
            soup = BeautifulSoup(response.text, 'html.parser')
            minified_html = str(soup)

            return {
                "status": "Success",
                "message": "HTML minified successfully.",
                "original_size": len(response.text),
                "minified_size": len(minified_html),
                "reduction_percent": (1 - (len(minified_html) / len(response.text))) * 100,
                "minified_html": minified_html
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "Error",
                "message": f"An error occurred while fetching the page: {e}"
            }
        except Exception as e:
            return {
                "status": "Error",
                "message": f"An unexpected error occurred: {e}"
            }

# Streamlit UI (for testing or as a standalone tool page)
if __name__ == "__main__":
    st.title("HTML Minifier")
    st.write("Enter a URL to minify its HTML content.")
    url = st.text_input("Enter URL", placeholder="https://www.example.com")
    
    if st.button("Run Analysis") and url:
        tool = HtmlMinifier()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        else:
            st.success(result["message"])
            st.write(f"Original size: {result['original_size']} characters")
            st.write(f"Minified size: {result['minified_size']} characters")
            st.write(f"Size reduction: {result['reduction_percent']:.2f}%")
            
            with st.expander("View Minified HTML"):
                st.code(result["minified_html"], language="html")
