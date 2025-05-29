import json
from fastmcp import Context
import networkx as nx


async def get_application_view_tool(ctx: Context):
    """
    Retrieve a high-level JApplication view of the Java project.

    Includes:
    - `symbol_table` (Dict[str, JCompilationUnit]): All parsed compilation units.
    - `call_graph` (List[JGraphEdges]): Full method call graph.
    - `system_dependency_graph` (List[JGraphEdges]): System-level dependencies.

    Returns:
        str: JSON-encoded JApplication model.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_application_view().model_dump())


async def get_symbol_table_tool(ctx: Context):
    """
    Retrieve the symbol table (Dict[str, JCompilationUnit]) for the project.

    Each JCompilationUnit includes:
    - package name
    - imports
    - type_declarations (Dict[str, JType]) with all classes/interfaces

    Returns:
        str: JSON mapping of file paths to JCompilationUnit models.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({k: v.model_dump() for k, v in analysis.get_symbol_table().items()})


async def get_compilation_units_tool(ctx: Context):
    """
    Get a list of all JCompilationUnit objects.

    Each unit represents a source file, including:
    - file path
    - package name
    - imports
    - type_declarations (Dict[str, JType])

    Returns:
        str: JSON list of JCompilationUnit models.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps([cu.model_dump() for cu in analysis.get_compilation_units()])


async def get_call_graph_tool(ctx: Context):
    """
    Retrieve the call graph as a NetworkX node-link data structure.

    Nodes represent methods; edges are JGraphEdges (source/target JMethodDetail, edge type).

    Returns:
        dict: Node-link JSON graph.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    graph = analysis.get_call_graph()
    return nx.readwrite.json_graph.node_link_data(graph)


async def get_call_graph_json_tool(ctx: Context):
    """
    Retrieve the serialized call graph.

    Returns:
        str: JSON string representing the full call graph.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return analysis.get_call_graph_json()


async def get_callers_tool(ctx: Context, target_class_name: str, target_method_declaration: str, using_symbol_table: bool = True):
    """
    Retrieve the serialized call graph.

    Returns:
        str: JSON dictionary mapping caller details.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_callers(target_class_name, target_method_declaration, using_symbol_table))


async def get_callees_tool(ctx: Context, source_class_name: str, source_method_declaration: str, using_symbol_table: bool = True):
    """
    Get all callees invoked by a specific method.

    Returns:
        str: JSON dictionary mapping callee details.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_callees(source_class_name, source_method_declaration, using_symbol_table))


async def get_methods_tool(ctx: Context):
    """
    Retrieve all methods in the project.

    Returns:
        str: JSON {class_name -> {method_signature -> JCallable}}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({cls: {meth: call.model_dump() for meth, call in methods.items()} for cls, methods in analysis.get_methods().items()})


async def get_classes_tool(ctx: Context):
    """
    Retrieve all JType class/interface models.

    Returns:
        str: JSON {qualified_class_name -> JType}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({cls: typ.model_dump() for cls, typ in analysis.get_classes().items()})


async def get_classes_by_criteria_tool(ctx: Context, inclusions=None, exclusions=None):
    """
    Retrieve classes filtered by inclusion/exclusion.

    Returns:
        str: JSON {qualified_class_name -> JType}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({cls: typ.model_dump() for cls, typ in analysis.get_classes_by_criteria(inclusions, exclusions).items()})


async def get_class_tool(ctx: Context, qualified_class_name: str):
    """
    Retrieve details for a specific JType class.

    Returns:
        str: JSON JType object.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_class(qualified_class_name).model_dump())


async def get_method_tool(ctx: Context, qualified_class_name: str, qualified_method_name: str):
    """
    Retrieve details for a specific JCallable method.

    Returns:
        str: JSON JCallable object.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_method(qualified_class_name, qualified_method_name).model_dump())


async def get_method_parameters_tool(ctx: Context, qualified_class_name: str, qualified_method_name: str):
    """
    Retrieve parameter names for a method.

    Returns:
        str: JSON list of parameter names.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_method_parameters(qualified_class_name, qualified_method_name))


async def get_java_file_tool(ctx: Context, qualified_class_name: str):
    """
    Get the Java file path containing a class.

    Returns:
        str: File path string.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return analysis.get_java_file(qualified_class_name)


async def get_java_compilation_unit_tool(ctx: Context, file_path: str):
    """
    Get the JCompilationUnit for a Java file.

    Returns:
        str: JSON JCompilationUnit object.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_java_compilation_unit(file_path).model_dump())


async def get_methods_in_class_tool(ctx: Context, qualified_class_name: str):
    """
    Get all JCallable methods within a class.

    Returns:
        str: JSON {method_signature -> JCallable}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({meth: call.model_dump() for meth, call in analysis.get_methods_in_class(qualified_class_name).items()})


async def get_constructors_tool(ctx: Context, qualified_class_name: str):
    """
    Get all constructors (JCallable) in a class.

    Returns:
        str: JSON {constructor_signature -> JCallable}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({ctor: call.model_dump() for ctor, call in analysis.get_constructors(qualified_class_name).items()})


async def get_fields_tool(ctx: Context, qualified_class_name: str):
    """
    Get all JField declarations in a class.

    Returns:
        str: JSON list of JField objects.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps([field.model_dump() for field in analysis.get_fields(qualified_class_name)])


async def get_nested_classes_tool(ctx: Context, qualified_class_name: str):
    """
    Get all nested JType classes inside a class.

    Returns:
        str: JSON list of JType objects.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps([typ.model_dump() for typ in analysis.get_nested_classes(qualified_class_name)])


async def get_sub_classes_tool(ctx: Context, qualified_class_name: str):
    """
    Get all subclasses (JType) extending a class.

    Returns:
        str: JSON {subclass_name -> JType}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({cls: typ.model_dump() for cls, typ in analysis.get_sub_classes(qualified_class_name).items()})


async def get_extended_classes_tool(ctx: Context, qualified_class_name: str):
    """
    Get all extended superclasses for a class.

    Returns:
        str: JSON list of class names.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_extended_classes(qualified_class_name))


async def get_implemented_interfaces_tool(ctx: Context, qualified_class_name: str):
    """
    Get all implemented interfaces for a class.

    Returns:
        str: JSON list of interface names.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_implemented_interfaces(qualified_class_name))


async def get_class_call_graph_tool(ctx: Context, qualified_class_name: str, method_signature: str | None = None, using_symbol_table: bool = False):
    """
    Get the method-level call graph edges within a class.

    Each edge is a tuple (JMethodDetail, JMethodDetail).

    Returns:
        str: JSON list of edge tuples.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps([(src.model_dump(), tgt.model_dump()) for src, tgt in analysis.get_class_call_graph(qualified_class_name, method_signature, using_symbol_table)])


async def get_entry_point_classes_tool(ctx: Context):
    """
    Get all entry point classes (JType).

    Returns:
        str: JSON {qualified_class_name -> JType}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({cls: typ.model_dump() for cls, typ in analysis.get_entry_point_classes().items()})


async def get_entry_point_methods_tool(ctx: Context):
    """
    Get all entry point methods (JCallable) across classes.

    Returns:
        str: JSON {class_name -> {method_signature -> JCallable}}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({cls: {meth: call.model_dump() for meth, call in methods.items()} for cls, methods in analysis.get_entry_point_methods().items()})


async def remove_all_comments_tool(ctx: Context):
    """
    Strip all comments from the source code.

    Returns:
        str: Source code without comments.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return analysis.remove_all_comments()


async def get_test_methods_tool(ctx: Context):
    """
    Get all test methods detected in the project.

    Returns:
        str: JSON {method_name -> method_body}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_test_methods())


async def get_all_crud_operations_tool(ctx: Context):
    """
    Get all CRUD operations (JCRUDOperation) across the project.

    Returns:
        str: JSON list [{JType, JCallable, [JCRUDOperation]}].
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_all_crud_operations())


async def get_all_create_operations_tool(ctx: Context):
    """
    Get all CREATE CRUD operations.

    Returns:
        str: JSON list [{JType, JCallable, [JCRUDOperation]}].
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_all_create_operations())


async def get_all_read_operations_tool(ctx: Context):
    """
    Get all READ CRUD operations.

    Returns:
        str: JSON list [{JType, JCallable, [JCRUDOperation]}].
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_all_read_operations())


async def get_all_update_operations_tool(ctx: Context):
    """
    Get all UPDATE CRUD operations.

    Returns:
        str: JSON list [{JType, JCallable, [JCRUDOperation]}].
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_all_update_operations())


async def get_all_delete_operations_tool(ctx: Context):
    """
    Get all DELETE CRUD operations.

    Returns:
        str: JSON list [{JType, JCallable, [JCRUDOperation]}].
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps(analysis.get_all_delete_operations())


async def get_comments_in_a_method_tool(ctx: Context, qualified_class_name: str, method_signature: str):
    """
    Get all JComment objects inside a specific method.

    Returns:
        str: JSON list of JComment models.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps([c.model_dump() for c in analysis.get_comments_in_a_method(qualified_class_name, method_signature)])


async def get_comments_in_a_class_tool(ctx: Context, qualified_class_name: str):
    """
    Get all JComment objects inside a specific class.

    Returns:
        str: JSON list of JComment models.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps([c.model_dump() for c in analysis.get_comments_in_a_class(qualified_class_name)])


async def get_comment_in_file_tool(ctx: Context, file_path: str):
    """
    Get all JComment objects in a file.

    Returns:
        str: JSON list of JComment models.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps([c.model_dump() for c in analysis.get_comment_in_file(file_path)])


async def get_all_comments_tool(ctx: Context):
    """
    Get all comments across the project.

    Returns:
        str: JSON {file_path -> [JComment]}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({fp: [c.model_dump() for c in comments] for fp, comments in analysis.get_all_comments().items()})


async def get_all_docstrings_tool(ctx: Context):
    """
    Get all docstrings (JComment) across the project.

    Returns:
        str: JSON {file_path -> [JComment]}.
    """
    analysis = ctx.request_context.lifespan_context.analysis_instance
    return json.dumps({fp: [c.model_dump() for c in docstrings] for fp, docstrings in analysis.get_all_docstrings().items()})
