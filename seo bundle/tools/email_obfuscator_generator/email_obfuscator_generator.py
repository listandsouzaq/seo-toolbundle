"""
Email Obfuscator Generator Tool

Generates an obfuscated version of an email address (expects email in URL parameter).
"""

from tools.base_tool import BaseTool

class EmailObfuscatorGenerator(BaseTool):
    def __init__(self):
        super().__init__(
            name="Email Obfuscator Generator",
            description="Generates obfuscated email (expects email in URL parameter)."
        )

    def run(self, url: str) -> dict:
        """
        Expects an email address in the 'url' parameter.
        Returns an obfuscated email string.
        """
        email = url.strip()
        # Simple obfuscation: replace @ with [at], . with [dot]
        obfuscated = email.replace("@", " [at] ").replace(".", " [dot] ")
        # Basic HTML entity obfuscation
        html_obfuscated = "".join(f"&#{ord(c)};" for c in email)
        return {
            "original_email": email,
            "obfuscated_text": obfuscated,
            "obfuscated_html": html_obfuscated,
            "message": "Email obfuscated."
        }