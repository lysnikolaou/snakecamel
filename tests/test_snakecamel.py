from snakecamel import __version__, camelize


def test_version():
    assert __version__ == "0.1.0"


def test_simple_string() -> None:
    s = "snake_case_string"
    assert camelize(s) == "snakeCaseString"
