import ast
from typing import Mapping


def get_model_parts_info(model_ast, weights: Mapping[str, int]):
    parts_info = []
    for child_node in model_ast.body:
        node_type = get_model_node_type(child_node)
        if node_type in weights:
            parts_info.append(
                {
                    "model_name": model_ast.name,
                    "node": child_node,
                    "type": node_type,
                    "weight": weights[node_type],
                }
            )
    return parts_info


def get_model_node_type(child_node) -> str:
    direct_node_types_mapping = [
        (ast.If, lambda n: "if"),
        (ast.Pass, lambda n: "pass"),
        ((ast.Assign, ast.AnnAssign), lambda n: get_assighment_type(n)),
        ((ast.FunctionDef, ast.AsyncFunctionDef), lambda n: get_funcdef_type(n)),
        (
            ast.Expr,
            lambda n: "docstring" if isinstance(n.value, ast.Str) else "expression",
        ),
        (
            ast.ClassDef,
            lambda n: "meta_class" if child_node.name == "Meta" else "nested_class",
        ),
    ]
    for type_or_type_tuple, type_getter in direct_node_types_mapping:
        if isinstance(child_node, type_or_type_tuple):  # type: ignore
            return type_getter(child_node)


def get_assighment_type(child_node) -> str:
    assignee_node = (
        child_node.target
        if isinstance(child_node, ast.AnnAssign)
        else child_node.targets[0]
    )
    if isinstance(assignee_node, ast.Subscript):
        return "expression"
    if isinstance(assignee_node, ast.Name) and is_caps_lock_str(assignee_node.id):
        return "constant"
    return "field"


def get_funcdef_type(child_node) -> str:
    special_methods_names = {
        "__new__",
        "__init__",
        "__post_init__",
        "__str__",
    }
    decorator_names_to_types_map = {
        "property": "property_method",
        "cached_property": "property_method",
        "staticmethod": "static_method",
        "classmethod": "class_method",
        "private_property": "private_property_method",
        "private_cached_property": "private_property_method",
        "private_staticmethod": "private_static_method",
        "private_classmethod": "private_class_method",
    }
    for decorator_info in child_node.decorator_list:
        if (
            isinstance(decorator_info, ast.Name)
            and decorator_info.id in decorator_names_to_types_map
        ):

            if child_node.name.startswith("_"):
                return decorator_names_to_types_map[f"private_{decorator_info.id}"]

            return decorator_names_to_types_map[decorator_info.id]
    if child_node.name in special_methods_names:
        return child_node.name
    if child_node.name.startswith("__") and child_node.name.endswith("__"):
        return "magic_method"
    if child_node.name.startswith("_"):
        return "private_method"
    return "method"


def is_caps_lock_str(var_name: str) -> bool:
    return var_name.upper() == var_name
