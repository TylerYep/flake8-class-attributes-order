import ast
from typing import List, Tuple, Union

from .model_parts_info import SPECIAL_METHOD_NAMES, ModelPart


def get_ordering_errors(
    model_parts_info: List[ModelPart],
) -> List[Tuple[int, int, str]]:
    errors = []
    for model_part, next_model_part in zip(model_parts_info[:-1], model_parts_info[1:]):
        curr_name, curr_node, curr_type, curr_weight = model_part
        next_name, next_node, next_type, next_weight = next_model_part
        line_no, col_offset = curr_node.lineno, curr_node.col_offset

        if curr_name == next_name and curr_weight > next_weight:
            errors.append(
                (
                    line_no,
                    col_offset,
                    f"CCE001 {curr_name}.{get_node_name(curr_node, curr_type)} should "
                    f"be after {next_name}.{get_node_name(next_node, next_type)}",
                )
            )
        if curr_type in ("expression", "if"):
            errors.append(
                (
                    line_no,
                    col_offset,
                    "CCE002 Class level expression detected in "
                    f"class {curr_name}, line {line_no}",
                )
            )
    return errors


def get_node_name(node: ast.AST, node_type: str) -> str:
    if node_type.endswith("docstring"):
        return "docstring"
    if node_type.endswith("meta_class"):
        return "Meta"
    if node_type.endswith("constant"):
        return node.target.id if isinstance(node, ast.AnnAssign) else node.targets[0].id  # type: ignore  # noqa
    if node_type.endswith("field"):
        assert isinstance(node, (ast.Assign, ast.AnnAssign))
        return get_name_for_field_node_type(node)
    if node_type.endswith(("method", "nested_class") + SPECIAL_METHOD_NAMES):
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
