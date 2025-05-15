"""
Wrapper around OpenAI ChatCompletion API calls.
"""
import logging
from openai import OpenAI
from .config import Config

class OpenAIClient:
    """
    Client for interacting with OpenAI's Chat API.
    """
    def __init__(self, config: Config, logger: logging.Logger):
        self._client = OpenAI(api_key=config.api_key)
        self._model = config.model_id
        self._logger = logger

    def chat(self, system: str, prompt: str, temperature: float = 0.2) -> str:
        """
        Sends a chat completion request and returns the content.
        """
        self._logger.info(f"Calling model {self._model}")
        self._logger.debug(f"System message: {system}")
        self._logger.debug(f"User prompt: {prompt}")
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system",  "content": system},
                {"role": "user",    "content": prompt}
            ],
            temperature=temperature
        )
        content = response.choices[0].message.content
        self._logger.debug(f"Model response: {content}")
        return content
