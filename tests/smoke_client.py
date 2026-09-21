import asyncio
import sys

from mcp import ClientSession, StdioServerParameters, stdio_client


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,   # same Python as this script, so the venv is used
        args=["-m", "agent.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools the server offers:")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description}")

            calc = await session.call_tool("calculator", {"expression": "47 * 89"})
            print("calculator(47 * 89) ->", calc.content[0].text)

            rf = await session.call_tool("read_file", {"requested_path": "tests/fixtures/todo.txt"})
            print("read_file(todo.txt) ->", rf.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
