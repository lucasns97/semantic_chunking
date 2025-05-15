"""
Entry point: parses CLI args, runs chunking, saves output.
"""
import argparse
import json
from .config import Config, setup_logging
from .openai_client import OpenAIClient
from .parser import ResponseParser
from .chunker import SemanticChunker

def main():
    parser = argparse.ArgumentParser(description="Semantic text chunking via OpenAI")
    parser.add_argument('input', help="Path to the input text file")
    parser.add_argument('--output', default='output.json', help="Path to save chunks JSON")
    args = parser.parse_args()

    config = Config()
    logger = setup_logging()

    client = OpenAIClient(config, logger)
    resp_parser = ResponseParser()
    chunker = SemanticChunker(client, resp_parser, config, logger)

    logger.info(f"Reading from {args.input}")
    text = open(args.input, encoding='utf-8').read()
    chunks = chunker.chunk_text(text)

    logger.info(f"Writing {len(chunks)} chunks to {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
