from utils.primordials import *
from utils.math import *
from typing import TypedDict
from .console import _Driver, _DriverAttribute, _driver_new, _driver_set_size, _Rune, _RuneAttribute
import sys
import os

_DriverStd = TypedDict("DriverStd",
    size=Size,
    attribute=_DriverAttribute,
    contents=list[_Rune],
    dirtyLines=list[bool],
    
    lastLine=int,
    lastAttribute=_RuneAttribute
)

def _driverstd_new() -> _DriverStd:
    result: _DriverStd = dict_with(
        _driver_new(
            _DriverAttribute(tabSize=4),
            _driver_tick=_driverstd_tick,
            _driver_draw=_driverstd_draw
        ),
        lastLine=-1,
        lastAttribute=None
    )
    _driver_set_size(result, __get_terminal_size())
    return result

def _driverstd_tick(driverstd: _DriverStd) -> None:
    newSize = __get_terminal_size()
    if driverstd["size"] != newSize:
        _driver_set_size(driverstd, newSize)
    pass

def _driverstd_draw(driverstd: _DriverStd) -> None:
    size = driverstd["size"]
    contents = driverstd["contents"]
    dirtyLines = driverstd["dirtyLines"]
    for y in range(size.h):
        if not dirtyLines[y]:
            continue
        _driverstd_move_line(driverstd, y)
        for x in range(size.w):
            rune = contents[y * size.w + x]
            _driverstd_set_current_attribute(driverstd, rune.attribute)
            sys.stdout.write(rune.character)
    _driverstd_move_line(driverstd, size.h - 1)
    sys.stdout.flush()

def _driverstd_move_line(driverstd: _DriverStd, line: int) -> None:
    line = max(0, min(driverstd["size"].h - 1, line))
    if driverstd["lastLine"] == line:
        return
    command = f"\x1b[{line + 1};H"
    sys.stdout.write(command)
    driverstd["lastLine"] = line

def _driverstd_set_current_attribute(driverstd: _DriverStd, attribute: _RuneAttribute) -> str:
    lastAttribute = driverstd["lastAttribute"]
    if lastAttribute == attribute:
        return
    command = ""
    if lastAttribute is None or attribute.font != lastAttribute.font:
        command += f"\x1b[{max(0, min(10, attribute.font)) + 10}m"
    if lastAttribute is None or attribute.weight != lastAttribute.weight:
        command += f"\x1b[{2 if attribute.weight == -1 else 1 if attribute.weight == 1 else 22}m"
    if lastAttribute is None or attribute.italic != lastAttribute.italic:
        command += f"\x1b[{3 if attribute.italic else 23}m"
    if lastAttribute is None or attribute.foreground != lastAttribute.foreground:
        if attribute.foreground is None:
            command += f"\x1b[39m"
        else:
            r = max(0, min(255, attribute.foreground[0]))
            g = max(0, min(255, attribute.foreground[1]))
            b = max(0, min(255, attribute.foreground[2]))
            command += f"\x1b[38;2;{r};{g};{b}m"
    if lastAttribute is None or attribute.background != lastAttribute.background:
        if attribute.background is None:
            command += f"\x1b[49m"
        else:
            r = max(0, min(255, attribute.background[0]))
            g = max(0, min(255, attribute.background[1]))
            b = max(0, min(255, attribute.background[2]))
            command += f"\x1b[48;2;{r};{g};{b}m"
    sys.stdout.write(command)
    driverstd["lastAttribute"] = attribute

def __get_terminal_size() -> Size:
    value = os.get_terminal_size()
    return Size(value[0], value[1])
