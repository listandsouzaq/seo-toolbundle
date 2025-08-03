"""
Page Status Code Checker Tool

Checks and returns the HTTP status code for the provided URL.
"""

from tools.base_tool import BaseTool
from core.utils import fetch_url

class PageStatusCodeChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Page Status Code Checker",
            description="Checks the HTTP status code for a given URL."
        )

    def run(self, url: str) -> dict:
        """
        Fetches the URL and returns the status code and a message.
        """
        response = fetch_url(url)
        status_code = getattr(response, "status_code", None)
        if status_code:
            message = f"Status code: {status_code}"
        else:
            message = "Could not fetch the status code."
        return {
            "url": url,
            "status_code": status_code,
            "message": message
        }