from typing import Any, TypeVar, Callable, Union

_T = TypeVar("_T")
_U = TypeVar("_U")

# Primordials Functions
# All of these functions has no side effects and are the base construct of a programming language.
# I do really hope (newly merged! https://github.com/python/cpython/pull/113465) python JIT can recognize these functions.
# Because these functions can and WILL slowdown performance by A LOT. Though the purpose of this assignment was to teach
# the base of programming fundamentals, in a real world application you absolutely want to use already available built-in functions.

# String Primordials
# Based on javascript's standard string operations. Implemented manually.
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String

def _string_concat(*strings: str) -> str:
    result = ""
    for string in strings:
        result += string
    return result

def _string_slice(string: str, start: int, end: int = None) -> str:
    if end is None:
        end = len(string)
    result = ""
    for i in range(start, end):
        result += string[i]
    return result

def _string_substring(string: str, start: int, end: int = None) -> str:
    return _string_slice(string, start, end)

def _string_code_point_at(string: str, i: int) -> int:
    return ord(string[i])

def _string_index_of(string: str, search: str, position: int = 0) -> int:
    # return string.index(search)
    stringLength = len(string)
    searchLength = len(search)
    if position < 0:
        position = 0
    for i in range(position, stringLength - searchLength):
        valid = True
        for j in range(0, searchLength):
            if string[i + j] == search[j]:
                continue
            valid = False
            break
        if not valid:
            continue
        return i
    return -1

def _string_last_index_of(string: str, search: str, position: int = None) -> int:
    stringLength = len(string)
    searchLength = len(search)
    if position is None:
        position = stringLength - 1
    position = stringLength - position - 1
    for i in range(stringLength - searchLength - position, -1, -1):
        valid = True
        for j in range(0, searchLength):
            if string[i + j] == search[j]:
                continue
            valid = False
            break
        if not valid:
            continue
        return i
    return -1

def _string_includes(string: str, search: str) -> int:
    return _string_index_of(string, search) >= 0

def _string_starts_with(string: str, search: str) -> bool:
    stringLength = len(string)
    searchLength = len(search)
    if stringLength < searchLength:
        return False
    for i in range(0, searchLength):
        if string[i] == search[i]:
            continue
        return False
    return True

def _string_ends_with(string: str, search: str) -> bool:
    stringLength = len(string)
    searchLength = len(search)
    if stringLength < searchLength:
        return False
    for i in range(0, searchLength):
        if string[stringLength - searchLength + i] == search[i]:
            continue
        return False
    return True

def _string_pad_start(string: str, length: int, padding: str) -> int:
    additionalPadding = length - len(string)
    if additionalPadding <= 0:
        return string
    return _string_slice(_string_repeat(padding, additionalPadding // len(padding)), 0, additionalPadding) + string

def _string_pad_end(string: str, length: int, padding: str) -> int:
    additionalPadding = length - len(string)
    if additionalPadding <= 0:
        return string
    return string + _string_slice(_string_repeat(padding, additionalPadding // len(padding)), 0, additionalPadding)

def _string_repeat(string: str, count: int) -> str:
    result = ""
    for _ in range(count):
        result += string
    return result

def _string_to_upper_case(string: str) -> str:
    return string.upper()

def _string_to_lower_case(string: str) -> str:
    return string.lower()

# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar
_string_whitespace_characters = ['\t', '\x0b', '\x0c', ' ', '\xa0', '\ufeff', '\u3000', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2008', '\u2009', '\u200a', '\u205f', '\u2007', '\u202f']
_string_line_terminators_characters = ['\n', '\r', '\u2028', '\u2029']

def _string_trim_end(string: str) -> str:
    trimIndex = len(string) - 1
    while trimIndex >= 0:
        character = string[trimIndex]
        if _array_includes(_string_whitespace_characters, character) or _array_includes(_string_line_terminators_characters, character):
            continue
        break
    return _string_slice(string, 0, trimIndex + 1)

def _string_trim_start(string: str) -> str:
    stringLength = len(string)
    trimIndex = 0
    while trimIndex < stringLength:
        character = string[trimIndex]
        if _array_includes(_string_whitespace_characters, character) or _array_includes(_string_line_terminators_characters, character):
            continue
        break
    return _string_slice(string, trimIndex)

def _string_trim(string: str) -> str:
    return _string_trim_start(_string_trim_end(string))

def _string_replace(string: str, search: str, replacement: Union[str, Callable[[str, int, str, dict], str]]) -> str:
    searchLength = len(search)
    foundIndex = _string_index_of(string, search)
    if foundIndex == -1:
        return string
    foundString = _string_slice(string, foundIndex, foundIndex + searchLength) # always will be `search`
    replacementString = replacement(foundString, foundIndex, string, {}) if callable(replacement) else replacement
    return _string_slice(string, 0, foundIndex) + replacementString + _string_slice(string, foundIndex + searchLength)

def _string_replace_all(string: str, search: str, replacement: Union[str, Callable[[str, int, str, dict], str]]) -> str:
    stringLength = len(string)
    searchLength = len(search)
    result = ""
    index = 0
    while index < stringLength:
        foundIndex = _string_index_of(string, search, index)
        if foundIndex == -1:
            break
        foundString = _string_slice(string, foundIndex, foundIndex + searchLength) # always will be `search`
        result += _string_slice(string, index, foundIndex)
        if callable(replacement):
            result += replacement(foundString, foundIndex, string, {})
        else:
            result += replacement
        index = foundIndex + searchLength
    result += _string_slice(string, index)
    return result

def _string_split(string: str, separator: str) -> list[str]:
    stringLength = len(string)
    separatorLength = len(separator)
    result: list[str] = []
    index = 0
    while index < stringLength:
        foundIndex = _string_index_of(string, separator, index)
        if foundIndex == -1:
            break
        _array_push(result, _string_slice(string, index, foundIndex))
        index = foundIndex + separatorLength
    _array_push(result, _string_slice(string, index))
    return result

# Array Primordials
# Based on javascript's standard array operations. Implemented manually.
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array

def _array_push(array: list[_T], *elements: _T) -> int:
    for element in elements:
        array.append(element)
    return len(array)

def _array_pop(array: list[_T]) -> _T:
    if len(array) == 0:
        return None
    return array.pop()

def _array_unshift(array: list[_T], *elements: _T) -> int:
    _array_reverse(elements)
    for element in elements:
        array.insert(0, element)
    return len(array)

def _array_shift(array: list[_T]) -> _T:
    if len(array) == 0:
        return None
    return array.pop(0)

def _array_concat(*arrays: list[Any]) -> list[Any]:
    result: list[Any] = []
    for array in arrays:
        result += array
    return result

def _array_slice(array: list[_T], start: int = None, end: int = None) -> list[_T]:
    if start is None:
        start = 0
    if end is None:
        end = len(array)
    return array[start:end]

def _array_splice(array: list[_T], start: int, deleteCount: int = None, *elements: _T) -> list[_T]:
    if deleteCount is None:
        deleteCount = len(array) - start
    deleted: list[_T] = []
    while deleteCount > 0:
        if start >= len(array):
            break
        deleted.append(array.pop(start))
    _array_reverse(elements)
    for element in elements:
        array.insert(start, element)
    return deleted

def _array_copy_within(array: list[_T], target: int, start: int, end: int = None) -> list[_T]:
    if end is None:
        end = len(array)
    for i in range(start, end):
        array[target + i - start] = array[i]
    return array

def _array_every(array: list[_T], callback: Callable[[_T, int, list[_T]], bool]) -> bool:
    for i in range(0, len(array)):
        if callback(array[i], i, array):
            continue
        return False
    return True

def _array_some(array: list[_T], callback: Callable[[_T, int, list[_T]], bool]) -> bool:
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        return True
    return False

def _array_index_of(array: list[_T], element: _T) -> int:
    for i in range(0, len(array)):
        if array[i] != element:
            continue
        return i
    return -1

def _array_last_index_of(array: list[_T], element: _T) -> int:
    for i in range(len(array) - 1, -1, -1):
        if array[i] != element:
            continue
        return i
    return -1

def _array_includes(array: list[_T], element: _T) -> bool:
    return _array_index_of(array, element) >= 0

def _array_find(array: list[_T], callback: Callable[[_T, int, list[_T]], bool]) -> _T:
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        return array[i]
    return None

def _array_find_index(array: list[_T], callback: Callable[[_T, int, list[_T]], bool]) -> int:
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        return i
    return -1

def _array_find_last(array: list[_T], callback: Callable[[_T, int, list[_T]], bool]) -> _T:
    for i in range(len(array) - 1, -1, -1):
        if not callback(array[i], i, array):
            continue
        return array[i]
    return None

def _array_find_last_index(array: list[_T], callback: Callable[[_T, int, list[_T]], bool]) -> int:
    for i in range(len(array) - 1, -1, -1):
        if not callback(array[i], i, array):
            continue
        return i
    return -1

def _array_for_each(array: list[_T], callback: Callable[[_T, int, list[_T]], Any]) -> None:
    for i in range(0, len(array)):
        callback(array[i], i, array)

def _array_filter(array: list[_T], callback: Callable[[_T, int, list[_T]], bool]) -> list[_T]:
    result: list[_T] = []
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        result.append(array[i])
    return result

def _array_map(array: list[_T], callback: Callable[[_T, int, list[_T]], _U]) -> list[_U]:
    result: list[_U] = []
    for i in range(0, len(array)):
        result.append(callback(array[i], i, array))
    return result

def _array_flat(array: list[Any], depth: int = 1, result: list[Any] = []) -> list[Any]:
    for i in range(0, len(array)):
        if not hasattr(array[i], "__len__"):
            result.append(array[i])
            continue
        _array_flat(array[i], depth - 1, result)
    return result

def _array_flat_map(array: list[_T], callback: Callable[[_T, int, list[_T]], _U]) -> list[Any]:
    return _array_flat(_array_map(array, callback))

def _array_join(array: list[Any], separator: str = ",") -> str:
    result = ""
    arrayLength = len(array)
    for i in range(0, arrayLength):
        result += array[i]
        if i != arrayLength - 1:
            result += separator
    return result

def _array_reduce(array: list[_T], callback: Callable[[_U, _T, int, list[_T]], _U], initial: _U) -> _U:
    accumulator = initial
    for i in range(0, len(array)):
        accumulator = callback(accumulator, array[i], i, array)
    return accumulator

def _array_reduce_right(array: list[_T], callback: Callable[[_U, _T, int, list[_T]], _U], initial: _U) -> _U:
    accumulator = initial
    for i in range(len(array) - 1, -1, -1):
        accumulator = callback(accumulator, array[i], i, array)
    return accumulator

def _array_reverse(array: list[_T]) -> None:
    arrayLength = len(array)
    for i in range(0, arrayLength // 2):
        array[i] = array[arrayLength - i - 1]

def _array_sort(array: list[_T], comparator: Callable[[_T, _T], int] = lambda x, y: x - y) -> list[_T]:
    arrayLength = len(array)
    for i in range(1, arrayLength):
        temp = array[i]
        j = i
        while comparator(temp, array[j - 1]) < 0:
            array[j] = array[j - 1]
            j -= 1
        array[j] = temp
    return array

def _array_to_reversed(array: list[_T]) -> list[_T]:
    array = _array_slice(array)
    _array_reverse(array)
    return array

def _array_to_sorted(array: list[_T], comparator: Callable[[_T, _T], int] = lambda x, y: x - y) -> list[_T]:
    array = _array_slice(array)
    _array_sort(array, comparator)
    return array

def _array_to_spliced(array: list[_T], start: int, deleteCount: int, *elements: _T) -> list[_T]:
    array = _array_slice(array)
    _array_splice(array, start, deleteCount, *elements)
    return array

def _array_with(array: list[_T], index: int, value: _T) -> list[_T]:
    array = _array_slice(array)
    array[index] = value
    return array
