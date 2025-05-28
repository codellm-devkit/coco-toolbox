from pathlib import Path
import pytest
from mcp import ClientSession
from mcp.client.stdio import stdio_client


class TestBasicCocoMCPServer:
    """Test basic functionality of the CoCo MCP server."""

    @pytest.mark.asyncio
    async def test_list_tools(self, coco_server_params, project_path):
        """Should invoke the tool and return the list of available tools."""
        async with stdio_client(coco_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                result = await session.list_tools()
                assert len(result.tools) == 53, f"Expected 53 tools, got {len(result.tools)}"
