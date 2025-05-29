import typer
from typing import *
from cldk import CLDK
from pathlib import Path
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from cldk.analysis.java import JavaAnalysis
from fastmcp import FastMCP

from cocoa.tools import iter_explainers, iter_tools


@dataclass
class CLDKAnalysis:
    """
    Data class to hold the CLDK analysis instance.
    """

    project_path: Path
    analysis_instance: JavaAnalysis | None = field(default=None, init=False)

    def __post_init__(self):
        self.analysis_instance = CLDK("java").analysis(project_path=str(self.project_path))


def create_lifespan(project_path: Path):
    @asynccontextmanager
    async def coco_lifespan(server: FastMCP) -> AsyncIterator[CLDKAnalysis]:
        """
        Context manager to start the cocoa MCP server.
        """
        yield CLDKAnalysis(project_path=project_path)

    return coco_lifespan


# The main entry point for the CLI application
app = typer.Typer(
    name="cocoa",
    help="Code Context (cocoa) Toolbox: Static code analysis toolbox as an MCP server",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)


@app.callback()
def main():
    """
    Code Context Toolbox: MCP server for static code analysis.

    Start the server with: cocoa serve --project-path <path_to_project>
    """
    pass


@app.command()
def toolbox(
    project_path: Annotated[Path, typer.Option("-p", "--project-path", help="Path to the project directory")],
):
    """
    Start the cocoa MCP server.
    """
    # Create MCP instance with project-specific lifespan
    mcp = FastMCP(name="cocoa", lifespan=create_lifespan(project_path), description="Code Context Agent (CoCoA) Toolbox as an MCP server")

    # Register tools
    for tool in iter_tools():
        mcp.add_tool(tool)

    # Register explainers
    for explainer in iter_explainers():
        mcp.add_tool(explainer)

    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    app()
