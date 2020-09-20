import ast
from typing import Iterator, List, Tuple

from flake8_function_order import __version__ as version
from flake8_function_order.model_parts_info import get_model_parts_info
from flake8_function_order.ordering_errors import get_ordering_errors


class ClassFunctionOrderChecker:

    name = "flake8-function-order"
    version = version

    def __init__(self, tree: ast.Module, filename: str):
        self.filename = filename
        self.tree = tree

    def run(self) -> Iterator[Tuple[int, int, str, type]]:
        weight_info = {
            "docstring": 0,
            "pass": 1,
            "meta_class": 2,
            "nested_class": 3,
            "constant": 4,
            "field": 5,
            "outer_field": 6,
            "if": 7,
            "expression": 8,
            "__new__": 9,
            "__init__": 10,
            "__post_init__": 11,
            "__str__": 12,
            "magic_method": 13,
            "property_method": 20,
            "private_property_method": 21,
            "class_method": 22,
            "private_class_method": 23,
            "static_method": 24,
            "private_static_method": 25,
            "method": 26,
            "private_method": 28,
        }
        classes = [n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)]
        errors: List[Tuple[int, int, str]] = []

        for class_def in classes:
            model_parts_info = get_model_parts_info(class_def, weight_info)
            errors += get_ordering_errors(model_parts_info)

        for lineno, col_offset, error_msg in errors:
            yield lineno, col_offset, error_msg, type(self)
