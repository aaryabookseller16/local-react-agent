# Jarvis

A local ReAct agent built from scratch with Ollama, no agent frameworks.

## Layout

- `jarvis/chat.py` — the client: runs the chat loop, prompts the model, and parses
  its ReAct-style replies (`jarvis/parser.py`). It launches the MCP server as a
  subprocess over stdio, discovers its tools at startup, and calls them through
  an MCP `ClientSession`.
- `jarvis/server.py` — the MCP server exposing the tools.
- `jarvis/tool.py` — the tool implementations (calculator, read_file,
  list_directory, search_files), all sandboxed to the project directory.
- `jarvis/chunker.py` — text chunking (greedy packing / recursive splitting).
- `tests/` — `test_chunker.py` chunker checks and `smoke_client.py`, a standalone
  script that exercises the server directly without the chat loop.

## Usage

Run from the project root:

```
python -m jarvis.chat
python tests/smoke_client.py
python -m tests.test_chunker
```

Work in progress.
