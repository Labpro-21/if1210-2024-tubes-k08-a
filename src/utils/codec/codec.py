from utils.primordials import *

__base64_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def _base64_decode(data: str) -> str:
    dataLength = len(data)
    paddingIndex = string_index_of(data, "=")
    if paddingIndex == -1:
        paddingIndex = dataLength
    paddingLength = (dataLength - paddingIndex) + (4 - dataLength % 4 if dataLength % 4 != 0 else 0)
    if paddingLength > 2:
        raise "Invalid encoding"
    data = string_slice(data, 0, paddingIndex) + string_repeat("A", paddingLength)
    result = ""
    for i in range(0, dataLength, 4):
        a = string_index_of(__base64_table, data[i])
        b = string_index_of(__base64_table, data[i + 1])
        c = string_index_of(__base64_table, data[i + 2])
        d = string_index_of(__base64_table, data[i + 3])
        if a == -1 or b == -1 or c == -1 or d == -1:
            raise "Invalid encoding"
        e = (a << 18) | (b << 12) | (c << 6) | d
        result += chr(__shrz(e, 16) & 255) + chr(__shrz(e, 8) & 255) + chr(e & 255)
    result = string_slice(result, 0, len(result) - paddingLength)
    return result

def _base64_encode(data: str) -> str:
    paddingLength = 3 - len(data) % 3 if len(data) % 3 != 0 else 0
    data += string_repeat(chr(0), paddingLength)
    result = ""
    for i in range(0, len(data), 3):
        a = (ord(data[i]) << 16) | (ord(data[i + 1]) << 8) | ord(data[i + 2])
        b = __base64_table[__shrz(a, 18) & 63]
        c = __base64_table[__shrz(a, 12) & 63]
        d = __base64_table[__shrz(a, 6) & 63]
        e = __base64_table[a & 63]
        result += b + c + d + e
    result = string_slice(result, 0, len(result) - paddingLength)
    result += string_repeat("=", paddingLength)
    return result

def __shrz(val, n):
    return (val >> n) if val >= 0 else ((val + 0x100000000) >> n)
