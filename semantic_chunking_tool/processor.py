"""
TextProcessor: this module contains the Processor class, which is responsible for preprocessing text.
"""
import re

class TextProcessor:
    """
    Preprocesses input text by removing unnecessary repeated newlines and trailing spaces.
    """

    def clean_text(self, text: str) -> str:
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n\s*\n+', '\n', text)
        # Remove trailing spaces from each line
        text = '\n'.join(line.rstrip() for line in text.splitlines())
        return text