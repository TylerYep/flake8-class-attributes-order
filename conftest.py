from __future__ import annotations

import ast
from pathlib import Path

from flake8_function_order.checker import ClassFunctionOrderChecker


def run_validator_for_test_file(filename: str) -> list[tuple[int, int, str, type]]:
    raw_content = Path(f"tests/test_files/{filename}").read_text()
    tree = ast.parse(raw_content)

    checker = ClassFunctionOrderChecker(tree=tree, filename=filename)
    return list(checker.run())
