"""
Configuration and logging setup for the semantic chunking tool.
"""
import os
import logging
from dotenv import load_dotenv
from colorlog import ColoredFormatter

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
    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, log_level_str, logging.INFO)

    formatter = ColoredFormatter(
        '%(log_color)s%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('semantic_chunker')
    logger.setLevel(level)
    logger.handlers = []  # remove old handlers
    logger.addHandler(handler)
    return logger

def log_progress(logger: logging.Logger, percent_done: float, bar_length: int = 40):
    """
    Logs progress messages with a specific format.
    """
    filled_length = int(bar_length * percent_done // 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    logger.info(f"[{bar}] {percent_done:.2f}% done")
