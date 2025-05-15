"""
Utilities to parse JSON responses from the AI.
"""
import re
import json
import logging

class ResponseParser:
    """
    Parses AI text responses to extract JSON payloads.
    """
    @staticmethod
    def parse(response: str, logger: logging.Logger) -> dict:
        """
        Extracts a JSON object enclosed in triple backticks or treats full text as JSON.
        Returns parsed dict or empty on failure.
        """
        logger.info("Parsing AI response")
        try:
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
            payload = match.group(1) if match else response
            data = json.loads(payload)
            if not isinstance(data, dict):
                raise ValueError("Expected JSON object")
            logger.debug(f"Parsed JSON: {data}")
            return data
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return {}
