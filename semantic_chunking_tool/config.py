"""
Configuration and logging setup for the semantic chunking tool.
"""
import os
import logging
from dotenv import load_dotenv

class Config:
    """
    Application configuration loaded from environment.
    Attributes:
        api_key: OpenAI API key
        model_id: Default model identifier
        chunk_size: Number of words per chunk
    """
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model_id = os.getenv('MODEL_ID', 'gpt-4.1-mini')
        self.chunk_size = int(os.getenv('CHUNK_SIZE', 300))
        self.max_retries = int(os.getenv('MAX_RETRIES', 5))


def setup_logging() -> logging.Logger:
    """
    Configures and returns a logger instance based on LOG_LEVEL env var.
    """
    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, log_level_str, logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    return logging.getLogger('semantic_chunker')
