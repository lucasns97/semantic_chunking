# Semantic Chunking Tool

A Python tool for splitting large texts into coherent, meaningful semantic chunks using OpenAI's language models.

## Features

- Automatically segments long texts into topic-based chunks.
- Each chunk is labeled with a title and includes its position in the original text.
- Outputs results as a structured JSON file.

## Installation

1. **Clone the repository**  
   ```sh
   git clone https://github.com/lucasns97/semantic_chunking.git
   cd semantic-chunking-tool
   ```

2. **Create a virtual environment (optional but recommended)**  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**  
   - Copy `.env_copy` to `.env`:
     ```sh
     cp .env_copy .env
     ```
   - Edit `.env` and set your actual OpenAI API key:
     ```
     OPENAI_API_KEY="your_openai_api_key_here"
     ```

## Usage

1. **Prepare your input text**  
   Place your text in a file, e.g., `example/input.txt`.

2. **Run the chunking tool**  
   ```sh
   python -m semantic_chunking_tool.main example/input.txt --output example/output.json
   ```

   - `example/input.txt`: Path to your input text file.
   - `--output example/output.json`: (Optional) Path to save the output JSON file. Defaults to `output.json`.

3. **View the results**  
   The output will be a JSON file containing an array of chunks, each with a title, content, and position info.

## Example

Input:  
[example/input.txt](example/input.txt)

Visual example of the input text:
```
This is the introduction to the text. It provides an overview of the main topics that will be discussed in detail later on.
```

Output:  
[example/output.json](example/output.json)

Visual example of the output JSON:
```json
[
    {
        "title": "Introduction",
        "content": "This is the introduction to the text.",
        "start": 0,
        "end": 37,
        "length": 37
    },
    {
        "title": "Main Topic",
        "content": "It provides an overview of the main topics that will be discussed in detail later on.",
        "start": 38,
        "end": 156,
        "length": 85
    }
]
```

## Configuration

You can adjust chunk size, model, and other settings in the `.env` file:

```
OPENAI_API_KEY="your_openai_api_key_here" # Your OpenAI API key
LOG_LEVEL="INFO" # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
CHUNK_SIZE="300" # Approximate size of each chunk in 'words'
MODEL_ID="gpt-4.1-mini" # OpenAI model to use
MAX_RETRIES="5" # Maximum number of retries for API calls for each chunk
```

## License

MIT License

---

**Note:** Requires an OpenAI API key. See [OpenAI API documentation](https://platform.openai.com/docs/api-reference) for more details.
