import ollama
from parser import parse_input
from tool import calculator

messages = [{"role": "system", "content":
 """
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

"""}]

TOOLS = {"calculator": calculator}
while True:
    user = input("> ")
    messages.append({"role": "user", "content": user})
    resp = ollama.chat(model="llama3.1:8b", messages=messages, options={"temperature": 0})
    reply = resp["message"]["content"]
    reply_tuple = parse_input(reply)

    while reply_tuple[0] != "final": #keep calling model until we have final answer
        # update action with observation so that the model can determine if it needs to stop or keep going (updated info)
        messages.append({"role": "assistant", "content": reply})

        tool_name = reply_tuple[1]
        tool_input = reply_tuple[2]
        # can also write: observation = TOOLS[tool_name](tool_input)
        func = TOOLS[tool_name]
        observation = func(tool_input)

        messages.append({"role": "user", "content": f"Observation: {observation}"})

        # call model again with updated Observation
        resp = ollama.chat(model="llama3.1:8b", messages=messages, options={"temperature": 0})
        reply = resp["message"]["content"]
        reply_tuple =  parse_input(reply)


       
    print(reply)
    messages.append({"role": "assistant", "content": reply})