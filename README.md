# Jarvis

A local ReAct agent built from scratch with Ollama, no agent frameworks.

`chat.py` is the client: it runs the chat loop, prompts the model, and parses
its ReAct-style replies. Tools live behind an MCP server (`server.py`) instead
of being called in-process — the client launches the server as a subprocess
over stdio, discovers its tools at startup, and calls them through an MCP
`ClientSession`. `tool.py` holds the actual tool implementations (calculator,
read_file, list_directory, search_files), all sandboxed to the project
directory. `client_test.py` is a standalone script for exercising the server
directly, without the chat loop.

Work in progress
