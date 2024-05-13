from utils.primordials import *

def get_arr(handle: str) -> list[list[str]]:
    # membuat array of array dari file csv
    res = []
    
    with open(handle) as f:
        lines = string_split(f.read(), "\n")
        for line in lines:
            line = string_trim(line)
            if line == "":
                continue
            array_push(res, string_split(line, ";"))
        array_push(res, "__EOP__")
    return res

def _csv_read_from_file(handle: str) -> list[list[str]]:
    return array_slice(get_arr(handle), 0, -1)

def _csv_write_to_file(handle: str, data: list[list[str]]) -> None:
    with open(handle) as f:
        lines = array_map(data, lambda d, *_: array_join(d, ";"))
        combinedLines = array_join(lines, "\n")
        f.write(combinedLines)
