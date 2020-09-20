import ast
from typing import Any, Dict, List, Tuple, Union


def get_ordering_errors(
    model_parts_info: List[Dict[str, Any]]
) -> List[Tuple[int, int, str]]:
    errors = []
    for model_part, next_model_part in zip(
        model_parts_info, model_parts_info[1:] + [None]  # type: ignore
    ):
        if (
            next_model_part
            and model_part["model_name"] == next_model_part["model_name"]
            and model_part["weight"] > next_model_part["weight"]
        ):
            errors.append(
                (
                    model_part["node"].lineno,
                    model_part["node"].col_offset,
                    "CCE001 {0}.{1} should be after {0}.{2}".format(
                        model_part["model_name"],
                        get_node_name(model_part["node"], model_part["type"]),
                        get_node_name(next_model_part["node"], next_model_part["type"]),
                    ),
                )
            )
        if model_part["type"] in ("expression", "if"):
            errors.append(
                (
                    model_part["node"].lineno,
                    model_part["node"].col_offset,
                    "CCE002 Class level expression detected in class {0}, line {1}".format(
                        model_part["model_name"],
                        model_part["node"].lineno,
                    ),
                )
            )
    return errors


def get_node_name(node: ast.AST, node_type: str) -> str:
    special_methods_names = (
        "__new__",
        "__init__",
        "__post_init__",
        "__str__",
    )
    if node_type.endswith("docstring"):
        return "docstring"
    if node_type.endswith("meta_class"):
        return "Meta"
    if node_type.endswith("constant"):
        return node.target.id if isinstance(node, ast.AnnAssign) else node.targets[0].id  # type: ignore
    if node_type.endswith("field"):
        assert isinstance(node, (ast.Assign, ast.AnnAssign))
        return get_name_for_field_node_type(node)
    if node_type.endswith(("method", "nested_class") + special_methods_names):
        return node.name  # type: ignore
    if node_type.endswith("expression"):
        return "<class_level_expression>"
    if node_type.endswith("if"):
        return "if ..."
    return ""


def get_name_for_field_node_type(node: Union[ast.Assign, ast.AnnAssign]) -> str:
    default_name = "<class_level_assignment>"
    if isinstance(node, ast.AnnAssign):
        return node.target.id if isinstance(node.target, ast.Name) else default_name
    if isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    if hasattr(node.targets[0], "attr"):
        return node.targets[0].attr  # type: ignore
    if isinstance(node.targets[0], ast.Tuple):
        return ", ".join(
            [e.id for e in node.targets[0].elts if isinstance(e, ast.Name)]
        )
    return default_name
