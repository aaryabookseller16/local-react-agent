from mcp.server import MCPServer
from jarvis.tool import calculator as _calculator, read_file as _read_file, list_directory as _list_directory, search_files as _search_files

mcp = MCPServer("jarvis-tools")

@mcp.tool()
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression, for example '47 * 89' or '(3 + 4) * 2'. Use this for any math."""
    return str(_calculator(expression))

@mcp.tool()
def read_file(requested_path: str) -> str:
    """Read a text file inside the project directory. Pass a path relative to the project, for example 'README.md'."""
    return _read_file(requested_path)

@mcp.tool()
def list_directory(path: str = ".") -> str:
    """List files and folders inside the project directory. Pass a path relative to the project, or '.' for the project root. Returns type, size, and name per entry."""
    return _list_directory(path)

@mcp.tool()
def search_files(pattern: str) -> str:
    """Find files by name or glob pattern (for example '*.py' or 'READ*') recursively inside the project directory. Returns matching paths relative to the project."""
    return _search_files(pattern)


if __name__ == "__main__":
    mcp.run(transport="stdio")
