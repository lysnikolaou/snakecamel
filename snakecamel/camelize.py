import re
import typing


def _camelize_string(s: str, capitalized: bool = False, strip_underscores: bool = False) -> str:
    if not isinstance(s, str):
        assert False, f"'s' should always be a string, but value {s} is not"

    if not s:
        return s

    s = s.strip(" _" if strip_underscores else " ")
    if capitalized:
        s = f"{s[0].upper()}{s[1:]}"

    # Explanation:
    # _(?P<after>[A-Za-z0-9]: Matches any underscore followed by a word character (letter or digit)
    # (?!^): Makes sure this is not at the beginning of the word since _simple_string should become _simpleString
    # (stripping initial undersocres is handled above)
    new = re.sub(r"(?!^)_(?P<after>[A-Za-z0-9])", lambda mo: mo.group("after").upper(), s)
    return type(s)(new)


def _camelize_other_iterable(
    iterable: typing.Iterable, capitalized: bool, strip_underscores: bool = False
) -> typing.Iterable:
    if not isinstance(iterable, typing.Iterable):
        assert False, f"'iterable' should always be an iterable, but value {iterable} is not"

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
    return type(iterable)(new)  # type: ignore


def _camelize_mapping(
    mapping: typing.Mapping,
    capitalized: bool = False,
    strip_underscores: bool = False,
    camelize_mapping_values: bool = False,
) -> dict:
    if not isinstance(mapping, typing.Mapping):
        assert False, f"'mapping' should always be a mapping, but value {mapping} is not"

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
