def parse_input(reply : str):
    # dont bother with the str if it contains the final answer
    if "Final Answer:" in reply:
        answer = reply.split("Final Answer:")[1].strip()
        return ("final", answer)

    lines = reply.splitlines()
    tool = None
    tool_input = None

    for line in lines:
        if line.startswith("Action:"):
            tool = line.split("Action:")[1].strip()
        if line.startswith("Action Input:"):
            tool_input = line.split("Action Input:")[1].strip()

    return ("action", tool, tool_input)

# print(parse_input("Thought: I multiply.\nAction: calculator\nAction Input: 47 * 89"))
# print(parse_input("Thought: Done.\nFinal Answer: 66"))