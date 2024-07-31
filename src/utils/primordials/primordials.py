from typing import Any, TypeVar, Callable, Union, NamedTuple, Type, Optional

__T = TypeVar("__T")
__U = TypeVar("__U")

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
    stringLength = len(string)
    if end is None:
        end = stringLength
    if start < 0:
        start = stringLength + start
    if end < 0:
        end = stringLength + end
    start = max(0, min(stringLength, start))
    end = max(0, min(stringLength, end))
    result = ""
    for i in range(start, end):
        result += string[i]
    return result

def _string_substring(string: str, start: int, end: int = None) -> str:
    return _string_slice(string, start, end)

def _string_code_point_at(string: str, i: int) -> int:
    return ord(string[i])

def _string_index_of(string: str, search: str, position: int = 0) -> int:
    return string.find(search, position) # Fasttrack
    stringLength = len(string)
    searchLength = len(search)
    if position < 0:
        position = 0
    if position > stringLength:
        position = stringLength
    if searchLength == 0:
        return position
    for i in range(position, stringLength - searchLength + 1):
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
        position = stringLength
    if position < 0:
        position = 0
    if position > stringLength:
        position = stringLength
    if searchLength == 0:
        return position
    for i in range(position - searchLength, -1, -1):
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
        if not _array_includes(_string_whitespace_characters, character) and not _array_includes(_string_line_terminators_characters, character):
            break
        trimIndex -= 1
    return _string_slice(string, 0, trimIndex + 1)

def _string_trim_start(string: str) -> str:
    stringLength = len(string)
    trimIndex = 0
    while trimIndex < stringLength:
        character = string[trimIndex]
        if not _array_includes(_string_whitespace_characters, character) and not _array_includes(_string_line_terminators_characters, character):
            break
        trimIndex += 1
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
        if separatorLength == 0:
            foundIndex += 1
        _array_push(result, _string_slice(string, index, foundIndex))
        index = foundIndex + separatorLength
    if separatorLength > 0:
        _array_push(result, _string_slice(string, index))
    return result

# Array Primordials
# Based on javascript's standard array operations. Implemented manually.
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array

def _array_push(array: list[__T], *elements: __T) -> int:
    for element in elements:
        array.append(element)
    return len(array)

def _array_pop(array: list[__T]) -> __T:
    if len(array) == 0:
        return None
    return array.pop()

def _array_unshift(array: list[__T], *elements: __T) -> int:
    elements = list(elements)
    _array_reverse(elements)
    for element in elements:
        array.insert(0, element)
    return len(array)

def _array_shift(array: list[__T]) -> __T:
    if len(array) == 0:
        return None
    return array.pop(0)

def _array_concat(*arrays: list[Any]) -> list[Any]:
    result: list[Any] = []
    for array in arrays:
        result += array
    return result

def _array_slice(array: list[__T], start: int = None, end: int = None) -> list[__T]:
    if start is None:
        start = 0
    if end is None:
        end = len(array)
    return array[start:end]

def _array_splice(array: list[__T], start: int, deleteCount: int = None, *elements: __T) -> list[__T]:
    if deleteCount is None:
        deleteCount = len(array) - start
    deleted: list[__T] = []
    while deleteCount > 0:
        if start >= len(array):
            break
        deleted.append(array.pop(start))
        deleteCount -= 1
    elements = list(elements)
    _array_reverse(elements)
    for element in elements:
        array.insert(start, element)
    return deleted

def _array_copy_within(array: list[__T], target: int, start: int, end: int = None) -> list[__T]:
    if end is None:
        end = len(array)
    for i in range(start, end):
        array[target + i - start] = array[i]
    return array

def _array_every(array: list[__T], callback: Callable[[__T, int, list[__T]], bool]) -> bool:
    for i in range(0, len(array)):
        if callback(array[i], i, array):
            continue
        return False
    return True

def _array_some(array: list[__T], callback: Callable[[__T, int, list[__T]], bool]) -> bool:
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        return True
    return False

def _array_index_of(array: list[__T], element: __T) -> int:
    # return array.index(element) if element in array else -1 # Fasttrack
    for i in range(0, len(array)):
        if array[i] is not element:
            continue
        return i
    return -1

def _array_last_index_of(array: list[__T], element: __T) -> int:
    for i in range(len(array) - 1, -1, -1):
        if array[i] is not element:
            continue
        return i
    return -1

def _array_includes(array: list[__T], element: __T) -> bool:
    # return element in array # Fasttrack
    return _array_index_of(array, element) >= 0

def _array_find(array: list[__T], callback: Callable[[__T, int, list[__T]], bool]) -> __T:
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        return array[i]
    return None

def _array_find_index(array: list[__T], callback: Callable[[__T, int, list[__T]], bool]) -> int:
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        return i
    return -1

def _array_find_last(array: list[__T], callback: Callable[[__T, int, list[__T]], bool]) -> __T:
    for i in range(len(array) - 1, -1, -1):
        if not callback(array[i], i, array):
            continue
        return array[i]
    return None

def _array_find_last_index(array: list[__T], callback: Callable[[__T, int, list[__T]], bool]) -> int:
    for i in range(len(array) - 1, -1, -1):
        if not callback(array[i], i, array):
            continue
        return i
    return -1

def _array_for_each(array: list[__T], callback: Callable[[__T, int, list[__T]], Any]) -> None:
    for i in range(0, len(array)):
        callback(array[i], i, array)

def _array_filter(array: list[__T], callback: Callable[[__T, int, list[__T]], bool]) -> list[__T]:
    result: list[__T] = []
    for i in range(0, len(array)):
        if not callback(array[i], i, array):
            continue
        result.append(array[i])
    return result

def _array_map(array: list[__T], callback: Callable[[__T, int, list[__T]], __U]) -> list[__U]:
    result: list[__U] = []
    for i in range(0, len(array)):
        result.append(callback(array[i], i, array))
    return result

def _array_flat(array: list[Any], depth: int = 1, result: list[Any] = None) -> list[Any]:
    if result is None:
        result = []
    for i in range(0, len(array)):
        if type(array[i]) is not list:
            result.append(array[i])
            continue
        _array_flat(array[i], depth - 1, result)
    return result

def _array_flat_map(array: list[__T], callback: Callable[[__T, int, list[__T]], __U]) -> list[Any]:
    return _array_flat(_array_map(array, callback))

def _array_join(array: list[Any], separator: str = ",") -> str:
    return separator.join(array) # Fasttrack
    result = ""
    arrayLength = len(array)
    for i in range(0, arrayLength):
        result += array[i]
        if i != arrayLength - 1:
            result += separator
    return result

def _array_reduce(array: list[__T], callback: Callable[[__U, __T, int, list[__T]], __U], initial: __U) -> __U:
    accumulator = initial
    for i in range(0, len(array)):
        accumulator = callback(accumulator, array[i], i, array)
    return accumulator

def _array_reduce_right(array: list[__T], callback: Callable[[__U, __T, int, list[__T]], __U], initial: __U) -> __U:
    accumulator = initial
    for i in range(len(array) - 1, -1, -1):
        accumulator = callback(accumulator, array[i], i, array)
    return accumulator

def _array_reverse(array: list[__T]) -> None:
    array.reverse() # Fasttrack
    return
    arrayLength = len(array)
    for i in range(0, arrayLength // 2):
        temp = array[i]
        array[i] = array[arrayLength - i - 1]
        array[arrayLength - i - 1] = temp

def _array_sort(array: list[__T], comparator: Callable[[__T, __T], int] = lambda x, y: x - y) -> list[__T]:
    arrayLength = len(array)
    for i in range(1, arrayLength):
        temp = array[i]
        j = i
        while comparator(temp, array[j - 1]) < 0:
            array[j] = array[j - 1]
            j -= 1
        array[j] = temp
    return array

def _array_to_reversed(array: list[__T]) -> list[__T]:
    array = _array_slice(array)
    _array_reverse(array)
    return array

def _array_to_sorted(array: list[__T], comparator: Callable[[__T, __T], int] = lambda x, y: x - y) -> list[__T]:
    array = _array_slice(array)
    _array_sort(array, comparator)
    return array

def _array_to_spliced(array: list[__T], start: int, deleteCount: int, *elements: __T) -> list[__T]:
    array = _array_slice(array)
    _array_splice(array, start, deleteCount, *elements)
    return array

def _array_with(array: list[__T], index: int, value: __T) -> list[__T]:
    array = _array_slice(array)
    array[index] = value
    return array

# This function is not compliant with JS standard. 
# isNaN(parseInt("23a")) == true
# _parse_int("23a") is None
__zero_ord = ord("0")
def _parse_int(string: str) -> Optional[int]:
    string = _string_trim(string)
    if string == "" or string == "-":
        return None
    negate = False
    result = 0
    for i in range(len(string)):
        character = string[i]
        if i == 0 and character == "-":
            negate = True
            continue
        digit = ord(character) - __zero_ord
        if digit < 0 or digit > 9:
            return None
        result = result * 10 + digit
    return -result if negate else result

# Tuple/NamedTuple/Dict primordials

__Tuple = TypeVar("__Tuple", covariant=tuple)
__NamedTuple = TypeVar("__NamedTuple", covariant=NamedTuple)
__Dict = TypeVar("__Dict", covariant=dict)

def _tuple_to_array(tuple: __Tuple) -> list[Any]:
    result = [None for _ in range(len(tuple))]
    for i in range(len(tuple)):
        result[i] = tuple[i]
    return result

def _tuple_with(tuple: __Tuple, **elements: Any) -> __Tuple:
    result = _tuple_to_array(tuple)
    for key, value in elements.items():
        if not _string_starts_with(key, "_"):
            continue
        result[int(_string_slice(key, 1))] = value
    return (*result,)

def _namedtuple_to_dict(tuple: __NamedTuple) -> dict:
    tupleType: Type[NamedTuple] = type(tuple)
    result = dict()
    for key in tupleType._fields:
        result[key] = getattr(tuple, key)
    return result

def _namedtuple_with(tuple: __NamedTuple, **elements: Any) -> __NamedTuple:
    tupleType: Type[NamedTuple] = type(tuple)
    result = _namedtuple_to_dict(tuple)
    for key, value in elements.items():
        result[key] = value
    return tupleType(**result)

def _dict_clear(dictionary: __Dict):
    for key in list(dictionary.keys()):
        del dictionary[key]

def _dict_set(dictionary: __Dict, to: Union[__Dict, list[tuple[str, Any]]]):
    if type(to) is dict:
        for key, value in to.items():
            dictionary[key] = value
    if type(to) is list:
        for key, value in to:
            dictionary[key] = value
    return dictionary

def _dict_with(dictionary: __Dict, **elements: Any) -> __Dict:
    result = dict()
    _dict_set(result, dictionary)
    _dict_set(result, elements)
    return result

def _dict_key_of(dictionary: __Dict, element: Any) -> Any:
    for key, value in dictionary.items():
        if value is not element:
            continue
        return key
    return None
