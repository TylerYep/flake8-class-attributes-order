import warnings

from conftest import run_validator_for_test_file


def test_async_def_not_breaks_validator():
    assert not run_validator_for_test_file("async_def.py")


def test_ok_cases_produces_no_errors():
    assert not run_validator_for_test_file("ok.py")


def test_always_require_fixed_attributes():
    errors = run_validator_for_test_file(
        "late_docstring.py",
    )
    assert len(errors) == 1
