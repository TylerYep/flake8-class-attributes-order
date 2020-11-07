import configparser

from conftest import run_validator_for_test_file
from flake8_function_order.checker import ClassFunctionOrderChecker


def test_version() -> None:
    config = configparser.ConfigParser()
    config.read("setup.cfg")
    assert config["metadata"]["version"] == ClassFunctionOrderChecker.version


def test_async_def_not_breaks_validator() -> None:
    errors = run_validator_for_test_file("async_def.py")
    assert len(errors) == 0


def test_ok_cases_produces_no_errors() -> None:
    errors = run_validator_for_test_file("ok.py")
    assert len(errors) == 0


def test_strict_ok_cases_no_errors() -> None:
    errors = run_validator_for_test_file("strict_ok.py")
    assert len(errors) == 1


def test_always_require_fixed_attributes() -> None:
    errors = run_validator_for_test_file("late_docstring.py")
    assert len(errors) == 1


def test_file_with_improper_default_order() -> None:
    errors = run_validator_for_test_file("errored.py")
    assert len(errors) == 3


def test_strict_mode_improper_order() -> None:
    errors = run_validator_for_test_file("strict_errored.py")
    assert len(errors) == 3


def test_child_attributes_fallback_to_parent_if_not_configured() -> None:
    errors = run_validator_for_test_file("configurable.py")
    assert len(errors) == 3


def test_save_delete() -> None:
    errors = run_validator_for_test_file("special_method.py")
    assert len(errors) == 4
    assert errors[0][2] == "CCE001 A.foo should be after A.__new__"
    assert errors[1][2] == "CCE001 B.foo should be after B.__init__"
    assert errors[2][2] == "CCE001 C.foo should be after C.__post_init__"
    assert errors[3][2] == "CCE001 D.foo should be after D.__str__"
    # assert errors[4][2] == "CCE001 E.foo should be after E.save"
    # assert errors[5][2] == "CCE001 F.foo should be after F.delete"
