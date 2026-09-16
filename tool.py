"""Calculator tool for the ReAct agent.
 
Safely evaluates arithmetic expression strings (e.g. "47 * 89", "(3 + 4) * 2")
WITHOUT using eval(). It parses the string into an AST and walks it, permitting
only arithmetic node types. Anything else — function calls, names, attribute
access, imports — raises ValueError instead of executing.
 
This replaces the earlier `return eval(action_input)` placeholder, which would
run arbitrary Python from the model's output.
"""
 
import ast
import operator
from pathlib import Path
 
# Allowed binary operators: AST node type -> function that performs it.
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
 
# Allowed unary operators (e.g. the minus in -5).
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
 
 
def _eval_node(node):
    """Recursively evaluate a single AST node, allowing only arithmetic."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
 
    # A literal number, e.g. 47 or 3.14
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")
 
    # A binary operation, e.g. 47 * 89
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _BIN_OPS[op_type](left, right)
 
    # A unary operation, e.g. -5
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPS[op_type](_eval_node(node.operand))
 
    # Anything else (Name, Call, Attribute, etc.) is rejected.
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")
 
 
def calculator(action_input):
    """Evaluate an arithmetic expression string and return the numeric result.
 
    Returns a string on error so the agent loop can feed it back to the model
    as an Observation instead of crashing.
    """
    try:
        tree = ast.parse(action_input, mode="eval")
        return _eval_node(tree)
    except (ValueError, SyntaxError, TypeError, ZeroDivisionError) as e:
        return f"Error: could not evaluate {action_input!r} ({e})"
 
def read_file(requested_path):
    # 1. allowed dir as a resolved Path
    ALLOWED_DIRECTORY = Path(__file__).parent.resolve()

    # 2. join with requested_path, resolve it
    try:
        full_path =  ALLOWED_DIRECTORY / Path(requested_path)
        file = full_path.resolve()
    except (TypeError, ValueError, OSError, RuntimeError):
        return f"Please submit a file inside {ALLOWED_DIRECTORY}"

    # 3. if file is NOT inside allowed dir -> return a refusal string
    if not file.is_relative_to(ALLOWED_DIRECTORY):
        return f"Please submit a file inside {ALLOWED_DIRECTORY}"

    # 4. if it doesn't exist or isn't a regular file -> return a "not found" string
    try:
        if not file.is_file():
            return f"This file does not exist in {ALLOWED_DIRECTORY}"
    except OSError:
        return f"This file does not exist in {ALLOWED_DIRECTORY}"
     # 5. else: read the text and return it, inside try/except so a
     # permission or decode error returns a message instead of crashing
    else:
        try:
            llm_input = file.read_text()
            return llm_input
        except PermissionError:
            return "no permission to read that file"
        except UnicodeDecodeError:
            return "that file isn't readable"
        except OSError:
            return "that file isn't readable"

    return ""

if __name__ == "__main__":
    print(read_file("todo.txt"))
    print(read_file("../secrets.txt"))
    print(read_file("/etc/passwd"))
    print(read_file("does_not_exist.txt"))