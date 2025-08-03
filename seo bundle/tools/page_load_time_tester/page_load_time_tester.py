"""
Page Load Time Tester Tool

This tool measures the time it takes to fetch a page using HTTP requests.
It helps you gauge the network load time (not full browser render time) for a given URL.
"""

from tools.base_tool import BaseTool
import time
import requests

class PageLoadTimeTester(BaseTool):
    def __init__(self):
        super().__init__(
            name="Page Load Time Tester",
            description="Measures the HTTP response time to load the web page."
        )

    def run(self, url: str) -> dict:
        """
        Measures how long it takes to fetch the page's HTML content using a GET request.
        Returns the load time in seconds (rounded), status code, and any errors.
        """
        try:
            start_time = time.time()
            response = requests.get(url, timeout=15)
            end_time = time.time()
            load_time = round(end_time - start_time, 3)
            status_code = response.status_code

            return {
                "url": url,
                "status_code": status_code,
                "load_time_seconds": load_time,
                "message": f"Page loaded in {load_time} seconds (HTTP status: {status_code})."
            }

        except requests.exceptions.RequestException as e:
            return {
                "url": url,
                "error": str(e),
                "message": "An error occurred while measuring page load time."
            }