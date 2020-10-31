import ast
from typing import Dict, List, NamedTuple, Union

SPECIAL_METHOD_NAMES = (
    "__new__",
    "__init__",
    "__post_init__",
)


class ModelPart(NamedTuple):
    model_name: str
    node: ast.AST
    type_: str
    weight: int


def get_model_parts_info(
    model_ast: ast.ClassDef, weights: Dict[str, int]
) -> List[ModelPart]:
    parts_info = []
    for child_node in model_ast.body:
        node_type = get_model_node_type(child_node)
        if node_type in weights:
            parts_info.append(
                ModelPart(model_ast.name, child_node, node_type, weights[node_type])
            )
    return parts_info


def get_model_node_type(child_node: ast.AST) -> str:
    if isinstance(child_node, ast.If):
        return "if"
    if isinstance(child_node, ast.Pass):
        return "pass"
    if isinstance(child_node, (ast.Assign, ast.AnnAssign)):
        return get_assighment_type(child_node)
    if isinstance(child_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return get_funcdef_type(child_node)
    if isinstance(child_node, ast.Expr):
        return "docstring" if isinstance(child_node.value, ast.Str) else "expression"
    if isinstance(child_node, ast.ClassDef):
        return "meta_class" if child_node.name == "Meta" else "nested_class"
    return ""


def get_assighment_type(child_node: Union[ast.Assign, ast.AnnAssign]) -> str:
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


def get_funcdef_type(child_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
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
            return decorator_names_to_types_map[
                f"private_{decorator_info.id}"
                if child_node.name.startswith("_")
                else decorator_info.id
            ]
        if isinstance(decorator_info, ast.Attribute) and decorator_info.attr in (
            "getter",
            "setter",
        ):
            return decorator_names_to_types_map["property"]
    if child_node.name in SPECIAL_METHOD_NAMES:
        return child_node.name
    if child_node.name.startswith("__") and child_node.name.endswith("__"):
        return "magic_method"
    if child_node.name.startswith("_"):
        return "private_method"
    return "method"


def is_caps_lock_str(var_name: str) -> bool:
    return var_name.upper() == var_name
