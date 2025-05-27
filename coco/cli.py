import os
import typer
from pathlib import Path
from typing import *
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from cldk import CLDK
from fastmcp import FastMCP, Context
from cldk.analysis.java import JavaAnalysis
from coco.utils.session_manager import SessionManager
from fastmcp.server.dependencies import get_context


@dataclass
class CoCoConfig:
    """
    Configuration for the CoCo MCP server.
    """

    analysis: JavaAnalysis | None


@asynccontextmanager
async def coco_lifespan(server: FastMCP) -> AsyncIterator[CLDK]:
    """
    Context manager to start the CoCo MCP server.
    """
    yield CoCoConfig(analysis=analysis)


mcp = FastMCP(name="coco", lifespan=coco_lifespan, description="Code Context (CoCo) Toolbox: Static code analysis toolbox as an MCP server")

# The main entry point for the CLI application
app = typer.Typer(
    name="coco",
    help="Code Context (CoCo) Toolbox: Static code analysis toolbox as an MCP server",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)


@mcp.tool()
async def test_tool(ctx: Context):
    """
    Get the context for the CoCo MCP server.
    """
    context = await get_context(ctx)
    analysis = context.request_context.lifespan_context["analysis"]
    return analysis.project_path


@app.callback()
def main():
    """
    [bold blue]Code Context Toolbox[/bold blue] - MCP server for static code analysis.

    Start the server with: [cyan]coco serve[/cyan]
    """
    pass


@app.command()
def serve(
    project_path: Annotated[Path, typer.Argument("-p", "--project-path", help="Path to the project directory")],
):
    """
    Start the CoCo MCP server.
    """
    global analysis
    analysis = CLDK("java").analysis(project_path=project_path)


if __name__ == "__main__":
    app()
