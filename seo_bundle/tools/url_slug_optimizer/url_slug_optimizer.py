"""
URL Slug Optimizer Tool

This tool analyzes the URL slug (the path part of the URL) for SEO best practices, such as
length, use of hyphens, presence of stopwords, and lowercasing. It provides recommendations
for optimization.
"""

from tools.base_tool import BaseTool
from urllib.parse import urlparse, unquote
import re

class URLSlugOptimizer(BaseTool):
    def __init__(self):
        super().__init__(
            name="URL Slug Optimizer",
            description="Analyzes and suggests improvements for URL slugs for better SEO."
        )

    def run(self, url: str) -> dict:
        """
        Parse the URL and analyze its slug (path).
        Returns a dict with the slug, issues found, and recommendations.
        """
        # Parse and decode the URL
        parsed = urlparse(url)
        slug = unquote(parsed.path.strip("/"))
        issues = []
        recommendations = []
        
        # Check for empty slug
        if not slug:
            issues.append("URL does not have a slug (just the domain/root).")
            recommendations.append("Add a descriptive, keyword-rich slug to the URL.")
            return {
                "slug": "/",
                "issues": issues,
                "recommendations": recommendations,
                "message": "No slug found in the URL."
            }

        # Check for spaces and replaceable characters
        if " " in slug or "_" in slug:
            issues.append("Slug contains spaces or underscores.")
            recommendations.append("Use hyphens '-' instead of spaces or underscores.")
        
        # Check for uppercase
        if any(x.isupper() for x in slug):
            issues.append("Slug contains uppercase letters.")
            recommendations.append("Convert all characters in the slug to lowercase.")

        # Check for length
        if len(slug) > 60:
            issues.append("Slug is too long.")
            recommendations.append("Shorten the slug to under 60 characters if possible.")

        # Check for stopwords (basic list)
        stopwords = {"the", "and", "or", "a", "an", "of", "to", "in", "for", "on", "at", "with", "from", "by"}
        words = re.split(r"[-_/]", slug)
        found_stopwords = [w for w in words if w.lower() in stopwords]
        if found_stopwords:
            issues.append(f"Slug contains common stopwords: {', '.join(set(found_stopwords))}.")
            recommendations.append("Remove unnecessary stopwords to make the slug more concise.")

        # Check for non-alphanumeric characters (besides hyphen)
        if re.search(r"[^a-z0-9\-\/]", slug.lower()):
            issues.append("Slug contains special characters.")
            recommendations.append("Remove special characters, use only letters, numbers, and hyphens.")

        # General recommendation
        if "-" not in slug:
            recommendations.append("Use hyphens '-' to separate words in the slug (SEO best practice).")

        # Compose message
        if not issues:
            message = "Slug follows most SEO best practices."
        else:
            message = "Slug has some optimization issues. See recommendations."

        return {
            "slug": slug,
            "issues": issues,
            "recommendations": recommendations,
            "message": message
        }