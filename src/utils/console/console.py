from utils.math import *
from utils.primordials import *
from utils.mixin import *
from typing import TypedDict, Any, Callable, Union, Literal, NamedTuple

_PosType = Union[
    Literal["Absolute"], 
    Literal["Factor"], 
    Literal["Center"], 
    Literal["End"], 
    Literal["Combine"], 
    Literal["View"], 
    Literal["Function"]
]
_Pos = TypedDict("Pos",
    type=_PosType
)
_PosAbsolute = TypedDict("Pos",
    type=Literal["Absolute"],
    absolute=float
)
_PosFactor = TypedDict("Pos",
    type=Literal["Factor"],
    factor=float
)
_PosCenter = TypedDict("Pos",
    type=Literal["Center"]
)
_PosEnd = TypedDict("Pos",
    type=Literal["End"],
    offset=float
)
_PosCombine = TypedDict("Pos",
    type=Literal["Combine"],
    add=bool,
    left=_Pos,
    right=_Pos
)
_PosView = TypedDict("Pos",
    type=Literal["View"],
    view="_View",
    side=int
)
_PosFunction = TypedDict("Pos",
    type=Literal["Function"],
    function=Callable[[float], float]
)
def _pos_from_absolute(absolute: float) -> _PosAbsolute:
    return dict(
        type="Absolute",
        absolute=absolute
    )
def _pos_from_factor(factor: float) -> _PosFactor:
    return dict(
        type="Factor",
        factor=factor
    )
def _pos_from_center() -> _PosCenter:
    return dict(
        type="Center"
    )
def _pos_from_end(offset: float) -> _PosEnd:
    return dict(
        type="End",
        offset=offset
    )
def _pos_from_combine(add: bool, left: _Pos, right: _Pos) -> _PosCombine:
    return dict(
        type="Combine",
        add=add,
        left=left,
        right=right
    )
def _pos_from_view(view: "_View", side: int) -> _PosView:
    return dict(
        type="View",
        view=view,
        side=side
    )
def _pos_from_function(function: Callable[[float], float]) -> _PosFunction:
    return dict(
        type="Function",
        function=function
    )
def _pos_as_absolute(pos: _Pos) -> Union[None, _PosAbsolute]:
    return pos if pos["type"] == "Absolute" else None
def _pos_as_factor(pos: _Pos) -> Union[None, _PosFactor]:
    return pos if pos["type"] == "Factor" else None
def _pos_as_center(pos: _Pos) -> Union[None, _PosCenter]:
    return pos if pos["type"] == "Center" else None
def _pos_as_end(pos: _Pos) -> Union[None, _PosEnd]:
    return pos if pos["type"] == "End" else None
def _pos_as_combine(pos: _Pos) -> Union[None, _PosCombine]:
    return pos if pos["type"] == "Combine" else None
def _pos_as_view(pos: _Pos) -> Union[None, _PosView]:
    return pos if pos["type"] == "View" else None
def _pos_as_function(pos: _Pos) -> Union[None, _PosFunction]:
    return pos if pos["type"] == "Function" else None
def _pos_anchor(pos: _Pos, scalar: float) -> float:
    if _pos_as_absolute(pos) is not None:
        return _pos_absolute_anchor(pos, scalar)
    if _pos_as_factor(pos) is not None:
        return _pos_factor_anchor(pos, scalar)
    if _pos_as_center(pos) is not None:
        return _pos_center_anchor(pos, scalar)
    if _pos_as_end(pos) is not None:
        return _pos_end_anchor(pos, scalar)
    if _pos_as_combine(pos) is not None:
        return _pos_combine_anchor(pos, scalar)
    if _pos_as_view(pos) is not None:
        return _pos_view_anchor(pos, scalar)
    if _pos_as_function(pos) is not None:
        return _pos_function_anchor(pos, scalar)
def _pos_absolute_anchor(pos: _PosAbsolute, scalar: float) -> float:
    return pos["absolute"]
def _pos_factor_anchor(pos: _PosFactor, scalar: float) -> float:
    return pos["factor"] * scalar
def _pos_center_anchor(pos: _PosCenter, scalar: float) -> float:
    return scalar / 2
def _pos_end_anchor(pos: _PosEnd, scalar: float) -> float:
    return scalar - pos["offset"]
def _pos_combine_anchor(pos: _PosCombine, scalar: float) -> float:
    leftAnchor = _pos_anchor(pos["left"], scalar)
    rightAnchor = _pos_anchor(pos["right"], scalar)
    return leftAnchor + rightAnchor if pos["add"] else leftAnchor - rightAnchor
def _pos_view_anchor(pos: _PosView, scalar: float) -> float:
    view = pos["view"]
    side = pos["side"]
    frame = view["frame"]
    if side == 0:
        return frame.x
    if side == 1:
        return frame.y
    if side == 2:
        return frame.x + frame.w
    if side == 3:
        return frame.y + frame.h
    return None
def _pos_function_anchor(pos: _PosFunction, scalar: float) -> float:
    return pos["function"](scalar)

def _pos_add(left: _Pos, right: _Pos) -> _Pos:
    return _pos_from_combine(True, left, right)
def _pos_sub(left: _Pos, right: _Pos) -> _Pos:
    return _pos_from_combine(False, left, right)
def _pos_from_view_left(view: "_View") -> _Pos:
    return _pos_from_combine(True, _pos_from_view(view, 0), _pos_from_absolute(0))
def _pos_from_view_top(view: "_View") -> _Pos:
    return _pos_from_combine(True, _pos_from_view(view, 1), _pos_from_absolute(0))
def _pos_from_view_right(view: "_View") -> _Pos:
    return _pos_from_combine(True, _pos_from_view(view, 2), _pos_from_absolute(0))
def _pos_from_view_bottom(view: "_View") -> _Pos:
    return _pos_from_combine(True, _pos_from_view(view, 3), _pos_from_absolute(0))
def _pos_from_view_x(view: "_View") -> _Pos:
    return _pos_from_view_left(view)
def _pos_from_view_y(view: "_View") -> _Pos:
    return _pos_from_view_top(view)

_DimType = Union[
    Literal["Absolute"], 
    Literal["Factor"], 
    Literal["Fill"], 
    Literal["Combine"], 
    Literal["View"], 
    Literal["Function"]
]
_Dim = TypedDict("Dim",
    type=_DimType
)
_DimAbsolute = TypedDict("Dim",
    type=Literal["Absolute"],
    absolute=float
)
_DimFactor = TypedDict("Dim",
    type=Literal["Factor"],
    factor=float
)
_DimFill = TypedDict("Dim",
    type=Literal["Fill"],
    offset=float
)
_DimCombine = TypedDict("Dim",
    type=Literal["Combine"],
    add=bool,
    left=_Dim,
    right=_Dim
)
_DimView = TypedDict("Dim",
    type=Literal["View"],
    view="_View",
    side=int
)
_DimFunction = TypedDict("Dim",
    type=Literal["Function"],
    function=Callable[[float], float]
)
def _dim_from_absolute(absolute: float) -> _DimAbsolute:
    return dict(
        type="Absolute",
        absolute=absolute
    )
def _dim_from_factor(factor: float) -> _DimFactor:
    return dict(
        type="Factor",
        factor=factor
    )
def _dim_from_fill(offset: float) -> _DimFill:
    return dict(
        type="Fill",
        offset=offset
    )
def _dim_from_combine(add: bool, left: _Dim, right: _Dim) -> _DimCombine:
    return dict(
        type="Combine",
        add=add,
        left=left,
        right=right
    )
def _dim_from_view(view: "_View", side: int) -> _DimView:
    return dict(
        type="View",
        view=view,
        side=side
    )
def _dim_from_function(function: Callable[[float], float]) -> _DimFunction:
    return dict(
        type="Function",
        function=function
    )
def _dim_as_absolute(dim: _Dim) -> Union[None, _DimAbsolute]:
    return dim if dim["type"] == "Absolute" else None
def _dim_as_factor(dim: _Dim) -> Union[None, _DimFactor]:
    return dim if dim["type"] == "Factor" else None
def _dim_as_fill(dim: _Dim) -> Union[None, _DimFill]:
    return dim if dim["type"] == "Fill" else None
def _dim_as_combine(dim: _Dim) -> Union[None, _DimCombine]:
    return dim if dim["type"] == "Combine" else None
def _dim_as_view(dim: _Dim) -> Union[None, _DimView]:
    return dim if dim["type"] == "View" else None
def _dim_as_function(dim: _Dim) -> Union[None, _DimFunction]:
    return dim if dim["type"] == "Function" else None
def _dim_anchor(dim: _Dim, scalar: float) -> float:
    if _dim_as_absolute(dim) is not None:
        return _dim_absolute_anchor(dim, scalar)
    if _dim_as_factor(dim) is not None:
        return _dim_factor_anchor(dim, scalar)
    if _dim_as_fill(dim) is not None:
        return _dim_fill_anchor(dim, scalar)
    if _dim_as_combine(dim) is not None:
        return _dim_combine_anchor(dim, scalar)
    if _dim_as_view(dim) is not None:
        return _dim_view_anchor(dim, scalar)
    if _dim_as_function(dim) is not None:
        return _dim_function_anchor(dim, scalar)
def _dim_absolute_anchor(dim: _DimAbsolute, scalar: float) -> float:
    return dim["absolute"]
def _dim_factor_anchor(dim: _DimFactor, scalar: float) -> float:
    return dim["factor"] * scalar
def _dim_fill_anchor(dim: _DimFill, scalar: float) -> float:
    return scalar - dim["offset"]
def _dim_combine_anchor(dim: _DimCombine, scalar: float) -> float:
    leftAnchor = _dim_anchor(dim["left"], scalar)
    rightAnchor = _dim_anchor(dim["right"], scalar)
    return leftAnchor + rightAnchor if dim["add"] else leftAnchor - rightAnchor
def _dim_view_anchor(dim: _DimView, scalar: float) -> float:
    view = dim["view"]
    side = dim["side"]
    frame = view["frame"]
    if side == 0:
        return frame.w
    if side == 1:
        return frame.h
    return None
def _dim_function_anchor(dim: _DimFunction, scalar: float) -> float:
    return dim["data"](scalar)

def _dim_add(left: _Dim, right: _Dim) -> _Dim:
    return _dim_from_combine(True, left, right)
def _dim_sub(left: _Dim, right: _Dim) -> _Dim:
    return _dim_from_combine(False, left, right)
def _dim_from_view_width(view: "_View") -> _Dim:
    return _dim_from_view(view, 1)
def _dim_from_view_height(view: "_View") -> _Dim:
    return _dim_from_view(view, 0)

_RuneAttribute = NamedTuple("RuneAttribute", [
    ("font", int),
    ("weight", int),
    ("italic", bool),
    ("underline", bool),
    ("foreground", tuple[int,int,int]),
    ("background", tuple[int,int,int])
])
_Rune = NamedTuple("Rune", [
    ("character", str),
    ("attribute", _RuneAttribute)
])
_RuneAttribute_clear = _RuneAttribute(0, 1, False, False, None, None)
_Rune_clear = _Rune(" ", _RuneAttribute_clear)

def _rune_from_string(text: str, attribute: _RuneAttribute) -> list[_Rune]:
    result = string_split(text, "")
    result = array_map(result, lambda c, *_: _Rune(c, attribute))
    return result

_DriverAttribute = NamedTuple("DriverAttribute", [
    ("tabSize", int)
])
_Driver = TypedDict("Driver",
    size=Size,
    attribute=_DriverAttribute,
    contents=list[_Rune],
    dirtyLines=list[bool]
)

def _driver_new(attribute: _DriverAttribute, **kwargs) -> _Driver:
    return dict(
        size=Size(0, 0),
        attribute=attribute,
        contents=[],
        dirtyLines=[],
        **mixin_new(kwargs)
    )
def _driver_get_size(driver: _Driver) -> Size:
    return driver["size"]
def _driver_get_attribtue(driver: _Driver) -> _DriverAttribute:
    return driver["attribute"]
def _driver_get_rune_width(driver: _Driver, rune: _Rune, direction: "_TextDirection") -> int:
    attribute = driver["attribute"]
    if rune.character == "\t" and _text_direction_is_horizontal(direction):
        return attribute.tabSize
    return 1
def _driver_get_rune_height(driver: _Driver, rune: _Rune, direction: "_TextDirection") -> int:
    attribute = driver["attribute"]
    if rune.character == "\t" and _text_direction_is_vertical(direction):
        return attribute.tabSize
    return 1
def _driver_set_size(driver: _Driver, size: Size) -> None:
    driver["size"] = size
    driver["contents"] = [_Rune_clear for _ in range(size.w * size.h)]
    driver["dirtyLines"] = [True for _ in range(size.h)]
def _driver_set_content(driver: _Driver, x: int, y: int, rune: _Rune) -> None:
    size = driver["size"]
    contents = driver["contents"]
    dirtyLines = driver["dirtyLines"]
    if x < 0 or y < 0 or x >= size.w or y >= size.h:
        return
    contents[y * size.w + x] = rune
    dirtyLines[y] = True
def _driver_fill_rect(driver: _Driver, rectangle: Rectangle, rune: _Rune) -> None:
    size = driver["size"]
    contents = driver["contents"]
    dirtyLines = driver["dirtyLines"]
    driverBounds = rectangle_from_point_size(EmptyPoint, size)
    bounds = rectangle_intersect(driverBounds, rectangle)
    for y in range(bounds.y, bounds.y + bounds.h):
        for x in range(bounds.x, bounds.x + bounds.w):
            contents[y * size.w + x] = rune
        dirtyLines[y] = True
def _driver_clear_content(driver: _Driver, x: int, y: int) -> None:
    _driver_set_content(driver, x, y, _Rune_clear)
def _driver_clear_contents(driver: _Driver) -> None:
    _driver_fill_rect(driver, rectangle_from_point_size(EmptyPoint, driver["size"]), _Rune_clear)
def _driver_tick(driver: _Driver) -> None:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    pass
def _driver_draw(driver: _Driver) -> None:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    raise "Not implemented"

# https://github.com/gui-cs/Terminal.Gui/blob/develop/Terminal.Gui/Core/TextFormatter.cs
_TextHorizontalAlignment = Union[
    Literal["Left"],
    Literal["Right"],
    Literal["Center"],
    Literal["Justified"]
]
_TextVerticalAlignment = Union[
    Literal["Top"],
    Literal["Bottom"],
    Literal["Middle"],
    Literal["Justified"]
]
_TextDirection = Union[
    Literal["LeftRight_TopBottom"],
    Literal["TopBottom_LeftRight"],
    Literal["RightLeft_TopBottom"],
    Literal["TopBottom_RightLeft"],
    Literal["LeftRight_BottomTop"],
    Literal["BottomTop_LeftRight"],
    Literal["RightLeft_BottomTop"],
    Literal["BottomTop_RightLeft"]
]

def _text_direction_is_horizontal(direction: _TextDirection) -> bool:
    if direction == "LeftRight_TopBottom":
        return True
    if direction == "LeftRight_BottomTop":
        return True
    if direction == "RightLeft_TopBottom":
        return True
    if direction == "RightLeft_BottomTop":
        return True
    return False
def _text_direction_is_vertical(direction: _TextDirection) -> bool:
    if direction == "TopBottom_LeftRight":
        return True
    if direction == "TopBottom_RightLeft":
        return True
    if direction == "BottomTop_LeftRight":
        return True
    if direction == "BottomTop_RightLeft":
        return True
    return False
def _text_direction_is_left_to_right(direction: _TextDirection) -> bool:
    if direction == "LeftRight_TopBottom":
        return True
    if direction == "LeftRight_BottomTop":
        return True
    if direction == "TopBottom_LeftRight":
        return True
    if direction == "BottomTop_LeftRight":
        return True
    return False
def _text_direction_is_top_to_bottom(direction: _TextDirection) -> bool:
    if direction == "TopBottom_LeftRight":
        return True
    if direction == "TopBottom_RightLeft":
        return True
    if direction == "LeftRight_TopBottom":
        return True
    if direction == "RightLeft_TopBottom":
        return True
    return False

_TextFormatter = TypedDict("TextFormatter",
    driver=_Driver,
    text=list[_Rune],
    autoSize=bool,
    size=Size,
    multiline=bool,
    wordwrap=bool,
    direction=_TextDirection,
    horizontalAlignment=_TextHorizontalAlignment,
    verticalAlignment=_TextVerticalAlignment,
    lines=list[list[_Rune]],
    recompute=bool
)
def _text_formatter_new(driver: _Driver) -> _TextFormatter:
    return dict(
        driver=driver,
        text="",
        autoSize=True,
        size=Size(0, 0),
        multiline=True,
        wordwrap=True,
        direction="LeftRight_TopBottom",
        horizontalAlignment="Left",
        verticalAlignment="Top",
        lines=[],
        recompute=False
    )
def _text_formatter_get_text(textFormatter: _TextFormatter) -> list[_Rune]:
    return textFormatter["text"]
def _text_formatter_get_auto_size(textFormatter: _TextFormatter) -> bool:
    return textFormatter["autoSize"]
def _text_formatter_get_size(textFormatter: _TextFormatter) -> Size:
    return textFormatter["size"]
def _text_formatter_get_multiline(textFormatter: _TextFormatter) -> bool:
    return textFormatter["multiline"]
def _text_formatter_get_wordwrap(textFormatter: _TextFormatter) -> bool:
    return textFormatter["wordwrap"]
def _text_formatter_get_direction(textFormatter: _TextFormatter) -> _TextDirection:
    return textFormatter["direction"]
def _text_formatter_get_horizontal_alignment(textFormatter: _TextFormatter) -> _TextHorizontalAlignment:
    return textFormatter["horizontalAlignment"]
def _text_formatter_get_vertical_alignment(textFormatter: _TextFormatter) -> _TextVerticalAlignment:
    return textFormatter["verticalAlignment"]
def _text_formatter_get_lines(textFormatter: _TextFormatter) -> list[list[_Rune]]:
    if not textFormatter["recompute"]:
        return textFormatter["lines"]
    lines = _text_formatter_get_computed_lines(textFormatter)
    textFormatter["lines"] = lines
    textFormatter["recompute"] = False
    return lines
def _text_formatter_set_text(textFormatter: _TextFormatter, text: list[_Rune]) -> None:
    textFormatter["text"] = text
    textFormatter["recompute"] = True
    if textFormatter["autoSize"]:
        textFormatter["size"] = _text_formatter_get_calculated_auto_size(textFormatter)
def _text_formatter_set_auto_size(textFormatter: _TextFormatter, autoSize: bool) -> None:
    textFormatter["autoSize"] = autoSize
    textFormatter["recompute"] = True
    if autoSize:
        textFormatter["size"] = _text_formatter_get_calculated_auto_size(textFormatter)
def _text_formatter_set_size(textFormatter: _TextFormatter, size: Size) -> None:
    if textFormatter["autoSize"]:
        return
    textFormatter["size"] = size
    textFormatter["recompute"] = True
def _text_formatter_set_multiline(textFormatter: _TextFormatter, multiline: bool) -> None:
    textFormatter["multiline"] = multiline
    textFormatter["recompute"] = True
def _text_formatter_set_wordwrap(textFormatter: _TextFormatter, wordwrap: bool) -> None:
    textFormatter["wordwrap"] = wordwrap
    textFormatter["recompute"] = True
def _text_formatter_set_direction(textFormatter: _TextFormatter, direction: _TextDirection) -> None:
    textFormatter["direction"] = direction
    textFormatter["recompute"] = True
    if textFormatter["autoSize"]:
        textFormatter["size"] = _text_formatter_get_calculated_auto_size(textFormatter)
def _text_formatter_set_horizontal_alignment(textFormatter: _TextFormatter, horizontalAlignment: _TextHorizontalAlignment) -> None:
    textFormatter["horizontalAlignment"] = horizontalAlignment
    textFormatter["recompute"] = True
def _text_formatter_set_vertical_alignment(textFormatter: _TextFormatter, verticalAlignment: _TextVerticalAlignment) -> None:
    textFormatter["verticalAlignment"] = verticalAlignment
    textFormatter["recompute"] = True

def _text_formatter_draw(textFormatter: _TextFormatter, screen: Rectangle) -> None:
    driver = textFormatter["driver"]
    direction = textFormatter["direction"]
    horizontalAlignment = textFormatter["horizontalAlignment"]
    verticalAlignment = textFormatter["verticalAlignment"]
    lines = _text_formatter_get_lines(textFormatter)
    def matchSizeIndexAtPosition(sizes: list[int], offsetIndex: int, position: int) -> int:
        index = offsetIndex
        current = 0
        while position > 0 and index < len(sizes):
            if current <= 0:
                current = sizes[index]
                index += 1
            current -= 1
            position -= 1
        if current == 0 and index < len(sizes):
            return index
        return None
    if _text_direction_is_horizontal(direction):
        lineSizes = array_map(lines, lambda l, *_: array_reduce(l, lambda c, r, *_: max(c, _driver_get_rune_height(driver, r, direction)), 0))
        lineTotalSize = array_reduce(lineSizes, lambda c, s, *_: c + s, 0)
        startY = 0
        if verticalAlignment == "Top" or verticalAlignment == "Justified":
            startY = screen.y
        if verticalAlignment == "Middle":
            startY = screen.y + (screen.h - lineTotalSize) // 2
        if verticalAlignment == "Bottom":
            startY = screen.y + screen.h - lineTotalSize
        lineOffset = 0
        if startY < 0:
            for i in range(8):
                lineOffset = matchSizeIndexAtPosition(lineSizes, 0, -startY + (i // 2) * (1 if i % 2 == 0 else -1))
                if lineOffset is not None:
                    break
            startY = 0
        endY = startY + min(lineTotalSize, screen.h)
        for y in range(startY, endY):
            lineIndex = matchSizeIndexAtPosition(lineSizes, lineOffset, y - startY)
            if lineIndex is None:
                continue
            text = lines[lineIndex]
            runeSizes = array_map(text, lambda r, *_: _driver_get_rune_width(driver, r, direction))
            textSize = array_reduce(runeSizes, lambda c, s, *_: c + s, 0)
            startX = 0
            if horizontalAlignment == "Left" or horizontalAlignment == "Justified":
                startX = screen.x
            if horizontalAlignment == "Center":
                startX = screen.x + (screen.w - textSize) // 2
            if horizontalAlignment == "Right":
                startX = screen.x + screen.w - textSize
            runeOffset = 0
            if startX < 0:
                for i in range(8):
                    runeOffset = matchSizeIndexAtPosition(runeSizes, 0, -startX + (i // 2) * (1 if i % 2 == 0 else -1))
                    if runeOffset is not None:
                        break
                startX = 0
            endX = startX + min(textSize, screen.w)
            for x in range(startX, endX):
                runeIndex = matchSizeIndexAtPosition(runeSizes, runeOffset, x - startX)
                if runeIndex is None:
                    continue
                rune = text[runeIndex]
                _driver_set_content(driver, x, y, rune)
    if _text_direction_is_vertical(direction):
        lineSizes = array_map(lines, lambda l, *_: array_reduce(l, lambda c, r, *_: max(c, _driver_get_rune_width(driver, r, direction)), 0))
        lineTotalSize = array_reduce(lineSizes, lambda c, s, *_: c + s, 0)
        startX = 0
        if horizontalAlignment == "Left" or horizontalAlignment == "Justified":
            startX = screen.x
        if horizontalAlignment == "Center":
            startX = screen.x + (screen.w - lineTotalSize) // 2
        if horizontalAlignment == "Right":
            startX = screen.x + screen.w - lineTotalSize
        lineOffset = 0
        if startX < 0:
            for i in range(8):
                lineOffset = matchSizeIndexAtPosition(lineSizes, 0, -startX + (i // 2) * (1 if i % 2 == 0 else -1))
                if lineOffset is not None:
                    break
            startX = 0
        endX = startX + min(lineTotalSize, screen.w)
        for x in range(startX, endX):
            lineIndex = matchSizeIndexAtPosition(lineSizes, lineOffset, x - startX)
            if lineIndex is None:
                continue
            text = lines[lineIndex]
            runeSizes = array_map(text, lambda r, *_: _driver_get_rune_height(driver, r, direction))
            textSize = array_reduce(runeSizes, lambda c, s, *_: c + s, 0)
            startY = 0
            if verticalAlignment == "Top" or verticalAlignment == "Justified":
                startY = screen.y
            if verticalAlignment == "Middle":
                startY = screen.y + (screen.h - textSize) // 2
            if verticalAlignment == "Bottom":
                startY = screen.y + screen.h - textSize
            runeOffset = 0
            if startY < 0:
                for i in range(8):
                    runeOffset = matchSizeIndexAtPosition(runeSizes, 0, -startY + (i // 2) * (1 if i % 2 == 0 else -1))
                    if runeOffset is not None:
                        break
                startY = 0
            endY = startY + min(textSize, screen.h)
            for y in range(startY, endY):
                runeIndex = matchSizeIndexAtPosition(runeSizes, runeOffset, y - startY)
                if runeIndex is None:
                    continue
                rune = text[runeIndex]
                _driver_set_content(driver, x, y, rune)
    pass
def _text_formatter_get_computed_lines(textFormatter: _TextFormatter) -> list[list[_Rune]]:
    driver = textFormatter["driver"]
    text = textFormatter["text"]
    multiline = textFormatter["multiline"]
    wordwrap = textFormatter["wordwrap"]
    direction = textFormatter["direction"]
    horizontalAlignment = textFormatter["horizontalAlignment"]
    verticalAlignment = textFormatter["verticalAlignment"]
    size = textFormatter["size"].w if _text_direction_is_horizontal(direction) else textFormatter["size"].h
    def reverseLinesBasedOnDirection(lines: list[list[_Rune]], direction: _TextDirection) -> list[list[_Rune]]:
        if _text_direction_is_horizontal(direction) and not _text_direction_is_top_to_bottom(direction):
            return array_to_reversed(lines)
        if _text_direction_is_vertical(direction) and not _text_direction_is_left_to_right(direction):
            return array_to_reversed(lines)
        return lines
    def reverseTextBasedOnDirection(text: list[_Rune], direction: _TextDirection) -> list[_Rune]:
        if _text_direction_is_horizontal(direction) and not _text_direction_is_left_to_right(direction):
            return array_to_reversed(text)
        if _text_direction_is_vertical(direction) and not _text_direction_is_top_to_bottom(direction):
            return array_to_reversed(text)
        return text
    def replaceCrlfWithSpace(text: list[_Rune]) -> list[_Rune]:
        result: list[_Rune] = []
        for rune in text:
            if rune.character != "\r\n" and rune.character != "\r" and rune.character != "\n":
                array_push(result, rune)
                continue
            array_push(result, _Rune(" ", rune.attribute))
        return result
    def replaceTabWithSpaces(text: list[_Rune], direction: _TextDirection, driver: _Driver) -> list[_Rune]:
        result: list[_Rune] = []
        for rune in text:
            if rune.character != "\t":
                array_push(result, rune)
                continue
            tabSize = getRuneSize(rune, direction, driver)
            spaceRune = _Rune(" ", rune.attribute)
            for _ in range(tabSize):
                array_push(result, spaceRune)
        return result
    def splitRunes(text: list[_Rune], by: list[str]) -> tuple[list[list[_Rune]], list[int]]:
        result: list[list[_Rune]] = []
        indices: list[int] = []
        lastIndex = -1
        for i in range(len(text)):
            if not array_includes(by, text[i].character):
                continue
            array_push(result, array_slice(text, lastIndex + 1, i))
            array_push(indices, lastIndex)
            lastIndex = i
        if lastIndex < len(text) - 1:
            array_push(result, array_slice(text, lastIndex + 1))
            array_push(indices, lastIndex)
        return (result, indices)
    def getRuneSize(rune: _Rune, direction: _TextDirection, driver: _Driver) -> int:
        if _text_direction_is_horizontal(direction):
            return _driver_get_rune_width(driver, rune, direction)
        if _text_direction_is_vertical(direction):
            return _driver_get_rune_height(driver, rune, direction)
        return 0
    def findCumulativeIndex(sizes: list[int], start: int, targetSize: int) -> int:
        current = 0
        for i in range(start, len(sizes)):
            size = sizes[i]
            if current + size > targetSize:
                return i
            current += size
        return len(sizes)
    def justify(text: list[_Rune], size: int, direction: _TextDirection, driver: _Driver) -> list[_Rune]:
        words, wordIndices = splitRunes(text, [" "])
        textSizeWithoutSpace = array_reduce(words, lambda s, w, *_: s + array_reduce(w, lambda c, r, *_: c + getRuneSize(r, direction, driver), 0), 0)
        spaces = (size - textSizeWithoutSpace) // (len(words) - 1) if len(words) > 1 else 1
        extras = (size - textSizeWithoutSpace) % (len(words) - 1) if len(words) > 1 else 0
        result: list[_Rune] = []
        i = 0
        while i < len(words):
            word = words[i]
            if len(word) > 0:
                array_push(result, *word)
                spaceRune = text[wordIndices[i + 1]] if i + 1 < len(wordIndices) else _Rune(" ", word[len(word) - 1].attribute)
                if i + 1 < len(words):
                    for _ in range(spaces):
                        array_push(result, spaceRune)
                if extras > 0:
                    array_push(result, spaceRune)
                    extras -= 1
                i += 1
                continue
            startIndex = i
            while i + 1 < len(words) and len(words[i + 1]) == 0:
                i += 1
            spacesBetween = i - startIndex + 1
            remainingSpaces = (spaces + (1 if extras > 0 else 0)) - spacesBetween
            additionalSpaces = remainingSpaces // spacesBetween
            extraSpaces = remainingSpaces % spacesBetween
            for j in range(spacesBetween):
                spaceRune = text[wordIndices[startIndex + j]]
                array_push(result, spaceRune)
                for _ in range(additionalSpaces):
                    array_push(result, spaceRune)
                if extraSpaces > 0:
                    array_push(result, spaceRune)
                    extraSpaces -= 1
            i += 1
        return result
    def clipAndJustify(text: list[_Rune], size: int, direction: _TextDirection, horizontalAlignment: _TextHorizontalAlignment, verticalAlignment: _TextVerticalAlignment, driver: _Driver) -> list[_Rune]:
        runeSizes = array_map(text, lambda r, *_: getRuneSize(r, direction, driver))
        textSize = array_reduce(runeSizes, lambda c, s, *_: c + s, 0)
        if textSize > size:
            if((_text_direction_is_horizontal(direction) and horizontalAlignment == "Center") or 
               (_text_direction_is_vertical(direction) and verticalAlignment == "Middle")):
                startIndex = findCumulativeIndex(runeSizes, 0, (textSize - size) // 2)
                endIndex = findCumulativeIndex(runeSizes, startIndex, size)
                return array_slice(text, startIndex, endIndex)
            if((_text_direction_is_horizontal(direction) and horizontalAlignment == "Right") or 
               (_text_direction_is_vertical(direction) and verticalAlignment == "Bottom")):
                startIndex = findCumulativeIndex(runeSizes, 0, textSize - size)
                endIndex = findCumulativeIndex(runeSizes, startIndex, size)
                return array_slice(text, startIndex, endIndex)
            startIndex = 0
            endIndex = findCumulativeIndex(runeSizes, startIndex, size)
            return array_slice(text, startIndex, endIndex)
        if((_text_direction_is_horizontal(direction) and horizontalAlignment == "Justified") or 
           (_text_direction_is_vertical(direction) and verticalAlignment == "Justified")):
            return justify(text, size, direction, driver)
        return text
    def wordWrap(text: list[_Rune], size: int, direction: _TextDirection, driver: _Driver) -> list[list[_Rune]]:
        runeSizes = array_map(text, lambda r, *_: getRuneSize(r, direction, driver))
        lines: list[list[_Rune]] = []
        startIndex = 0
        while startIndex < len(text):
            endIndex = findCumulativeIndex(runeSizes, startIndex, size)
            if endIndex < len(text) and text[endIndex].character != " ":
                spaceIndex = endIndex
                while spaceIndex > startIndex and text[spaceIndex].character != " ":
                    spaceIndex -= 1
                if spaceIndex != startIndex:
                    endIndex = spaceIndex
            if endIndex == startIndex:
                endIndex += 1
            array_push(lines, array_slice(text, startIndex, endIndex))
            startIndex = endIndex
        return lines
    lines: list[list[_Rune]] = []
    if not wordwrap:
        text = replaceTabWithSpaces(text, direction, driver)
        if not multiline:
            text = replaceCrlfWithSpace(text)
            text = reverseTextBasedOnDirection(text, direction)
            text = clipAndJustify(text, size, direction, horizontalAlignment, verticalAlignment, driver)
            array_push(lines, text)
            return reverseLinesBasedOnDirection(lines, direction)
        splittedLines = splitRunes(text, ["\r\n", "\r", "\n"])[0]
        for splittedLine in splittedLines:
            splittedLine = reverseTextBasedOnDirection(splittedLine, direction)
            splittedLine = clipAndJustify(splittedLine, size, direction, horizontalAlignment, verticalAlignment, driver)
            array_push(lines, splittedLine)
        return reverseLinesBasedOnDirection(lines, direction)
    splittedLines = splitRunes(text, ["\r\n", "\r", "\n"])[0]
    for splittedLine in splittedLines:
        wrappedLines = reverseTextBasedOnDirection(splittedLine, direction)
        wrappedLines = wordWrap(wrappedLines, size, direction, driver)
        if len(wrappedLines) == 0:
            array_push(lines, [])
            continue
        for wrappedLine in wrappedLines:
            wrappedLine = replaceTabWithSpaces(wrappedLine, direction, driver)
            wrappedLine = clipAndJustify(wrappedLine, size, direction, horizontalAlignment, verticalAlignment, driver)
            array_push(lines, wrappedLine)
    return reverseLinesBasedOnDirection(lines, direction)
def _text_formatter_get_calculated_auto_size(textFormatter: _TextFormatter) -> Size:
    driver = textFormatter["driver"]
    text = textFormatter["text"]
    direction = textFormatter["direction"]
    width = 0
    height = 0
    if _text_direction_is_horizontal(direction):
        currentWidth = 0
        currentMaxHeight = 0
        for rune in text:
            if rune.character == "\r\n" or rune.character == "\r" or rune.character == "\n":
                width = max(width, currentWidth)
                height += currentMaxHeight
                continue
            currentWidth += _driver_get_rune_width(driver, rune, direction)
            currentMaxHeight = max(currentMaxHeight, _driver_get_rune_height(driver, rune, direction))
        width = max(width, currentWidth)
        height += currentMaxHeight
    if _text_direction_is_vertical(direction):
        currentHeight = 0
        currentMaxWidth = 0
        for rune in text:
            if rune.character == "\r\n" or rune.character == "\r" or rune.character == "\n":
                height = max(height, currentHeight)
                width += currentMaxWidth
                continue
            currentHeight += _driver_get_rune_height(driver, rune, direction)
            currentMaxWidth = max(currentMaxWidth, _driver_get_rune_width(driver, rune, direction))
        height = max(height, currentHeight)
        width += currentMaxWidth
    return Size(width, height)

_LayoutStyle = Union[
    Literal["Absolute"],
    Literal["Computed"]
]

_View = TypedDict("View",
    x=_Pos,
    y=_Pos,
    width=_Dim,
    height=_Dim,
    frame=Rectangle,
    layoutStyle=_LayoutStyle,
    autoSize=bool,
    forceValidatePosDim=bool,
    subviews=list["_View"]
)

def _view_get_x(view: _View) -> _Pos:
    return view["x"]
def _view_get_y(view: _View) -> _Pos:
    return view["y"]
def _view_get_width(view: _View) -> _Dim:
    return view["width"]
def _view_get_height(view: _View) -> _Dim:
    return view["height"]
def _view_get_frame(view: _View) -> Rectangle:
    return view["frame"]
def _view_get_layout_style(view: _View) -> _LayoutStyle:
    return view["layoutStyle"]
def _view_get_auto_size(view: _View) -> bool:
    return view["autoSize"]
def _view_get_force_validate_pos_dim(view: _View) -> bool:
    return view["forceValidatePosDim"]
def _view_get_bounds(view: _View) -> Rectangle:
    return rectangle_from_point_size(EmptyPoint, rectangle_get_size(_view_get_frame(view)))
def _view_set_x(view: _View, x: _Pos) -> None:
    if view["forceValidatePosDim"] and not _view_validate_pos_dim(view, view["x"], x):
        raise "ArgumentException"
    view["x"] = x
    _view_recompute_resize(view)
def _view_set_y(view: _View, y: _Pos) -> None:
    if view["forceValidatePosDim"] and not _view_validate_pos_dim(view, view["y"], y):
        raise "ArgumentException"
    view["y"] = y
    _view_recompute_resize(view)
def _view_set_width(view: _View, width: _Dim) -> None:
    if view["forceValidatePosDim"] and not _view_validate_pos_dim(view, view["width"], width):
        raise "ArgumentException"
    view["width"] = width
    _view_recompute_resize(view)
def _view_set_height(view: _View, height: _Dim) -> None:
    if view["forceValidatePosDim"] and not _view_validate_pos_dim(view, view["height"], height):
        raise "ArgumentException"
    view["height"] = height
    _view_recompute_resize(view)
def _view_set_frame(view: _View, frame: Rectangle) -> None:
    view["frame"] = frame
    _view_recompute_layout(view)
    _view_recompute_display(view)
def _view_set_layout_style(view: _View, layoutStyle: _LayoutStyle) -> None:
    view["layoutStyle"] = layoutStyle
    _view_recompute_layout(view)
def _view_set_auto_size(view: _View, autoSize: bool) -> None:
    view["autoSize"] = autoSize
    _view_recompute_resize(view)
def _view_set_force_validate_pos_dim(view: _View, forceValidatePosDim: bool) -> None:
    view["forceValidatePosDim"] = forceValidatePosDim
def _view_set_bounds(view: _View, bounds: Rectangle) -> None:
    _view_set_frame(view, rectangle_from_point_size(rectangle_get_point(_view_get_frame(view)), rectangle_get_size(bounds)))

def _view_validate_pos_dim(view: _View, oldValue: Any, newValue: Any) -> bool:
    if view["layoutStyle"] == "Absolute":
        return True
    if _pos_as_absolute(newValue) is None and _dim_as_absolute(newValue) is None:
        return True
    return False
def _view_recompute_resize(view: _View) -> None:
    _view_recompute_layout()
    _view_recompute_display()
def _view_recompute_layout(view: _View) -> None:
    # TODO
    pass
def _view_recompute_display(view: _View) -> None:
    # TODO
    pass
