# OpenAI Client Integration

A Python client for interacting with OpenAI's API with support for both standard chat and MCP (Model Context Protocol) functionality.

## Features

- **Standard Chat**: Interactive chat with Gen Alpha personality
- **MCP Integration**: Chat with Model Context Protocol tools for repository assistance
- **Streaming Support**: Real-time response streaming
- **Session Management**: Maintains conversation history across interactions

## Requirements

- Python 3.13+
- OpenAI API key

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### OpenAI Client
Run the interactive chat application:
```bash
python llms/openai_client.py
```

Select from the menu:
- **1. Chat**: Standard chat with Gen Alpha personality
- **2. MCP**: Chat with repository assistance tools
- **Press any other key**: Exit the application

Use `/exit` to end the current chat session.

### Generate Embeddings
Generate embeddings for the IMDB dataset:
```bash
python llms/generate_embeddings.py
```

This will read the IMDB CSV data, create embeddings for each movie, and save them to a SQLite database.

### Semantic Search
Search through movies using semantic similarity:
```bash
python llms/semantic_search.py
```

Enter search queries to find movies based on semantic similarity. Use `/exit` to quit the search interface.

## Configuration

- **Model**: `gpt-4.1-mini-2025-04-14`
- **Chat Temperature**: 1.0 (creative)
- **MCP Temperature**: 0.5 (focused)
- **MCP Server**: `https://gitmcp.io/dcos/shakedown`

## Functions

- `chat()`: Standard OpenAI chat functionality
- `mcp_chat()`: Chat with MCP tools integration
- `handle_response()`: Process both streaming and non-streaming responses
- `handle_streaming_events()`: Real-time event processing