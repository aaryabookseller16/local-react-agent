import ollama
from parser import parse_input
from tool import calculator

MODEL = "llama3.1:8b"
TOOLS = {"calculator": calculator}

SYSTEM_PROMPT = """
You are an agent that solves problems step by step using tools.

Respond in EXACTLY this format if you use the tool, and then wait for the tool's answer.
Thought: <your reasoning about what to do next>
Action: calculator
Action Input: <the input to the tool>

When you have the final answer, respond in EXACTLY this format:
Thought: <your reasoning>
Final Answer: <your answer>
Produce only ONE Thought and ONE Action, then stop. Do NOT write an Observation yourself — it will be provided to you.


For example:
If a user asks "what is 5*6?". Your response should be:
Thought: To calculate multiplcation.
Action: calculator
Action Input: 5*6

"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    user = input("> ")
    messages.append({"role": "user", "content": user})

    resp = ollama.chat(model=MODEL, messages=messages, options={"temperature": 0})
    reply = resp["message"]["content"]
    reply_tuple = parse_input(reply)

    retries = 3
    failed = False

    while reply_tuple[0] != "final":  # keep calling model until we have final answer
        # update action with observation so that the model can determine if it needs to stop or keep going (updated info)
        messages.append({"role": "assistant", "content": reply})

        tool_name = reply_tuple[1]
        tool_input = reply_tuple[2]

        if tool_name in TOOLS and tool_input is not None:
            # can also write: observation = TOOLS[tool_name](tool_input)
            func = TOOLS[tool_name]
            observation = func(tool_input)
        else:
            # figure out WHICH failure, build the right correction
            if tool_name is None and tool_input is None:
                # neither an Action nor a Final Answer — the reply is off-format entirely
                correction = (
                    "Error: your reply had no 'Action:' line and no 'Final Answer:' line. "
                    "Respond in EXACTLY one of the two formats: "
                    "'Thought:/Action:/Action Input:' to use a tool, or "
                    "'Thought:/Final Answer:' when you are done."
                )
            elif tool_name not in TOOLS:
                correction = (
                    f"Error: '{tool_name}' is not a valid tool. "
                    f"Available tools: {list(TOOLS.keys())}."
                )
            else:  # tool_name is fine, so the problem must be the missing input
                correction = "Error: you emitted an Action but no 'Action Input:' line. Include it."

            if retries == 0:
                print("Failed: the model couldn't produce a valid tool call.")
                failed = True
                break
            else:
                observation = correction
                retries -= 1

        messages.append({"role": "user", "content": f"Observation: {observation}"})

        # call model again with updated Observation
        resp = ollama.chat(model=MODEL, messages=messages, options={"temperature": 0})
        reply = resp["message"]["content"]
        reply_tuple = parse_input(reply)

    if not failed:
        print(reply)
        messages.append({"role": "assistant", "content": reply})
