"""
tools/robots_txt_fetcher_parser/robots_txt_fetcher_parser.py
Robots.txt Fetcher & Parser Tool.
"""

import streamlit as st
import requests
from tools.base_tool import BaseTool

class RobotsTxtFetcherParser(BaseTool):
    def __init__(self):
        super().__init__(
            name="Robots.txt Fetcher & Parser",
            description="Fetches and displays the robots.txt file for a given URL."
        )

    def run(self, url: str) -> dict:
        """
        Fetches the robots.txt file for a given URL and returns its content.
        """
        robots_url = url.rstrip('/') + '/robots.txt'
        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                return {
                    "status": "Found",
                    "robots_txt_content": response.text
                }
            else:
                return {
                    "status": "Not Found",
                    "message": f"robots.txt not found at {robots_url}. Status code: {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "Error",
                "message": f"An error occurred while fetching robots.txt: {e}"
            }

# Streamlit UI (for testing or as a standalone tool page)
if __name__ == "__main__":
    st.title("Robots.txt Fetcher & Parser")
    st.write("Analyze the robots.txt file for any web page.")
    url = st.text_input("Enter URL to analyze")
    if st.button("Fetch robots.txt") and url:
        tool = RobotsTxtFetcherParser()
        result = tool.run(url)
        st.json(result)
