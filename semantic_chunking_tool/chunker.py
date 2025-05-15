"""
SemanticChunker class: handles chunk extraction using OpenAI and parsing.
"""
import logging
from typing import List, Dict, Any
from .openai_client import OpenAIClient
from .parser import ResponseParser

class SemanticChunker:
    """
    Splits texts into coherent semantic chunks via AI-driven prompts.
    """
    system_message = "You are a helpful assistant that splits texts into meaningful semantic chunks."
    instruction_template = """
You are an expert at text segmentation. 
Given the following text, extract the first meaningful chunk based on topic or semantic shifts.

Rules:
- The chunk should be coherent and self-contained.
- Label the chunk with a title.
- Try to make the chunk around {size} words if possible.
- Output as a JSON object with 'title' and 'content' fields.
- The JSON should be contained within triple backticks (``` or ```json) for easy parsing.
- The output chunk text should be EXACTLY as it is in the input text, without any modifications.

Text to split:
\"\"\"
{text}
\"\"\"
"""

    def __init__(self, client: OpenAIClient, parser: ResponseParser, config, logger: logging.Logger):
        self.client = client
        self.parser = parser
        self.size = config.chunk_size
        self.logger = logger
        self.max_retries = config.max_retries

    def _get_chunk(self, text: str) -> Dict:
        """
        Requests the next chunk from the AI and parses the result.
        """
        prompt = self.instruction_template.format(text=text[:10*self.size], size=self.size)
        raw = self.client.chat(self.system_message, prompt)
        chunk = self.parser.parse(raw, self.logger)
        return chunk

    @staticmethod
    def _locate(text: str, content: str) -> tuple:
        start = text.find(content)
        end = start + len(content) if start >= 0 else -1
        return start, end

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Splits the input text into coherent semantic chunks until fully processed.

        Args:
            text (str): The complete text to segment.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each with:
                - title (str): Semantic label for the chunk.
                - content (str): Extracted chunk text.
                - start (int): Starting index in the original text.
                - end (int): Ending index in the original text.
                - length (int): Number of characters in the chunk.
        """
        self.logger.info("Starting semantic chunking of text (%d chars)", len(text))
        offset = 0
        retries = 0
        remaining = text
        chunks: List[Dict[str, Any]] = []

        while remaining:
            # Check if max retries reached
            if retries >= self.max_retries:
                self.logger.error(f"Max retries reached ({self.max_retries}); stopping chunking.")
                break
            
            # Extract the next chunk via AI
            data = self._get_chunk(remaining)
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()

            if not content:
                self.logger.warning(f"Empty chunk returned; trying again ({retries + 1}/{self.max_retries})")
                retries += 1
                continue

            # Locate content within remaining text
            start_rel = remaining.find(content)
            if start_rel < 0:
                self.logger.error(f"Chunk content not found in remaining text; trying again ({retries + 1}/{self.max_retries})")
                retries += 1
                continue
            
            end_rel = start_rel + len(content)

            # Calculate absolute indices in the original text
            start_idx = offset + start_rel
            end_idx = offset + end_rel

            chunks.append({
                'title': title,
                'content': content,
                'start': start_idx,
                'end': end_idx,
                'length': len(content)
            })
            
            # Log the chunk details
            self.logger.info(f"Extracted chunk: '{title}' (start={start_idx}, end={end_idx}, length={len(content)})")

            # Update offset and remaining text slice
            offset = end_idx
            remaining = text[offset:].lstrip()
            
            # Reset retries after a successful chunk
            retries = 0

        self.logger.info("Completed chunking; extracted %d chunks", len(chunks))
        return chunks

