from collections import defaultdict
from datetime import date

from snakecamel import snakeize


def test_snakeize_empty_string() -> None:
    assert snakeize("") == ""


def test_snakeize_simple_string() -> None:
    assert snakeize("snakeString") == "snake_string"


def test_campelize_simple_string_capitalized() -> None:
    assert snakeize("SnakeString", capitalized=True) == "snake_string"


def test_snakeize_simple_mapping() -> None:
    assert snakeize({"simpleKey": "simpleValue"}) == {"simple_key": "simpleValue"}


def test_snakeize_simple_mapping_snakeize_values() -> None:
    assert snakeize({"simpleKey": "simpleValue"}, snakeize_mapping_values=True) == {
        "simple_key": "simple_value"
    }


def test_snakeize_nested_mapping() -> None:
    assert snakeize({"simpleKey": "simple_value", "complexKey": {"nestedKey": "nested_value"}}) == {
        "simple_key": "simple_value",
        "complex_key": {"nested_key": "nested_value"},
    }


def test_snakeize_mapping_nested_iterable() -> None:
    assert snakeize({"simpleKey": ["firstValue", "secondValue"]}, snakeize_mapping_values=True) == {
        "simple_key": ["first_value", "second_value"]
    }


def test_snakeize_mapping_not_dict() -> None:
    d = defaultdict(list)
    d["simpleString"].append("simpleValue")
    assert snakeize(d, snakeize_mapping_values=True) == {"simple_string": ["simple_value"]}


def test_snakeize_simple_list() -> None:
    assert snakeize(["simpleString"]) == ["simple_string"]


def test_snakeize_iterable_string_iterable() -> None:
    assert snakeize(["simpleString", ["anotherSimpleString"]]) == [
        "simple_string",
        ["another_simple_string"],
    ]


def test_snakeize_simple_set() -> None:
    assert snakeize({"simpleString"}) == {"simple_string"}


def test_snakeize_simple_tuple() -> None:
    assert snakeize(("simpleString",)) == ("simple_string",)


def test_snakeize_iterable_with_non_snakeized_type() -> None:
    assert snakeize(["simpleString", 5]) == ["simple_string", 5]


def test_snakeize_iterable_with_mapping() -> None:
    assert snakeize(["simpleString", {"simpleKey": "simple_value"}]) == [
        "simple_string",
        {"simple_key": "simple_value"},
    ]


def test_snakeize_unknown_type() -> None:
    assert snakeize(date.today()) == date.today()


def test_snakeize_complex_dictionary() -> None:
    assert snakeize(
        {
            "simpleKey": "simpleValue",
            "listKey": ["listValue"],
            "setKey": {"setValue"},
            5: "hello",
            "nestedKey": {"nestedKeyAgain": "nestedValue"},
        },
        snakeize_mapping_values=True,
    ) == {
        "simple_key": "simple_value",
        "list_key": ["list_value"],
        "set_key": {"set_value"},
        5: "hello",
        "nested_key": {"nested_key_again": "nested_value"},
    }
