import re
import typing


def _snakeize_string(s: str, capitalized: bool = False) -> str:
    if not isinstance(s, str):
        assert False, f"'s' should always be a string, but value {s} is not"

    if not s:
        return s

    s = s.strip()
    if capitalized:
        s = f"{s[0].lower()}{s[1:]}"

    new = re.sub(r"(?!^)(?P<upper>[A-Z])", lambda mo: f"_{mo.group('upper').lower()}", s)
    return type(s)(new)


def _snakeize_other_iterable(
    iterable: typing.Iterable, capitalized: bool = False
) -> typing.Iterable:
    if not isinstance(iterable, typing.Iterable):
        assert False, f"'iterable' should always be an iterable, but value {iterable} is not"

    new: list = []
    for item in iterable:
        if isinstance(item, typing.Mapping):
            new.append(_snakeize_mapping(item, capitalized))
        elif isinstance(item, str):
            new.append(_snakeize_string(item, capitalized))
        elif isinstance(item, typing.Iterable):
            new.append(_snakeize_other_iterable(item, capitalized))
        else:
            new.append(item)
    return type(iterable)(new)  # type: ignore


def _snakeize_mapping(
    mapping: typing.Mapping,
    capitalized: bool = False,
    snakeize_mapping_values: bool = False,
) -> dict:
    if not isinstance(mapping, typing.Mapping):
        assert False, f"'mapping' should always be a mapping, but value {mapping} is not"

    new: dict = {}
    for key, value in mapping.items():
        if isinstance(key, str):
            new_key = _snakeize_string(
                key,
                capitalized=capitalized,
            )
        else:
            new_key = key

        if isinstance(value, typing.Mapping):
            new[new_key] = _snakeize_mapping(value, capitalized, snakeize_mapping_values)
        elif snakeize_mapping_values and isinstance(value, str):
            new[new_key] = _snakeize_string(value, capitalized)
        elif snakeize_mapping_values and isinstance(value, typing.Iterable):
            new[new_key] = _snakeize_other_iterable(value, capitalized)
        else:
            new[new_key] = value
    return new


def snakeize(
    element: typing.Any,
    capitalized: bool = False,
    snakeize_mapping_values: bool = False,
) -> typing.Any:
    if isinstance(element, typing.Mapping):
        return _snakeize_mapping(element, capitalized, snakeize_mapping_values)
    elif isinstance(element, str):
        return _snakeize_string(element, capitalized)
    elif isinstance(element, typing.Iterable):
        return _snakeize_other_iterable(element, capitalized)
    return element
