from utils.primordials import *

def __get_arr(handle: str) -> list[list[str]]:
    # membuat array of array dari file csv
    res = []
    
    with open(handle, encoding="utf-8") as f:
        lines = string_split(f.read(), "\n")
        for line in lines:
            line = string_trim(line)
            if line == "":
                continue
            array_push(res, __parse_csv_line(line))
        array_push(res, "__EOP__")
    return res

def _csv_read_from_file(handle: str) -> list[list[str]]:
    return array_slice(__get_arr(handle), 0, -1)

def _csv_write_to_file(handle: str, data: list[list[str]]) -> None:
    with open(handle) as f:
        lines = array_map(data, lambda d, *_: array_join(d, ";"))
        combinedLines = array_join(lines, "\n")
        f.write(combinedLines)

# __parse_csv_line("")
# __parse_csv_line("a;")
# __parse_csv_line(";a")
# __parse_csv_line("a;a")
# __parse_csv_line("a;a\"")
# __parse_csv_line("a;a\";")
# __parse_csv_line("a;\"a\"")
# __parse_csv_line("a;\"a\";")
# __parse_csv_line("a;\";a\"")

def __parse_csv_line(line: str) -> str:
    entries: list[str] = []
    stack = ""
    i = 0
    while i < len(line):
        char = line[i]
        if char == ";":
            array_push(entries, stack)
            stack = ""
            i += 1
            continue
        if char != "\"" or len(stack) > 0:
            stack += char
            i += 1
            continue
        j = i + 1
        while j < len(line):
            char = line[j]
            if char == "\\" and j + 1 < len(line):
                if j + 4 <= len(line) and line[j + 1] == "r" and line[j + 2] == "\\" and line[j + 3] == "n":
                    stack += "\n"
                    j += 4
                    continue
                j += 1
                char = line[j]
                if char == "r" or char == "n":
                    stack += "\n"
                else:
                    stack += char
                j += 1
                continue
            if char == "\"" and (j + 1 >= len(line) or line[j + 1] == ";"):
                array_push(entries, stack)
                stack = ""
                j += 2
                break
            stack += char
            j += 1
        if j == len(line) and line[j - 1] != "\"":
            stack = "\"" + stack
            array_push(entries, stack)
            stack = ""
        i = j
    if len(stack) > 0 or (len(line) > 0 and line[len(line) - 1] == ";"):
        array_push(entries, stack)
    return entries
