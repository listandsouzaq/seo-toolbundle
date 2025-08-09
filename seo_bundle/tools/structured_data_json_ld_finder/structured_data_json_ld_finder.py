"""
tools/structured_data_json_ld_finder/structured_data_json_ld_finder.py

Structured Data Finder Tool.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
from tools.base_tool import BaseTool

class StructuredDataFinder(BaseTool):
    def __init__(self):
        super().__init__(
            name="Structured Data Finder",
            description="Finds and extracts JSON-LD structured data from a webpage."
        )

    def run(self, url: str) -> dict:
        """
        Finds and extracts JSON-LD structured data from a webpage.
        """
        st.text("StructuredDataFinder tool is running...")
        structured_data_list = []
        try:
            st.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return {
                    "status": "Error",
                    "message": f"Could not fetch page content. Status code: {response.status_code}"
                }

            soup = BeautifulSoup(response.text, 'html.parser')
            
            json_ld_scripts = soup.find_all('script', type='application/ld+json')

            if not json_ld_scripts:
                return {
                    "status": "Info",
                    "message": "No JSON-LD structured data found on the page."
                }

            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    structured_data_list.append(data)
                except json.JSONDecodeError as e:
                    structured_data_list.append({
                        "error": "JSON Decode Error",
                        "message": str(e),
                        "script_content": script.string
                    })

            if structured_data_list:
                return {
                    "status": "Success",
                    "message": f"Found {len(structured_data_list)} JSON-LD structured data blocks.",
                    "structured_data": structured_data_list
                }
            else:
                return {
                    "status": "Warning",
                    "message": "Found <script type='application/ld+json'> tags, but could not parse the content.",
                    "structured_data": structured_data_list
                }

        except requests.exceptions.RequestException as e:
            return {
                "status": "Error",
                "message": f"An error occurred while fetching the page: {e}"
            }

# Streamlit UI (for testing or as a standalone tool page)
if __name__ == "__main__":
    st.title("Structured Data Finder")
    st.write("Enter a URL to find JSON-LD structured data.")
    url = st.text_input("Enter URL", placeholder="https://www.example.com")
    
    if st.button("Run Analysis") and url:
        tool = StructuredDataFinder()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        elif result["status"] == "Warning":
            st.warning(result["message"])
            st.json(result["structured_data"])
        elif result["status"] == "Success":
            st.success(result["message"])
            st.json(result["structured_data"])
        else:
            st.info(result["message"])
