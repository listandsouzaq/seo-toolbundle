"""
tools/serp_preview_simulator/serp_preview_simulator.py

SERP Preview Simulator Tool.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from tools.base_tool import BaseTool

class SerpPreviewSimulator(BaseTool):
    def __init__(self):
        super().__init__(
            name="SERP Preview Simulator",
            description="Simulates how a page title and description will look in Google SERP."
        )

    def run(self, url: str) -> dict:
        """
        Fetches a page's title and description to simulate SERP preview.
        """
        st.text("SerpPreviewSimulator tool is running...")
        try:
            st.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title tag
            title = soup.find('title').string if soup.find('title') else "No title found"
            
            # Extract meta description
            meta_description = ""
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag and 'content' in meta_tag.attrs:
                meta_description = meta_tag['content']
            else:
                meta_description = "No meta description found"

            return {
                "status": "Success",
                "message": "Successfully fetched title and meta description for SERP preview.",
                "page_title": title,
                "meta_description": meta_description
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
    st.title("SERP Preview Simulator")
    st.write("Enter a URL to see how it might appear in Google search results.")
    url = st.text_input("Enter URL", placeholder="https://www.example.com")
    
    if st.button("Run Analysis") and url:
        tool = SerpPreviewSimulator()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        else:
            st.success(result["message"])
            st.markdown("### Simulated SERP Snippet")
            st.markdown(f"[{result['page_title']}]({url})")
            st.write(result['meta_description'])
