"""
tools/sitemap_xml_fetcher_validator/sitemap_xml_fetcher_validator.py

Sitemap XML Fetcher & Validator Tool.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from tools.base_tool import BaseTool

class SitemapXmlFetcherValidator(BaseTool):
    def __init__(self):
        super().__init__(
            name="Sitemap.xml Fetcher & Validator",
            description="Fetches and validates the sitemap.xml file of a website."
        )

    def run(self, url: str) -> dict:
        """
        Fetches a sitemap.xml file and extracts all URLs.
        """
        sitemap_url = url.rstrip('/') + '/sitemap.xml'
        try:
            st.info(f"Attempting to fetch sitemap from: {sitemap_url}")
            response = requests.get(sitemap_url, timeout=10)
            
            if response.status_code != 200:
                return {
                    "status": "Error",
                    "message": f"Could not fetch sitemap.xml. Status code: {response.status_code}"
                }

            sitemap_content = response.text
            soup = BeautifulSoup(sitemap_content, 'xml')
            
            urls = []
            for loc in soup.find_all('loc'):
                urls.append(loc.text)

            if not urls:
                return {
                    "status": "Valid",
                    "message": "Sitemap.xml found, but no URLs were extracted. It may be empty or malformed."
                }

            return {
                "status": "Valid",
                "total_urls": len(urls),
                "urls": urls[:20]  # Displaying the first 20 URLs for brevity
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "Error",
                "message": f"An error occurred while fetching sitemap.xml: {e}"
            }
        except Exception as e:
            return {
                "status": "Error",
                "message": f"An unexpected error occurred during sitemap parsing: {e}"
            }

# Streamlit UI (for testing or as a standalone tool page)
if __name__ == "__main__":
    st.title("Sitemap.xml Fetcher & Validator")
    st.write("Enter a URL to fetch and validate its sitemap.xml file.")
    url = st.text_input("Enter URL", placeholder="https://www.example.com")
    
    if st.button("Run Analysis") and url:
        tool = SitemapXmlFetcherValidator()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        elif "total_urls" in result:
            st.success(f"Sitemap.xml successfully fetched and validated. Found {result['total_urls']} URLs.")
            st.json(result)
        else:
            st.info(result["message"])
