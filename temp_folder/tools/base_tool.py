"""
tools/base_tool.py

Abstract base class for all SEO tools.
"""

from abc import ABC, abstractmethod

class BaseTool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, url: str) -> dict:
        """
        Execute the tool's logic on a given URL.

        Args:
            url: The URL of the page to analyze.

        Returns:
            A dictionary containing the results of the analysis.
        """
        pass