import inspect
from . import tools  # import the tools.py module inside this package
from . import schema_explainer


def iter_tools():
    """
    Yield all functions in tools.py that end with '_tool'.
    """
    for name, obj in inspect.getmembers(tools, inspect.isfunction):
        if name.endswith("_tool"):
            yield obj


def iter_explainers():
    """
    Yield all functions in tools.py that end with '_explainer'.
    """
    for name, obj in inspect.getmembers(schema_explainer, inspect.isfunction):
        if name.endswith("_explainer"):
            yield obj
