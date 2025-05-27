from pathlib import Path
import sys

from mcp import StdioServerParameters
import pytest


@pytest.fixture(scope="session")
def project_path():
    """Fixture to provide the path to the project directory."""
    return Path(__file__).parent / "resources" / "daytrader8"


@pytest.fixture
def coco_server_params(project_path):
    """Create server parameters using Python module execution."""
    return StdioServerParameters(
        command=sys.executable,  # Use current Python interpreter
        args=["-m", "coco.cli", "serve", "--project-path", str(project_path)],
        env=None,
    )
