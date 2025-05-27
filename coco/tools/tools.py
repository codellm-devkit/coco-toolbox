from fastmcp import Context


async def are_we_ready_tool(ctx: Context):
    """
    Get the context for the CoCo MCP server.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return str(analysis.project_dir)
