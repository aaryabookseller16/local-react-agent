import asyncio          # runs the async code (the event loop + asyncio.run)
import sys              # gives us sys.executable, the path to the current Python

import ollama           # talks to the local model
from mcp import ClientSession, StdioServerParameters, stdio_client  # the MCP client pieces

from jarvis.parser import parse_input

MODEL = "llama3.1:8b"

# The fixed part of the system prompt: HOW to reply. This is scaffolding, not tool
# info, so it is hardcoded. The tool list itself is added dynamically below.
FORMAT_RULES = """
Respond in EXACTLY this format if you use a tool, then wait for the tool's answer.
Thought: <your reasoning about what to do next>
Action: <the exact name of one tool from the list above>
Action Input: <the single input to that tool>

When you have the final answer, respond in EXACTLY this format:
Thought: <your reasoning>
Final Answer: <your answer>

Produce only ONE Thought and ONE Action, then stop. Do NOT write an Observation yourself; it will be provided to you.

If the message does not need a tool, such as a greeting or small talk, skip the Action and reply directly using the Thought/Final Answer format.
"""


def build_system_prompt(tools):
    # Build the tool menu from what the server reported, instead of typing it by hand.
    # Each tool contributes one line: its name and the description from its docstring.
    lines = ["You are an agent that solves problems step by step using tools.", "", "Available tools:"]
    for t in tools:
        lines.append(f"- {t.name}: {t.description}")
    # Menu on top, then the format rules underneath.
    return "\n".join(lines) + "\n" + FORMAT_RULES


async def main():
    # Recipe for starting the server: run "python -m jarvis.server" with THIS same Python,
    # so the subprocess uses your venv. Nothing launches yet; this is just the plan.
    server_params = StdioServerParameters(command=sys.executable, args=["-m", "jarvis.server"])

    # stdio_client launches the server as a subprocess and hands back the two pipe ends.
    # async with keeps the ONE server alive for the whole chat and cleans it up on exit.
    async with stdio_client(server_params) as (read, write):
        # Wrap the raw pipe in a session so we can speak in tools, not bytes.
        async with ClientSession(read, write) as session:
            # Handshake. Must happen before any other call.
            await session.initialize()

            # Ask the server what tools exist. .tools is the list of tool definitions.
            tool_list = (await session.list_tools()).tools

            # For each tool, find the name of its single parameter by reading its input
            # schema (the schema the decorator built from the type hints). Example:
            # calculator -> "expression", read_file -> "requested_path".
            # We need this to turn the model's one Action Input string into the dict
            # that call_tool expects, without hardcoding a name-to-parameter table.
            param_name = {t.name: next(iter(t.input_schema["properties"])) for t in tool_list}

            # The set of tool names the server actually offers, used to validate the
            # model's chosen Action below.
            valid_tools = set(param_name)

            # Seed the conversation with the system prompt built from the live tool list.
            messages = [{"role": "system", "content": build_system_prompt(tool_list)}]

            # Main chat loop: one pass per user question.
            while True:
                user = input("> ")
                messages.append({"role": "user", "content": user})

                # Ask the model. This is where the model decides: use a tool, or answer.
                # It is a normal blocking call (the ollama library is synchronous).
                resp = ollama.chat(model=MODEL, messages=messages, options={"temperature": 0})
                reply = resp["message"]["content"]
                reply_tuple = parse_input(reply)   # ("final", answer) or ("action", name, input)

                retries = 3        # how many malformed replies we tolerate before giving up
                failed = False

                # Keep looping as long as the model wants a tool (not a final answer).
                while reply_tuple[0] != "final":
                    # Record the model's tool-asking reply in the history.
                    messages.append({"role": "assistant", "content": reply})

                    tool_name = reply_tuple[1]
                    tool_input = reply_tuple[2]

                    if tool_name in valid_tools and tool_input is not None:
                        # Valid tool + input: build the arguments dict keyed by the
                        # tool's real parameter name, then run it ON THE SERVER.
                        # This await waits for the server to execute the tool, not the model.
                        arguments = {param_name[tool_name]: tool_input}
                        result = await session.call_tool(tool_name, arguments)
                        # The tool's text output is the first content block's text.
                        observation = result.content[0].text
                    else:
                        # Something was wrong with the model's reply. Figure out which
                        # failure it was and build a correction to send back as feedback.
                        if tool_name is None and tool_input is None:
                            # Neither an Action nor a Final Answer: reply was off-format.
                            correction = (
                                "Error: your reply had no 'Action:' line and no 'Final Answer:' line. "
                                "Respond in EXACTLY one of the two formats: "
                                "'Thought:/Action:/Action Input:' to use a tool, or "
                                "'Thought:/Final Answer:' when you are done."
                            )
                        elif tool_name not in valid_tools:
                            # It named a tool that does not exist.
                            correction = (
                                f"Error: '{tool_name}' is not a valid tool. "
                                f"Available tools: {sorted(valid_tools)}."
                            )
                        else:
                            # It gave an Action but forgot the Action Input line.
                            correction = "Error: you emitted an Action but no 'Action Input:' line. Include it."

                        # Out of retries: stop trying to salvage this turn.
                        if retries == 0:
                            print("Failed: the model couldn't produce a valid tool call.")
                            failed = True
                            break
                        # Otherwise, the correction becomes the observation and we spend a retry.
                        observation = correction
                        retries -= 1

                    # Feed the observation (tool result OR correction) back to the model
                    # so it can decide the next step with the new information.
                    messages.append({"role": "user", "content": f"Observation: {observation}"})

                    # Ask the model again, now that it has seen the observation.
                    resp = ollama.chat(model=MODEL, messages=messages, options={"temperature": 0})
                    reply = resp["message"]["content"]
                    reply_tuple = parse_input(reply)

                # Loop ended because the model gave a Final Answer (and we did not fail).
                if not failed:
                    print(reply)
                    messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    # Kick off the whole async chain. main() alone would only create a coroutine;
    # asyncio.run actually drives it to completion.
    asyncio.run(main())
