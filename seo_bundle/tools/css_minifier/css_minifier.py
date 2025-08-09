"""
tools/css_minifier/css_minifier.py

CSS Minifier Tool.
"""

import streamlit as st
import requests
import cssmin
from tools.base_tool import BaseTool

class CssMinifier(BaseTool):
    def __init__(self):
        super().__init__(
            name="CSS Minifier",
            description="Minifies CSS content to reduce file size and improve page load time."
        )

    def run(self, url: str) -> dict:
        """
        Minifies the CSS content from a given URL.
        """
        st.text("CssMinifier tool is running...")
        try:
            st.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes

            original_css = response.text
            minified_css = cssmin.cssmin(original_css)

            if not minified_css:
                return {
                    "status": "Error",
                    "message": "Minification failed. The provided content may not be valid CSS."
                }

            return {
                "status": "Success",
                "message": "CSS minified successfully.",
                "original_size": len(original_css),
                "minified_size": len(minified_css),
                "reduction_percent": (1 - (len(minified_css) / len(original_css))) * 100,
                "minified_css": minified_css
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
    st.title("CSS Minifier")
    st.write("Enter a URL to minify its CSS content.")
    url = st.text_input("Enter URL", placeholder="https://www.example.com/styles.css")
    
    if st.button("Run Analysis") and url:
        tool = CssMinifier()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        else:
            st.success(result["message"])
            st.write(f"Original size: {result['original_size']} characters")
            st.write(f"Minified size: {result['minified_size']} characters")
            st.write(f"Size reduction: {result['reduction_percent']:.2f}%")
            
            with st.expander("View Minified CSS"):
                st.code(result["minified_css"], language="css")
