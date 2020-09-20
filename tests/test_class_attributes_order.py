import warnings

from conftest import run_validator_for_test_file


def test_file_with_improper_default_order():
    errors = run_validator_for_test_file("errored.py")
    assert len(errors) == 4


def test_async_def_not_breaks_validator():
    assert not run_validator_for_test_file("async_def.py")


def test_ok_cases_produces_no_errors():
    assert not run_validator_for_test_file("ok.py")


def test_strict_mode_improper_order():
    errors = run_validator_for_test_file("strict_errored.py")
    assert len(errors) == 2


def test_strict_mode_no_errors():
    assert not run_validator_for_test_file("strict_ok.py")


def test_configurable_order_correct_order():
    assert not run_validator_for_test_file(
        "configurable.py",
    )


def test_configurable_order_wrong_order():
    errors = run_validator_for_test_file(
        "configurable.py",
    )
    assert len(errors) == 2


def test_child_attributes_fallback_to_parent_if_not_configured():
    assert not run_validator_for_test_file(
        "configurable.py",
    )
    errors = run_validator_for_test_file(
        "configurable.py",
    )
    assert len(errors) == 1


def test_ignore_base_attribute_and_subattributes_if_not_configured():
    errors = run_validator_for_test_file(
        "configurable.py",
    )
    assert len(errors) == 1


def test_always_require_fixed_attributes():
    errors = run_validator_for_test_file(
        "late_docstring.py",
    )
    assert len(errors) == 1


def test_warning_if_both_strict_mode_and_configurable_order_defined():
    with warnings.catch_warnings(record=True) as w:
        run_validator_for_test_file(
            "ok.py",
        )
        assert len(w) == 1


def test_save_delete():
    errors = run_validator_for_test_file(
        "special_method.py",
    )
    assert len(errors) == 6
    assert errors[0][2] == "CCE001 A.foo should be after A.__new__"
    assert errors[1][2] == "CCE001 B.foo should be after B.__init__"
    assert errors[2][2] == "CCE001 C.foo should be after C.__post_init__"
    assert errors[3][2] == "CCE001 D.foo should be after D.__str__"
    assert errors[4][2] == "CCE001 E.foo should be after E.save"
    assert errors[5][2] == "CCE001 F.foo should be after F.delete"
