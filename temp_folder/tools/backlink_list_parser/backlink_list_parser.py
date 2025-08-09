"""
Backlink List Parser Tool

Parses a CSV of backlinks and provides statistics (for use with uploaded CSVs in Streamlit).
"""

from tools.base_tool import BaseTool
import csv
import io

class BacklinkListParser(BaseTool):
    def __init__(self):
        super().__init__(
            name="Backlink List Parser",
            description="Parses an uploaded CSV of backlinks and analyzes them."
        )

    def run(self, url: str) -> dict:
        """
        Expects CSV content in the 'url' parameter.
        Returns number of backlinks, unique domains, and sample rows.
        """
        csv_content = url
        try:
            reader = csv.DictReader(io.StringIO(csv_content))
            rows = [row for row in reader]
        except Exception as e:
            return {"error": f"Error parsing CSV: {str(e)}"}

        domains = set(row['Domain'] for row in rows if 'Domain' in row)
        sample = rows[:5]
        return {
            "backlink_count": len(rows),
            "unique_domains": len(domains),
            "sample": sample,
            "message": f"Parsed {len(rows)} backlinks from {len(domains)} unique domains."
        }