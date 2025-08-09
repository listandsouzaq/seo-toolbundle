"""
tools/youtube_video_tag_extractor/youtube_video_tag_extractor.py

YouTube Video Tag Extractor Tool.
"""

import streamlit as st
import requests
import re
from tools.base_tool import BaseTool

class YoutubeVideoTagExtractor(BaseTool):
    def __init__(self):
        super().__init__(
            name="YouTube Video Tag Extractor",
            description="Extracts the tags from a YouTube video page."
        )

    def run(self, url: str) -> dict:
        """
        Extracts tags from a YouTube video page.
        """
        st.text("YoutubeVideoTagExtractor tool is running...")
        if "youtube.com/watch" not in url:
            return {
                "status": "Error",
                "message": "Invalid URL. Please provide a valid YouTube video URL."
            }
        
        try:
            st.info(f"Fetching content from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # YouTube page source often contains a 'keywords' meta tag
            # We can use a regex to find this tag and extract the content
            tags_match = re.search(r'\"keywords\":\[(.*?)\]', response.text)

            if tags_match:
                tags_string = tags_match.group(1)
                # The tags are a JSON array of strings
                tags = [tag.strip().strip('"') for tag in tags_string.split(',')]
                
                return {
                    "status": "Success",
                    "message": "Tags extracted successfully.",
                    "tags": tags
                }
            else:
                return {
                    "status": "Info",
                    "message": "No tags found for this video."
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
    st.title("YouTube Video Tag Extractor")
    st.write("Enter a YouTube video URL to extract its tags.")
    url = st.text_input("Enter URL", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    if st.button("Run Analysis") and url:
        tool = YoutubeVideoTagExtractor()
        result = tool.run(url)
        
        st.subheader("Results")
        if result["status"] == "Error":
            st.error(result["message"])
        elif result["status"] == "Info":
            st.info(result["message"])
        else:
            st.success(result["message"])
            st.json(result["tags"])
