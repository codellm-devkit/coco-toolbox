from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="cocoa",  # Executable
    args=["toolbox", "--project-path", "/Users/rkrsn/workspace/codeanalyzer-test-projects/sample.daytrader8"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            result = await session.call_tool("are_we_ready_tool", arguments={})
            print(result.content[0].text)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
