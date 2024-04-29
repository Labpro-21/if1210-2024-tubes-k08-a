# Based on javascript's standard string operations. Implemented manually.

def _string_code_point_at(string: str, i: int) -> int:
    return ord(string[i])

def _string_index_of(string: str, find: str) -> int:
    # return string.index(find)
    stringLength = len(string)
    findLength = len(find)
    for i in range(0, stringLength - findLength):
        valid = True
        for j in range(0, findLength):
            if(string[i + j] == find[j]):
                continue
            valid = False
            break
        if not valid:
            continue
        return i
    return -1

def _string_last_index_of(string: str, find: str) -> int:
    stringLength = len(string)
    findLength = len(find)
    for i in range(stringLength - findLength - 1, -1, -1):
        valid = True
        for j in range(0, findLength):
            if(string[i + j] == find[j]):
                continue
            valid = False
            break
        if not valid:
            continue
        return i
    return -1

def _string_includes(string: str, find: str) -> int:
    return _string_index_of(string, find) >= 0

def _string_starts_with(string: str, find: str) -> bool:
    stringLength = len(string)
    findLength = len(find)
    if stringLength < findLength:
        return False
    for i in range(0, findLength):
        if(string[i] == find[i]):
            continue
        return False
    return True

def _string_ends_with(string: str, find: str) -> bool:
    stringLength = len(string)
    findLength = len(find)
    if stringLength < findLength:
        return False
    for i in range(0, findLength):
        if(string[stringLength - findLength + i] == find[i]):
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
    for i in range(count):
        result += string
    return result

def _string_slice(string: str, start: int, end: int = len(string)) -> str:
    result = ""
    for i in range(start, end):
        result += string[i]
    return result

_string_whitespace_characters = [""]