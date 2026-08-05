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
 
