import typer
from typing import *
from cldk import CLDK
from pathlib import Path
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from cldk.analysis.java import JavaAnalysis
from fastmcp import FastMCP, Context


@dataclass
class CLDKAnalysis:
    """
    Data class to hold the CLDK analysis instance.
    """

    project_path: Path
    analysis_instance: JavaAnalysis | None = field(default=None, init=False)

    def __post_init__(self):
        typer.echo(f"Analysis initialized for project at: {self.project_path}")
        self.analysis_instance = CLDK("java").analysis(project_path=str(self.project_path))


def create_lifespan(project_path: Path):
    @asynccontextmanager
    async def coco_lifespan(server: FastMCP) -> AsyncIterator[CLDKAnalysis]:
        """
        Context manager to start the CoCo MCP server.
        """
        yield CLDKAnalysis(project_path=project_path)

    return coco_lifespan


# The main entry point for the CLI application
app = typer.Typer(
    name="coco",
    help="Code Context (CoCo) Toolbox: Static code analysis toolbox as an MCP server",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)


@app.callback()
def main():
    """
    [bold blue]Code Context Toolbox[/bold blue] - MCP server for static code analysis.

    Start the server with: [cyan]coco serve[/cyan]
    """
    pass


@app.command()
def serve(
    project_path: Annotated[Path, typer.Option("-p", "--project-path", help="Path to the project directory")],
):
    """
    Start the CoCo MCP server.
    """
    # Create MCP instance with project-specific lifespan
    mcp = FastMCP(name="coco", lifespan=create_lifespan(project_path), description="Code Context (CoCo) Toolbox: Static code analysis toolbox as an MCP server")

    # Register tools
    @mcp.tool()
    async def test_tool(ctx: Context):
        """
        Get the context for the CoCo MCP server.
        """
        analysis = ctx.request_context.lifespan_context.analysis_instance
        return str(analysis.project_dir)

    mcp.run()


if __name__ == "__main__":
    app()
