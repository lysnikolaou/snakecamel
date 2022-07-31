from collections import defaultdict
from datetime import date

from snakecamel import camelize


def test_camelize_empty_string() -> None:
    assert camelize("") == ""


def test_camelize_simple_string() -> None:
    assert camelize("snake_string") == "snakeString"


def test_campelize_simple_string_capitalized() -> None:
    assert camelize("snake_string", capitalized=True) == "SnakeString"


def test_camelize_outside_underscores() -> None:
    assert camelize("_snake_string__") == "_snakeString__"


def test_camelize_trim_outside_underscores() -> None:
    assert camelize("_snake_string__", strip_underscores=True) == "snakeString"


def test_camelize_trim_outside_underscores_capitalized() -> None:
    assert camelize("_snake_string__", strip_underscores=True, capitalized=True) == "SnakeString"


def test_camelize_simple_mapping() -> None:
    assert camelize({"simple_key": "simple_value"}) == {"simpleKey": "simple_value"}


def test_camelize_simple_mapping_camelize_values() -> None:
    assert camelize({"simple_key": "simple_value"}, camelize_mapping_values=True) == {
        "simpleKey": "simpleValue"
    }


def test_camelize_nested_mapping() -> None:
    assert camelize(
        {"simple_key": "simple_value", "complex_key": {"nested_key": "nested_value"}}
    ) == {"simpleKey": "simple_value", "complexKey": {"nestedKey": "nested_value"}}


def test_camelize_mapping_nested_iterable() -> None:
    assert camelize(
        {"simple_key": ["first_value", "second_value"]}, camelize_mapping_values=True
    ) == {"simpleKey": ["firstValue", "secondValue"]}


def test_camelize_mapping_not_dict() -> None:
    d = defaultdict(list)
    d["simple_string"].append("simple_value")
    assert camelize(d, camelize_mapping_values=True) == {"simpleString": ["simpleValue"]}


def test_camelize_simple_list() -> None:
    assert camelize(["simple_string"]) == ["simpleString"]


def test_camelize_iterable_string_iterable() -> None:
    assert camelize(["simple_string", ["another_simple_string"]]) == [
        "simpleString",
        ["anotherSimpleString"],
    ]


def test_camelize_simple_set() -> None:
    assert camelize({"simple_string"}) == {"simpleString"}


def test_camelize_simple_tuple() -> None:
    assert camelize(("simple_string",)) == ("simpleString",)


def test_camelize_iterable_with_non_camelized_type() -> None:
    assert camelize(["simple_string", 5]) == ["simpleString", 5]


def test_camelize_iterable_with_mapping() -> None:
    assert camelize(["simple_string", {"simple_key": "simple_value"}]) == [
        "simpleString",
        {"simpleKey": "simple_value"},
    ]


def test_camelize_unknown_type() -> None:
    assert camelize(date.today()) == date.today()


def test_camelize_complex_dictionary() -> None:
    assert camelize(
        {
            "simple_key": "simple_value",
            "list_key": ["list_value"],
            "set_key": {"set_value"},
            5: "hello",
            "nested_key": {"nested_key_again": "nested_value"},
        },
        camelize_mapping_values=True,
    ) == {
        "simpleKey": "simpleValue",
        "listKey": ["listValue"],
        "setKey": {"setValue"},
        5: "hello",
        "nestedKey": {"nestedKeyAgain": "nestedValue"},
    }
