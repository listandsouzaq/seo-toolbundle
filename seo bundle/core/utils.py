"""
core/utils.py

Common utility functions for the SEO toolkit.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import streamlit as st

def get_page_content(url: str) -> Optional[BeautifulSoup]:
    """
    Fetch the HTML content of a URL and return a BeautifulSoup object.
    Returns None if fetching fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        return None

def fetch_url(url: str) -> Optional[requests.Response]:
    """
    Fetch a URL and return the requests.Response object or None on error.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        return None

def get_text_from_html(soup: BeautifulSoup) -> str:
    """
    Extract all visible text from a BeautifulSoup object, removing excess whitespace.
    """
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())

def render_tool_ui(tool_name: str, tool_description: str):
    """
    Render a standard UI for a tool page: title, description, URL input, and a run button.
    Returns the URL if the user hits the button, else None.
    """
    st.title(tool_name)
    st.info(tool_description)
    url = st.text_input("Enter URL to analyze")
    run = st.button("Run Analysis")
    if url and run:
        return url
    return None