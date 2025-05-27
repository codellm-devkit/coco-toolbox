import inspect
from . import tools  # import the tools.py module inside this package


def iter_tools():
    """
    Yield all functions in tools.py that end with '_tool'.
    """
    for name, obj in inspect.getmembers(tools, inspect.isfunction):
        if name.endswith("_tool"):
            yield obj
