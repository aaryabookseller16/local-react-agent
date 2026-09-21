# Jarvis

A local ReAct agent built from scratch with Ollama, no agent frameworks.

## Layout

- `agent/chat.py` — the client: runs the chat loop, prompts the model, and parses
  its ReAct-style replies (`agent/parser.py`). It launches the MCP server as a
  subprocess over stdio, discovers its tools at startup, and calls them through
  an MCP `ClientSession`.
- `agent/server.py` — the MCP server exposing the tools.
- `agent/tool.py` — the tool implementations (calculator, read_file,
  list_directory, search_files), all sandboxed to the project directory.
- `agent/chunker.py` — text chunking (greedy packing / recursive splitting).
- `tests/` — `test_chunker.py` chunker checks and `smoke_client.py`, a standalone
  script that exercises the server directly without the chat loop.

## Usage

Run from the project root:

```
python -m agent.chat
python tests/smoke_client.py
python -m tests.test_chunker
```

Work in progress.
