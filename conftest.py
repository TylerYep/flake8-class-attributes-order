import ast
import os
from typing import List, Tuple

from flake8_function_order.checker import ClassFunctionOrderChecker


def run_validator_for_test_file(filename: str) -> List[Tuple[int, int, str, type]]:
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tests",
        "test_files",
        filename,
    )
    with open(test_file_path) as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)

    checker = ClassFunctionOrderChecker(tree=tree, filename=filename)
    return list(checker.run())
