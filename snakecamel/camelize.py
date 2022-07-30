import re
import typing


def _camelize_string(s: str, capitalized: bool = False, strip_underscores: bool = False) -> str:
    if not isinstance(s, str):
        raise ValueError(f"Value {s} is not a string")

    if not s:
        return s

    s = s.strip(" _" if strip_underscores else " ")
    if capitalized:
        s = f"{s[0].upper()}{s[1:]}"
    return re.sub(r"[_.-](\w|$)", lambda mo: mo.group(1).upper(), s)


def _camelize_other_iterable(
    iterable: typing.Iterable, capitalized: bool, strip_underscores: bool = False
) -> list:
    if not isinstance(iterable, typing.Iterable):
        raise ValueError(f"Value {iterable} is not iterable")

    new: list = []
    for item in iterable:
        if isinstance(item, typing.Mapping):
            new.append(_camelize_mapping(item, capitalized, strip_underscores))
        elif isinstance(item, str):
            new.append(_camelize_string(item, capitalized, strip_underscores))
        elif isinstance(item, typing.Iterable):
            new.append(_camelize_other_iterable(item, capitalized, strip_underscores))
        else:
            new.append(item)
    return new


def _camelize_mapping(
    mapping: typing.Mapping,
    capitalized: bool = False,
    strip_underscores: bool = False,
    camelize_mapping_values: bool = False,
) -> dict:
    if not isinstance(mapping, typing.Mapping):
        raise ValueError(f"Value {mapping} is not a mapping")

    new: dict = {}
    for key, value in mapping.items():
        if isinstance(key, str):
            new_key = _camelize_string(
                key,
                capitalized=capitalized,
            )
        else:
            new_key = key

        if isinstance(value, typing.Mapping):
            new[new_key] = _camelize_mapping(
                value, capitalized, strip_underscores, camelize_mapping_values
            )
        elif camelize_mapping_values and isinstance(value, str):
            new[new_key] = _camelize_string(value, capitalized, strip_underscores)
        elif camelize_mapping_values and isinstance(value, typing.Iterable):
            new[new_key] = _camelize_other_iterable(value, capitalized, strip_underscores)
        else:
            new[new_key] = value
    return new


def camelize(
    element: typing.Any,
    capitalized: bool = False,
    strip_underscores: bool = False,
    camelize_mapping_values: bool = False,
) -> typing.Any:
    if isinstance(element, typing.Mapping):
        return _camelize_mapping(element, capitalized, strip_underscores, camelize_mapping_values)
    elif isinstance(element, str):
        return _camelize_string(element, capitalized, strip_underscores)
    elif isinstance(element, typing.Iterable):
        return _camelize_other_iterable(element, capitalized, strip_underscores)
    return element
