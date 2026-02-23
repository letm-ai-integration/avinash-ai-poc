import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    load_dotenv()

    config = {
        "mcpServers": {
            "weather": {
                "command": "uv",
                "args": [
                    "--directory",
                    "C:\\LETM\\1st Week-RAG_Introduction\\mcp_server",
                    "run",
                    "weather.py"
                ]
            },
            "airbnb": {
                "command": "npx",
                "args": ["-y", "@openbnb/mcp-server-airbnb"]
            }
        }
    }

    client = MCPClient.from_dict(config)

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        streaming=True
    )

    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    result = await agent.run(
    "what is the weather in NY")
    # result = await agent.run(
    # "Find Airbnb listings in Barcelona, Spain from March 10 2026 to March 15 2026 for 2 adults")
    print(f"\nResult:\n{result}")

    # ✅ Give subprocess time to shutdown cleanly
    await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
