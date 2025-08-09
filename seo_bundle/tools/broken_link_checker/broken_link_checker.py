"""
tools/broken_link_checker/broken_link_checker.py

Broken Link Checker Tool.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup, SoupStrainer
from tools.base_tool import BaseTool

class BrokenLinkChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Broken Link Checker",
            description="Scans a page for broken internal and external links."
        )

    def run(self, url: str) -> dict:
        """
        Scans a page for broken links.
        """
        st.text("BrokenLinkChecker tool is running...") # Added for debugging
        broken_links = []
        try:
            st.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return {
                    "status": "Error",
                    "message": f"Could not fetch page content. Status code: {response.status_code}"
                }
            
            # Parse only the links from the HTML to save time and resources
            links_only = SoupStrainer('a')
            soup = BeautifulSoup(response.text, 'html.parser', parse_only=links_only)
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Ignore mailto, javascript, and other non-HTTP links
                if href.startswith('http'):
                    try:
                        st.text(f"Checking link: {href}")
                        link_response = requests.head(href, timeout=5, allow_redirects=True)
                        if link_response.status_code >= 400:
                            broken_links.append({
                                "url": href,
                                "status_code": link_response.status_code
                            })
                    except requests.exceptions.RequestException as e:
                        broken_links.append({
                            "url": href,
                            "status_code": "Error",
                            "error_message": str(e)
                        })
            
            if not broken_links:
                return {
                    "status": "Success",
                    "message": "No broken links found on the page."
                }
            else:
                return {
                    "status": "Warning",
                    "message": f"Found {len(broken_links)} broken links.",
                    "broken_links": broken_links
                }
        
        except requests.exceptions.RequestException as e:
            return {
                "status": "Error",
                "message": f"An error occurred while fetching the page: {e}"
            }

# Streamlit UI (for testing or as a standalone tool page)
if __name__ == "__main__":
    st.title("Broken Link Checker")
    st.write("Enter a URL to scan for broken links.")
    url = st.text_input("Enter URL", placeholder="https://www.example.com")
    
    if st.button("Run Analysis") and url:
        tool = BrokenLinkChecker()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        elif result["status"] == "Warning":
            st.warning(result["message"])
            st.json(result["broken_links"])
        else:
            st.success(result["message"])
