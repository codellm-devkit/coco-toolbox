from pathlib import Path
import pytest
from mcp import ClientSession
from mcp.client.stdio import stdio_client


class TestBasicCocoMCPServer:
    """Test basic functionality of the CoCo MCP server."""

    @pytest.mark.asyncio
    async def test_init_tool(self, coco_server_params, project_path):
        """Should invoke the tool and return the correct project path."""
        async with stdio_client(coco_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                result = await session.call_tool("are_we_ready_tool", arguments={})
                assert result.content[0].text == str(project_path), "Project path does not match expected value"
                assert Path(result.content[0].text).exists(), "Project path should exist"
