"""
tools/js_minifier/js_minifier.py

JS Minifier Tool.
"""

import streamlit as st
import requests
import jsmin
from tools.base_tool import BaseTool

class JsMinifier(BaseTool):
    def __init__(self):
        super().__init__(
            name="JS Minifier",
            description="Minifies JavaScript content to reduce file size and improve page load time."
        )

    def run(self, url: str) -> dict:
        """
        Minifies the JavaScript content from a given URL.
        """
        st.text("JsMinifier tool is running...")
        try:
            st.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes

            original_js = response.text
            minified_js = jsmin.jsmin(original_js)

            if not minified_js:
                return {
                    "status": "Error",
                    "message": "Minification failed. The provided content may not be valid JavaScript."
                }

            return {
                "status": "Success",
                "message": "JavaScript minified successfully.",
                "original_size": len(original_js),
                "minified_size": len(minified_js),
                "reduction_percent": (1 - (len(minified_js) / len(original_js))) * 100,
                "minified_js": minified_js
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
    st.title("JS Minifier")
    st.write("Enter a URL to minify its JavaScript content.")
    url = st.text_input("Enter URL", placeholder="https://www.example.com/script.js")
    
    if st.button("Run Analysis") and url:
        tool = JsMinifier()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        else:
            st.success(result["message"])
            st.write(f"Original size: {result['original_size']} characters")
            st.write(f"Minified size: {result['minified_size']} characters")
            st.write(f"Size reduction: {result['reduction_percent']:.2f}%")
            
            with st.expander("View Minified JavaScript"):
                st.code(result["minified_js"], language="javascript")
