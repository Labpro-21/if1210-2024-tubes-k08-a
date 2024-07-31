from utils.primordials import *

def formatString(string):
    try:
        string = string_trim(string)
        string = array_join(array_map(string_split(string, "\n"), lambda l, *_: string_trim(l)), "\n")
        return string
    except BaseException as e:
        print(string)
        raise e

print(formatString(f"""
    Nama: Monster 2
    HP: 301.5
    Attack: 75
    Defense: 80
    Potions: 0
"""))
