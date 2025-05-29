import json
from fastmcp import Context


async def JComment_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JComment",
            "description": "Represents a comment in Java code, including source line/column positions and whether it is Javadoc.",
            "fields": ["content", "start_line", "end_line", "start_column", "end_column", "is_javadoc"],
            "related_models": [],
        },
        indent=2,
    )


async def JRecordComponent_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JRecordComponent",
            "description": "Represents a component of a Java record, including type, annotations, modifiers, and optional default value.",
            "fields": ["comment", "name", "type", "modifiers", "annotations", "default_value", "is_var_args"],
            "related_models": ["JComment"],
        },
        indent=2,
    )


async def JField_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JField",
            "description": "Represents a field in a Java class or interface, including its type, variables, modifiers, and annotations.",
            "fields": ["comment", "type", "start_line", "end_line", "variables", "modifiers", "annotations"],
            "related_models": ["JComment"],
        },
        indent=2,
    )


async def JCallableParameter_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JCallableParameter",
            "description": "Represents a parameter of a Java method or constructor, including name, type, annotations, and positions.",
            "fields": ["name", "type", "annotations", "modifiers", "start_line", "end_line", "start_column", "end_column"],
            "related_models": [],
        },
        indent=2,
    )


async def JEnumConstant_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JEnumConstant",
            "description": "Represents a constant in a Java enumeration, including its name and constructor arguments.",
            "fields": ["name", "arguments"],
            "related_models": [],
        },
        indent=2,
    )


async def JCRUDOperation_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JCRUDOperation",
            "description": "Represents a CRUD operation in the code (Create, Read, Update, Delete), tied to a line number and operation type.",
            "fields": ["line_number", "operation_type"],
            "related_models": ["CRUDOperationType"],
        },
        indent=2,
    )


async def JCRUDQuery_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JCRUDQuery",
            "description": "Represents a CRUD query, including line number, arguments, and query type.",
            "fields": ["line_number", "query_arguments", "query_type"],
            "related_models": ["CRUDQueryType"],
        },
        indent=2,
    )


async def JCallSite_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JCallSite",
            "description": "Represents a method call site, including caller, receiver, arguments, return type, flags, and CRUD details.",
            "fields": [
                "comment",
                "method_name",
                "receiver_expr",
                "receiver_type",
                "argument_types",
                "return_type",
                "callee_signature",
                "is_static_call",
                "is_constructor_call",
                "crud_operation",
                "crud_query",
                "start_line",
                "start_column",
                "end_line",
                "end_column",
            ],
            "related_models": ["JComment", "JCRUDOperation", "JCRUDQuery"],
        },
        indent=2,
    )


async def JVariableDeclaration_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JVariableDeclaration",
            "description": "Represents a local variable declaration, including type, initializer, position, and comment.",
            "fields": ["comment", "name", "type", "initializer", "start_line", "start_column", "end_line", "end_column"],
            "related_models": ["JComment"],
        },
        indent=2,
    )


async def InitializationBlock_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "InitializationBlock",
            "description": "Represents an initialization block (static or instance) in Java, including code, comments, fields accessed, and complexity.",
            "fields": [
                "file_path",
                "comments",
                "annotations",
                "thrown_exceptions",
                "code",
                "start_line",
                "end_line",
                "is_static",
                "referenced_types",
                "accessed_fields",
                "call_sites",
                "variable_declarations",
                "cyclomatic_complexity",
            ],
            "related_models": ["JComment", "JCallSite", "JVariableDeclaration"],
        },
        indent=2,
    )


async def JCallable_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JCallable",
            "description": "Represents a method or constructor, including signature, annotations, parameters, body, call sites, CRUD operations, and complexity.",
            "fields": [
                "signature",
                "is_implicit",
                "is_constructor",
                "comments",
                "annotations",
                "modifiers",
                "thrown_exceptions",
                "declaration",
                "parameters",
                "return_type",
                "code",
                "start_line",
                "end_line",
                "referenced_types",
                "accessed_fields",
                "call_sites",
                "is_entrypoint",
                "variable_declarations",
                "crud_operations",
                "crud_queries",
                "cyclomatic_complexity",
            ],
            "related_models": ["JComment", "JCallableParameter", "JCallSite", "JCRUDOperation", "JCRUDQuery", "JVariableDeclaration"],
        },
        indent=2,
    )


async def JType_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JType",
            "description": "Represents a Java class, interface, enum, or annotation, including modifiers, annotations, methods, fields, nested types, and entrypoint flag.",
            "fields": [
                "is_interface",
                "is_inner_class",
                "is_local_class",
                "is_nested_type",
                "is_class_or_interface_declaration",
                "is_enum_declaration",
                "is_annotation_declaration",
                "is_record_declaration",
                "is_concrete_class",
                "comments",
                "extends_list",
                "implements_list",
                "modifiers",
                "annotations",
                "parent_type",
                "nested_type_declarations",
                "callable_declarations",
                "field_declarations",
                "enum_constants",
                "record_components",
                "initialization_blocks",
                "is_entrypoint_class",
            ],
            "related_models": ["JComment", "JCallable", "JField", "JEnumConstant", "JRecordComponent", "InitializationBlock"],
        },
        indent=2,
    )


async def JCompilationUnit_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JCompilationUnit",
            "description": "Represents a Java source file, including package, imports, type declarations, and comments.",
            "fields": ["file_path", "package_name", "comments", "imports", "type_declarations", "is_modified"],
            "related_models": ["JComment", "JType"],
        },
        indent=2,
    )


async def JMethodDetail_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JMethodDetail",
            "description": "Represents details about a method, linking its declaration string, owning class, and JCallable body.",
            "fields": ["method_declaration", "klass", "method"],
            "related_models": ["JCallable"],
        },
        indent=2,
    )


async def JGraphEdges_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JGraphEdges",
            "description": "Represents an edge between methods in a call graph or dependency graph, including source/target, edge type, and weight.",
            "fields": ["source", "target", "type", "weight", "source_kind", "destination_kind"],
            "related_models": ["JMethodDetail"],
        },
        indent=2,
    )


async def JApplication_explainer(ctx: Context):
    return json.dumps(
        {
            "name": "JApplication",
            "description": "Represents the entire analyzed Java application, including symbol table, call graph, and system dependency graph.",
            "fields": ["symbol_table", "call_graph", "system_dependency_graph"],
            "related_models": ["JCompilationUnit", "JGraphEdges"],
        },
        indent=2,
    )
