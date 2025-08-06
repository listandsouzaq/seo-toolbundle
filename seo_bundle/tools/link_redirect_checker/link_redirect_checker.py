"""
Link Redirect Checker Tool

Checks if a given URL or its links perform any redirects, and reports the redirect chain.
"""

from tools.base_tool import BaseTool
import requests

class LinkRedirectChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Link Redirect Checker",
            description="Checks if the URL performs redirects and returns the redirect chain."
        )

    def run(self, url: str) -> dict:
        """
        Follows redirects for the given URL and returns the chain.
        """
        try:
            response = requests.get(url, allow_redirects=True, timeout=15)
            history = response.history
            chain = []
            for resp in history:
                chain.append({
                    "url": resp.url,
                    "status_code": resp.status_code
                })
            # Add the final destination
            chain.append({
                "url": response.url,
                "status_code": response.status_code
            })
            message = f"Redirect chain has {len(chain)-1} redirect(s)." if len(chain) > 1 else "No redirects detected."
            return {
                "redirect_chain": chain,
                "message": message
            }
        except Exception as e:
            return {"error": str(e), "message": "Failed to check redirects."}