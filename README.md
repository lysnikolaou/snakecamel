# snakecamel

[![Test - pytest](https://github.com/lysnikolaou/snakecamel/actions/workflows/test.yml/badge.svg)](https://github.com/lysnikolaou/snakecamel/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/lysnikolaou/snakecamel/branch/main/graph/badge.svg?token=1VWY4JCAWS)](https://codecov.io/gh/lysnikolaou/snakecamel)

A small utility to camelize (convert to camel-case) or snakeize (convert to snake-case) any object.

This is a very early-stage project & for the time-being is only there as a personal utility.

## Usage

```python
import snakecamel
>>> snakecamel.camelize("simple_string")
'simpleString
>>> snakecamel.snakeize("simpleString")
'simple_string'
```

### General notes

1. The library is designed to be very forgiving. It does not raise upon encountering an unknown type, it
   just skips it. This way, you can pass arbitrary objects to it & everything that can be camelized/snakeized,
   will be.

```python
>>> import snakecamel
>>> snakecamel.camelize(50)
50
>>> from datetime import date
>>> snakecamel.camelize({"hello_world": "hello_world", 50: 50, date.today(): "today"})
{'helloWorld': 'hello_world', 50: 50, datetime.date(2022, 7, 31): 'today'}
```

2. The library will try to re-construct the type you pass to it, so that if you pass
   different kinds of iterables, you'll get the same type returned. Unfortunately, that still
   does not work with mappings.

```python
>>> import snakecamel
>>> snakecamel.camelize(["simple_string"])
['simpleString']
>>> snakecamel.camelize({"simple_string"})
{'simpleString'}
>>> snakecamel.camelize(("simple_string",))
('simpleString',)
>>> snakecamel.camelize("simple_string")
'simpleString'
```

3. When camelizing/snakeizing mappings, you can choose to do so with keys only or keys & values.

```python
>>> import snakecamel
>>> snakecamel.camelize({"simple_key": "simple_value"})
{'simpleKey': 'simple_value'}
>>> snakecamel.camelize({"simple_key": "simple_value"}, camelize_mapping_values=True)
{'simpleKey': 'simpleValue'}
```

4. You can shoose between capitalized or non-capitalized camel case.

```python
>>> import snakecamel
>>> snakecamel.camelize("simple_string")
'simpleString'
>>> snakecamel.camelize("simple_string", capitalized=True)
'SimpleString'
```

When snakeizing, you _need_ to pass `capitalized=True`, if you want the first letter of a
capitalized camel-case word to be lowercased.

```python
>>> snakecamel.snakeize("simpleString")
'simple_string'
>>> snakecamel.snakeize("simpleString", capitalized=True)
'simple_string'
>>> snakecamel.snakeize("SimpleString")
'Simple_string'
>>> snakecamel.snakeize("SimpleString", capitalized=True)
'simple_string'
```

5. When camelizing, you can choose whether you're stripping leading/trailing underscores or not.

```python
import snakecamel
>>> import snakecamel
>>> snakecamel.camelize("_simple_string_")
'_simpleString_'
>>> snakecamel.camelize("_simple_string_", strip_underscores=True)
'simpleString'
```
