"""
Domain Age Checker Tool

Fetches domain registration date using WHOIS and estimates the domain age.
"""

from tools.base_tool import BaseTool
import datetime

try:
    import whois
except ImportError:
    whois = None

class DomainAgeChecker(BaseTool):
    def __init__(self):
        super().__init__(
            name="Domain Age Checker",
            description="Parses WHOIS to estimate domain age. (Pass domain in URL parameter)"
        )

    def run(self, url: str) -> dict:
        """
        Expects a domain name as the 'url' parameter.
        Returns the domain creation date and estimated age.
        """
        if not whois:
            return {"error": "whois module not installed."}
        try:
            w = whois.whois(url)
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            today = datetime.datetime.utcnow()
            if creation_date:
                age_days = (today - creation_date).days
                age_years = age_days // 365
                message = f"Domain created on {creation_date.strftime('%Y-%m-%d')} ({age_years} year(s) old)."
            else:
                age_days = None
                message = "Could not determine domain creation date."
        except Exception as e:
            return {"error": str(e), "message": "WHOIS lookup failed."}
        return {
            "creation_date": str(creation_date),
            "age_days": age_days,
            "message": message
        }