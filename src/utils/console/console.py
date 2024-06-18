from utils.math import *
from utils.primordials import *
from utils.mixin import *
from typing import TypedDict, Any, Callable, Union, Literal, NamedTuple, Optional
from math import inf

_Direction = Union[
    Literal["Abscissa"],
    Literal["Ordinate"]
]

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
    offset=Optional[float]
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
def _pos_from_end(offset: Optional[float] = None) -> _PosEnd:
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
    return int(pos["factor"] * scalar)
def _pos_center_anchor(pos: _PosCenter, scalar: float) -> float:
    return int(scalar / 2)
def _pos_end_anchor(pos: _PosEnd, scalar: float) -> float:
    offset = pos["offset"]
    return scalar - (offset if offset is not None else 0)
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

def _pos_calculate(pos: _Pos, scalar: float, direction: _Direction, dim: "_Dim", view: "_View") -> float:
    if _pos_as_absolute(pos) is not None:
        return _pos_absolute_calculate(pos, scalar, direction, dim, view)
    if _pos_as_factor(pos) is not None:
        return _pos_factor_calculate(pos, scalar, direction, dim, view)
    if _pos_as_center(pos) is not None:
        return _pos_center_calculate(pos, scalar, direction, dim, view)
    if _pos_as_end(pos) is not None:
        return _pos_end_calculate(pos, scalar, direction, dim, view)
    if _pos_as_combine(pos) is not None:
        return _pos_combine_calculate(pos, scalar, direction, dim, view)
    if _pos_as_view(pos) is not None:
        return _pos_view_calculate(pos, scalar, direction, dim, view)
    if _pos_as_function(pos) is not None:
        return _pos_function_calculate(pos, scalar, direction, dim, view)
def _pos_absolute_calculate(pos: _PosAbsolute, scalar: float, direction: _Direction, dim: "_Dim", view: "_View") -> float:
    return _pos_absolute_anchor(pos, scalar)
def _pos_factor_calculate(pos: _PosFactor, scalar: float, direction: _Direction, dim: "_Dim", view: "_View") -> float:
    return _pos_factor_anchor(pos, scalar)
def _pos_center_calculate(pos: _PosCenter, scalar: float, direction: _Direction, dim: "_Dim", view: "_View") -> float:
    result = max(0, _dim_calculate(dim, scalar, direction, 0, view))
    result = _pos_center_anchor(pos, scalar - result)
    return result
def _pos_end_calculate(pos: _PosEnd, scalar: float, direction: _Direction, dim: "_Dim", view: "_View") -> float:
    offset = pos["offset"]
    result = _pos_end_anchor(pos, scalar)
    if offset is not None:
        return result - offset
    return result - _dim_anchor(dim, scalar)
def _pos_combine_calculate(pos: _PosCombine, scalar: float, direction: _Direction, dim: "_Dim", view: "_View") -> float:
    leftAnchor = _pos_calculate(pos["left"], scalar, direction, dim, view)
    rightAnchor = _pos_calculate(pos["right"], scalar, direction, dim, view)
    return leftAnchor + rightAnchor if pos["add"] else leftAnchor - rightAnchor
def _pos_view_calculate(pos: _PosView, scalar: float, direction: _Direction, dim: "_Dim", view0: "_View") -> float:
    view = pos["view"]
    side = pos["side"]
    frame = view["frame"]
    offset = _view_transform_frame_to_superview(view, view0["superview"])
    if side == 0:
        return offset.x
    if side == 1:
        return offset.y
    if side == 2:
        return offset.x + frame.w
    if side == 3:
        return offset.y + frame.h
    return None
def _pos_function_calculate(pos: _PosFunction, scalar: float, direction: _Direction, dim: "_Dim", view: "_View") -> float:
    return _pos_function_anchor(pos, scalar)

def _pos_add(left: _Pos, right: _Pos) -> _Pos:
    if _pos_as_absolute(left) is not None and _pos_as_absolute(right) is not None:
        return _pos_from_absolute(_pos_anchor(left, 0) + _pos_anchor(right, 0))
    return _pos_from_combine(True, left, right)
def _pos_sub(left: _Pos, right: _Pos) -> _Pos:
    if _pos_as_absolute(left) is not None and _pos_as_absolute(right) is not None:
        return _pos_from_absolute(_pos_anchor(left, 0) - _pos_anchor(right, 0))
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
    Literal["Function"],
    Literal["Auto"]
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
_DimAutoMode = Union[
    Literal["Text"],
    Literal["Content"],
    Literal["Text|Content"],
]
_DimAuto = TypedDict("Dim",
    type=Literal["Auto"],
    mode=_DimAutoMode,
    min=Optional[_Dim],
    max=Optional[_Dim]
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
def _dim_from_auto(mode: _DimAutoMode, min: Optional[_Dim] = None, max: Optional[_Dim] = None) -> _DimAuto:
    return dict(
        type="Auto",
        mode=mode,
        min=min,
        max=max
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
def _dim_as_auto(dim: _Dim) -> Union[None, _DimAuto]:
    return dim if dim["type"] == "Auto" else None

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
    if _dim_as_auto(dim) is not None:
        return _dim_auto_anchor(dim, scalar)
def _dim_absolute_anchor(dim: _DimAbsolute, scalar: float) -> float:
    return dim["absolute"]
def _dim_factor_anchor(dim: _DimFactor, scalar: float) -> float:
    return int(dim["factor"] * scalar)
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
def _dim_auto_anchor(dim: _DimAuto, scalar: float) -> float:
    return 0

def _dim_calculate(dim: _Dim, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    if _dim_as_absolute(dim) is not None:
        return _dim_absolute_calculate(dim, scalar, direction, position, view)
    if _dim_as_factor(dim) is not None:
        return _dim_factor_calculate(dim, scalar, direction, position, view)
    if _dim_as_fill(dim) is not None:
        return _dim_fill_calculate(dim, scalar, direction, position, view)
    if _dim_as_combine(dim) is not None:
        return _dim_combine_calculate(dim, scalar, direction, position, view)
    if _dim_as_view(dim) is not None:
        return _dim_view_calculate(dim, scalar, direction, position, view)
    if _dim_as_function(dim) is not None:
        return _dim_function_calculate(dim, scalar, direction, position, view)
    if _dim_as_auto(dim) is not None:
        return _dim_auto_calculate(dim, scalar, direction, position, view)
def _dim_absolute_calculate(dim: _DimAbsolute, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    return max(0, _dim_absolute_anchor(dim, 0))
def _dim_factor_calculate(dim: _DimFactor, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    return _dim_factor_anchor(dim, scalar)
def _dim_fill_calculate(dim: _DimFill, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    return max(0, _dim_fill_anchor(dim, scalar - position))
def _dim_combine_calculate(dim: _DimCombine, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    leftAnchor = _dim_calculate(dim["left"], scalar, direction, position, view)
    rightAnchor = _dim_calculate(dim["right"], scalar, direction, position, view)
    return leftAnchor + rightAnchor if dim["add"] else max(0, leftAnchor - rightAnchor)
def _dim_view_calculate(dim: _DimView, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    return max(0, _dim_view_anchor(dim, scalar - position))
def _dim_function_calculate(dim: _DimFunction, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    return max(0, _dim_function_anchor(dim, scalar - position))
def _dim_auto_calculate(dim: _DimAuto, scalar: float, direction: _Direction, position: float, view: "_View") -> float:
    mode = dim["mode"]
    minAuto = _dim_anchor(dim["min"], scalar) if dim["min"] is not None else 0
    maxAuto = _dim_anchor(dim["max"], scalar) if dim["max"] is not None else scalar
    if minAuto > scalar:
        return scalar
    textSize = 0
    subviewsSize = 0
    if mode == "Text" or mode == "Text|Content":
        textFormatter = _view_get_text_formatter(view)
        textFormatterSize = _text_formatter_get_size(textFormatter)
        textSize = textFormatterSize.w if direction == "Abscissa" else textFormatterSize.h
    if mode == "Content" or mode == "Text|Content":
        internalContentSize = view["contentSize"] # this is illegal
        if internalContentSize is not None:
            subviewsSize = internalContentSize.w if direction == "Abscissa" else internalContentSize.h
        else:
            subviews = view["subviews"] # this is illegal
            for subview in subviews:
                if direction == "Abscissa" and _pos_as_end(_view_get_x(subview)) is not None:
                    continue
                if direction == "Ordinate" and _pos_as_end(_view_get_y(subview)) is not None:
                    continue
                subviewFrame = _view_get_frame(view)
                subviewSize = subviewFrame.x + subviewFrame.w if direction == "Abscissa" else subviewFrame.y + subviewFrame.h
                if subviewSize > subviewsSize:
                    subviewsSize = subviewSize
    result = max(textSize, subviewsSize)
    marginThickness = _adornment_get_thickness(_view_get_margin(view))
    borderThickness = _adornment_get_thickness(_view_get_border(view))
    paddingThickness = _adornment_get_thickness(_view_get_padding(view))
    totalThickness = _thickness_add(_thickness_add(marginThickness, borderThickness), paddingThickness)
    result += _thickness_get_horizontal(totalThickness) if direction == "Abscissa" else _thickness_get_vertical(totalThickness)
    result = max(minAuto, min(maxAuto, result))
    return result

def _dim_add(left: _Dim, right: _Dim) -> _Dim:
    if _dim_as_absolute(left) is not None and _dim_as_absolute(right) is not None:
        return _dim_from_absolute(_dim_anchor(left, 0) + _dim_anchor(right, 0))
    return _dim_from_combine(True, left, right)
def _dim_sub(left: _Dim, right: _Dim) -> _Dim:
    if _dim_as_absolute(left) is not None and _dim_as_absolute(right) is not None:
        return _dim_from_absolute(_dim_anchor(left, 0) - _dim_anchor(right, 0))
    return _dim_from_combine(False, left, right)
def _dim_from_view_width(view: "_View") -> _Dim:
    return _dim_from_view(view, 0)
def _dim_from_view_height(view: "_View") -> _Dim:
    return _dim_from_view(view, 1)

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
    dirtyLines=list[int]
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
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    return driver["size"]
def _driver_get_attribtue(driver: _Driver) -> _DriverAttribute:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    return driver["attribute"]
def _driver_get_rune_width(driver: _Driver, rune: _Rune, direction: "_TextDirection") -> int:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    attribute = driver["attribute"]
    if rune.character == "\t" and _text_direction_is_horizontal(direction):
        return attribute.tabSize
    return 1
def _driver_get_rune_height(driver: _Driver, rune: _Rune, direction: "_TextDirection") -> int:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    attribute = driver["attribute"]
    if rune.character == "\t" and _text_direction_is_vertical(direction):
        return attribute.tabSize
    return 1
def _driver_set_size(driver: _Driver, size: Size) -> None:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    driver["size"] = size
    driver["contents"] = [_Rune_clear for _ in range(size.w * size.h)]
    driver["dirtyLines"] = [inf for _ in range(size.h)]
def _driver_set_content(driver: _Driver, x: int, y: int, rune: _Rune) -> None:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    size = driver["size"]
    contents = driver["contents"]
    dirtyLines = driver["dirtyLines"]
    if x < 0 or y < 0 or x >= size.w or y >= size.h:
        return
    contents[y * size.w + x] = rune
    dirtyLines[y] = min(x, dirtyLines[y])
def _driver_clear_content(driver: _Driver, x: int, y: int) -> None:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    _driver_set_content(driver, x, y, _Rune_clear)
def _driver_fill_rect(driver: _Driver, rectangle: Rectangle, rune: _Rune) -> None:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    size = driver["size"]
    contents = driver["contents"]
    dirtyLines = driver["dirtyLines"]
    driverBounds = rectangle_from_point_size(EmptyPoint, size)
    bounds = rectangle_intersect(driverBounds, rectangle)
    if bounds.w == 0 or bounds.h == 0:
        return
    for y in range(bounds.y, bounds.y + bounds.h):
        for x in range(bounds.x, bounds.x + bounds.w):
            contents[y * size.w + x] = rune
        dirtyLines[y] = min(bounds.x, dirtyLines[y])
def _driver_clear_rect(driver: _Driver, rectangle: Rectangle = None) -> None:
    if mixin_is_override(driver):
        return mixin_call_override(driver)
    if rectangle is None:
        rectangle = rectangle_from_point_size(EmptyPoint, driver["size"])
    _driver_fill_rect(driver, rectangle, _Rune_clear)
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
        text=[],
        autoSize=False,
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
    lines = __text_formatter_get_computed_lines(textFormatter)
    textFormatter["lines"] = lines
    textFormatter["recompute"] = False
    return lines
def _text_formatter_set_text(textFormatter: _TextFormatter, text: list[_Rune]) -> None:
    textFormatter["text"] = text
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True
    if textFormatter["autoSize"]:
        textFormatter["size"] = _text_formatter_get_calculated_auto_size(textFormatter)
def _text_formatter_set_auto_size(textFormatter: _TextFormatter, autoSize: bool) -> None:
    if autoSize == textFormatter["autoSize"]:
        return
    textFormatter["autoSize"] = autoSize
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True
    if autoSize:
        textFormatter["size"] = _text_formatter_get_calculated_auto_size(textFormatter)
def _text_formatter_set_size(textFormatter: _TextFormatter, size: Size) -> None:
    if textFormatter["autoSize"] or size == textFormatter["size"]:
        return
    textFormatter["size"] = size
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True
def _text_formatter_set_multiline(textFormatter: _TextFormatter, multiline: bool) -> None:
    if multiline == textFormatter["multiline"]:
        return
    textFormatter["multiline"] = multiline
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True
def _text_formatter_set_wordwrap(textFormatter: _TextFormatter, wordwrap: bool) -> None:
    if wordwrap == textFormatter["wordwrap"]:
        return
    textFormatter["wordwrap"] = wordwrap
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True
def _text_formatter_set_direction(textFormatter: _TextFormatter, direction: _TextDirection) -> None:
    if direction == textFormatter["direction"]:
        return
    textFormatter["direction"] = direction
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True
    if textFormatter["autoSize"]:
        textFormatter["size"] = _text_formatter_get_calculated_auto_size(textFormatter)
def _text_formatter_set_horizontal_alignment(textFormatter: _TextFormatter, horizontalAlignment: _TextHorizontalAlignment) -> None:
    if horizontalAlignment == textFormatter["horizontalAlignment"]:
        return
    textFormatter["horizontalAlignment"] = horizontalAlignment
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True
def _text_formatter_set_vertical_alignment(textFormatter: _TextFormatter, verticalAlignment: _TextVerticalAlignment) -> None:
    if verticalAlignment == textFormatter["verticalAlignment"]:
        return
    textFormatter["verticalAlignment"] = verticalAlignment
    textFormatter["recompute"] = True
    textFormatter["__unstable_has_changed"] = True

def _text_formatter_draw(textFormatter: _TextFormatter, screen: Rectangle) -> None:
    if "__unstable_has_changed" not in textFormatter or not textFormatter["__unstable_has_changed"]:
        return
    driver = textFormatter["driver"]
    direction = textFormatter["direction"]
    horizontalAlignment = textFormatter["horizontalAlignment"]
    verticalAlignment = textFormatter["verticalAlignment"]
    lines = _text_formatter_get_lines(textFormatter)
    textFormatter["__unstable_has_changed"] = False
    def matchSizeIndexAtPosition(sizes: list[int], offsetIndex: int, position: int) -> int:
        index = offsetIndex
        current = 0
        while position > 0 and index < len(sizes):
            if current <= 0:
                current = sizes[index]
                index += 1
            current -= 1
            position -= 1
        if position == 0 and index < len(sizes):
            return index
        return None
    if _text_direction_is_horizontal(direction):
        lineSizes = array_map(lines, lambda l, *_: array_reduce(l, lambda c, r, *_: max(c, _driver_get_rune_height(driver, r, direction)), 1))
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
            for i in range(32):
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
                for i in range(32):
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
        lineSizes = array_map(lines, lambda l, *_: array_reduce(l, lambda c, r, *_: max(c, _driver_get_rune_width(driver, r, direction)), 1))
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
            for i in range(32):
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
                for i in range(32):
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
def __text_formatter_get_computed_lines(textFormatter: _TextFormatter) -> list[list[_Rune]]:
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

# I don't like how the original repository is handling positions and sizes.
# The code uses ambiguous variable access in which may/may-not have side effects and thus even utterly-deranged person wouldn't event want to use it.
# And since, it will take way longer to come up with different idea (in which much inspired with css way of handling), I decided
# to continue in this manner. But please, my future self, cleanup this code (I do really hope I can reuse this in another project)
# This is a lot of hack (and by a lot, I mean it), and not many of them even handle things correctly.
# The code is also not really extensible.

_Thickness = NamedTuple("Thickness", [
    ("left", int),
    ("top", int),
    ("right", int),
    ("bottom", int)
])
_EmptyThickness = _Thickness(0, 0, 0, 0)

def _thickness_new(left: int, top: int, right: int, bottom: int) -> _Thickness:
    return _Thickness(left, top, right, bottom)
def _thickness_get_horizontal(thickness: _Thickness) -> int:
    return thickness.left + thickness.right
def _thickness_get_vertical(thickness: _Thickness) -> int:
    return thickness.top + thickness.bottom
def _thickness_compute_inside(thickness: _Thickness, outside: Rectangle) -> Rectangle:
    x = outside.x + thickness.left
    y = outside.y + thickness.top
    width = max(0, outside.w - (thickness.left + thickness.right))
    height = max(0, outside.h - (thickness.top + thickness.bottom))
    return Rectangle(x, y, width, height)
def _thickness_compute_outside(thickness: _Thickness, inside: Rectangle) -> Rectangle:
    x = inside.x - thickness.left
    y = inside.y - thickness.top
    width = inside.w + (thickness.left + thickness.right)
    height = inside.h + (thickness.top + thickness.bottom)
    return Rectangle(x, y, width, height)
def _thickness_draw(thickness: _Thickness, driver: _Driver, rectangle: Rectangle, rune: _Rune) -> None:
    left = thickness.left
    top = thickness.top
    right = thickness.right
    bottom = thickness.bottom
    _driver_fill_rect(driver, rectangle_from_point_size(rectangle_get_point(rectangle), Size(min(rectangle.w, left), rectangle.h)), rune)
    _driver_fill_rect(driver, rectangle_from_point_size(rectangle_get_point(rectangle), Size(rectangle.w, min(rectangle.h, top))), rune)
    _driver_fill_rect(driver, rectangle_from_point_size(Point(rectangle.x + max(0, rectangle.w - right), rectangle.y), Size(min(rectangle.w, right), rectangle.h)), rune)
    _driver_fill_rect(driver, rectangle_from_point_size(Point(rectangle.x, rectangle.y + max(0, rectangle.h - bottom)), Size(rectangle.w, min(rectangle.h, bottom))), rune)
def _thickness_with_horizontal(thickness: _Thickness, value: int) -> _Thickness:
    return _Thickness(value // 2, thickness.top, value // 2, thickness.bottom)
def _thickness_with_vertical(thickness: _Thickness, value: int) -> _Thickness:
    return _Thickness(thickness.left, value // 2, thickness.right, value // 2)
def _thickness_eq(left: _Thickness, right: _Thickness) -> bool:
    return left.left == right.left and left.top == right.top and left.right == right.right and left.bottom == right.bottom
def _thickness_neq(left: _Thickness, right: _Thickness) -> bool:
    return left.left != right.left or left.top != right.top or left.right != right.right or left.bottom != right.bottom
def _thickness_add(left: _Thickness, right: _Thickness) -> _Thickness:
    return _Thickness(left.left + right.left, left.top + right.top, left.right + right.right, left.bottom + right.bottom)
def _thickness_sub(left: _Thickness, right: _Thickness) -> _Thickness:
    return _Thickness(left.left - right.left, left.top - right.top, left.right - right.right, left.bottom - right.bottom)

_Adornment = TypedDict("Adornment",
    driver=_Driver,
    frame=Rectangle,
    thickness=_Thickness,
    viewportPosition=Point, # Bounded by contentSize
    viewportSize=Size, # Bounded by contentSize
    superview="_View",
    subviews=list["_View"],
    recomputeViewportSize=bool,
    recomputeLayout=bool,
    recomputeDisplay=Rectangle,
)

def _adornment_new(driver: _Driver, superview: "_View", **kwargs) -> _Adornment:
    return dict(
        driver=driver,
        frame=EmptyRectangle,
        thickness=_EmptyThickness,
        viewportPosition=EmptyPoint,
        viewportSize=EmptySize,
        superview=superview,
        subviews=[],
        recomputeViewportSize=True,
        recomputeLayout=True,
        recomputeDisplay=EmptyRectangle,
        **mixin_new(kwargs)
    )
def _adornment_get_frame(adornment: _Adornment) -> Rectangle:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    return adornment["frame"]
def _adornment_get_thickness(adornment: _Adornment) -> _Thickness:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    return adornment["thickness"]
def _adornment_get_viewport_position(adornment: _Adornment) -> Point:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    return adornment["viewportPosition"]
def _adornment_get_viewport_size(adornment: _Adornment) -> Size:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    if adornment["recomputeViewportSize"]:
        _adornment_recompute_viewport_size(adornment)
    return adornment["viewportSize"]
def _adornment_set_frame(adornment: _Adornment, frame: Rectangle) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    adornment["frame"] = frame
    _adornment_mark_recompute_viewport_size(adornment)
    _adornment_mark_recompute_layout(adornment)
def _adornment_set_thickness(adornment: _Adornment, thickness: _Thickness) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    adornment["thickness"] = thickness
    _adornment_mark_recompute_viewport_size(adornment)
    _adornment_mark_recompute_layout(adornment)
    _view_mark_recompute_viewport_size(adornment["superview"])
    _view_mark_recompute_layout(adornment["superview"])
def _adornment_set_viewport_position(adornment: _Adornment, viewportPosition: Point) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    adornment["viewportPosition"] = viewportPosition
    _adornment_mark_recompute_display(adornment)
def _adornment_set_viewport_size(adornment: _Adornment, viewportSize: Size) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    frame = adornment["frame"]
    thickness = adornment["thickness"]
    horizontalThickness = _thickness_get_horizontal(thickness)
    verticalThickness = _thickness_get_vertical(thickness)
    newFrameSize = Size(viewportSize.w + horizontalThickness, viewportSize.h + verticalThickness)
    newFrame = rectangle_from_point_size(rectangle_get_point(frame), newFrameSize)
    _adornment_set_frame(newFrame)
    adornment["viewportSize"] = viewportSize
    adornment["recomputeViewportSize"] = False

def _adornment_mark_recompute_viewport_size(adornment: _Adornment) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    if adornment["recomputeViewportSize"]:
        return
    adornment["recomputeViewportSize"] = True
    _adornment_mark_recompute_layout(adornment)
def _adornment_recompute_viewport_size(adornment: _Adornment) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    if not adornment["recomputeViewportSize"]:
        return
    adornment["recomputeViewportSize"] = False
    frame = adornment["frame"]
    thickness = adornment["thickness"]
    horizontalThickness = _thickness_get_horizontal(thickness)
    verticalThickness = _thickness_get_vertical(thickness)
    adornment["viewportSize"] = Size(frame.w - horizontalThickness, frame.h - verticalThickness)

def _adornment_mark_recompute_layout(adornment: _Adornment) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    if adornment["recomputeLayout"]:
        return
    adornment["recomputeLayout"] = True
    for subview in adornment["subviews"]:
        _view_mark_recompute_layout(subview)
def _adornment_recompute_layout(adornment: _Adornment) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    if not adornment["recomputeLayout"]:
        return
    adornment["recomputeLayout"] = False
    frame = adornment["frame"]
    subviews = adornment["subviews"]
    for subview in subviews:
        _view_resolve_computed_layout(subview, frame)
        _view_recompute_layout(subview)
    # Check if layout needs to call _adornment_mark_recompute_display
    pass

def _adornment_mark_recompute_display(adornment: _Adornment, region: Rectangle = None) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment)
    if region is None:
        region = adornment["frame"]
    adornment["recomputeDisplay"] = rectangle_union(adornment["recomputeDisplay"], region)
    for subview in adornment["subviews"]:
        subviewFrame = subview["frame"]
        intersection = rectangle_intersect(subviewFrame, region)
        if intersection.w < 0 or intersection.h < 0:
            continue
        subviewRegion = Rectangle(
            intersection.x - subviewFrame.x, 
            intersection.y - subviewFrame.y, 
            intersection.w, intersection.h
        )
        _view_mark_recompute_display(subview, subviewRegion)

def _adornment_draw(adornment: _Adornment, point: Point) -> None:
    if mixin_is_override(adornment):
        return mixin_call_override(adornment, point)
    driver = adornment["driver"]
    frame = adornment["frame"]
    thickness = adornment["thickness"]
    newPoint = Point(point.x + frame.x, point.y + frame.y)
    _thickness_draw(thickness, driver, rectangle_from_point_size(newPoint, rectangle_get_size(frame)), _Rune_clear)

_Margin = type[_Adornment]

def _margin_new(driver: _Driver, superview: "_View") -> _Margin:
    return dict_with(
        _adornment_new(
            driver,
            superview
        )
    )

_Border = type[_Adornment]

def _border_new(driver: _Driver, superview: "_View") -> _Border:
    return dict_with(
        _adornment_new(
            driver,
            superview,
            _adornment_draw=_border_draw
        )
    )
def _border_draw(border: _Border, point: Point) -> None:
    if mixin_is_override(border):
        return mixin_call_override(border)
    driver = border["driver"]
    frame = border["frame"]
    thickness = border["thickness"]
    newPoint = Point(point.x + frame.x, point.y + frame.y)
    rectangle = rectangle_from_point_size(newPoint, rectangle_get_size(frame))
    left = thickness.left
    top = thickness.top
    right = thickness.right
    bottom = thickness.bottom
    _driver_fill_rect(driver, rectangle_from_point_size(rectangle_get_point(rectangle), Size(min(rectangle.w, left), rectangle.h)), _Rune("│", _RuneAttribute_clear))
    _driver_fill_rect(driver, rectangle_from_point_size(rectangle_get_point(rectangle), Size(rectangle.w, min(rectangle.h, top))), _Rune("─", _RuneAttribute_clear))
    _driver_fill_rect(driver, rectangle_from_point_size(Point(rectangle.x + max(0, rectangle.w - right), rectangle.y), Size(min(rectangle.w, right), rectangle.h)), _Rune("│", _RuneAttribute_clear))
    _driver_fill_rect(driver, rectangle_from_point_size(Point(rectangle.x, rectangle.y + max(0, rectangle.h - bottom)), Size(rectangle.w, min(rectangle.h, bottom))), _Rune("─", _RuneAttribute_clear))
    if top != 0 and left != 0 and rectangle.w > 0 and rectangle.h > 0:
        _driver_set_content(driver, rectangle.x, rectangle.y, _Rune("╭", _RuneAttribute_clear))
    if top != 0 and right != 0 and rectangle.w > 0 and rectangle.h > 0:
        _driver_set_content(driver, rectangle.x + rectangle.w - 1, rectangle.y, _Rune("╮", _RuneAttribute_clear))
    if bottom != 0 and left != 0 and rectangle.w > 0 and rectangle.h > 0:
        _driver_set_content(driver, rectangle.x, rectangle.y + rectangle.h - 1, _Rune("╰", _RuneAttribute_clear))
    if bottom != 0 and right != 0 and rectangle.w > 0 and rectangle.h > 0:
        _driver_set_content(driver, rectangle.x + rectangle.w - 1, rectangle.y + rectangle.h - 1, _Rune("╯", _RuneAttribute_clear))

_Padding = type[_Adornment]

def _padding_new(driver: _Driver, superview: "_View") -> _Padding:
    return dict_with(
        _adornment_new(
            driver,
            superview
        )
    )

_LayoutMode = Union[
    Literal["Absolute"],
    Literal["Computed"]
]

_View = TypedDict("View",
    driver=_Driver,
    x=_Pos,
    y=_Pos,
    width=_Dim,
    height=_Dim,
    margin=_Margin,
    border=_Border,
    padding=_Padding,
    frame=Rectangle, # frame = contentSize + margin + border + padding
    contentSize=Optional[Size],
    viewportPosition=Point, # Bounded by contentSize
    viewportSize=Size, # Bounded by contentSize
    superview=Optional["_View"],
    subviews=list["_View"],
    textFormatter=_TextFormatter,
    recomputeViewportSize=bool,
    recomputeLayout=bool,
    recomputeDisplay=Rectangle,
)

def _view_new(driver: _Driver, **kwargs) -> _View:
    result = dict(
        driver=driver,
        x=_pos_from_absolute(0),
        y=_pos_from_absolute(0),
        width=_dim_from_absolute(0),
        height=_dim_from_absolute(0),
        margin=None,
        border=None,
        padding=None,
        frame=EmptyRectangle,
        contentSize=None,
        viewportPosition=EmptyPoint,
        viewportSize=EmptySize,
        superview=None,
        subviews=[],
        textFormatter=_text_formatter_new(driver),
        recomputeViewportSize=True,
        recomputeLayout=True,
        recomputeDisplay=EmptyRectangle,
        **mixin_new(kwargs)
    )
    result["margin"] = _margin_new(driver, result)
    result["border"] = _border_new(driver, result)
    result["padding"] = _padding_new(driver, result)
    return result
def _view_get_x(view: _View) -> _Pos:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["x"]
def _view_get_y(view: _View) -> _Pos:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["y"]
def _view_get_width(view: _View) -> _Dim:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["width"]
def _view_get_height(view: _View) -> _Dim:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["height"]
def _view_get_margin(view: _View) -> _Margin:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["margin"]
def _view_get_border(view: _View) -> _Border:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["border"]
def _view_get_padding(view: _View) -> _Padding:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["padding"]
def _view_get_frame(view: _View) -> Rectangle:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["frame"]
def _view_get_content_size(view: _View) -> Size:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if view["contentSize"] is None:
        return _view_get_viewport_size(view)
    return view["contentSize"]
def _view_get_viewport_position(view: _View) -> Point:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["viewportPosition"]
def _view_get_viewport_size(view: _View) -> Point:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if view["recomputeViewportSize"]:
        _view_recompute_viewport_size(view)
    return view["viewportSize"]
def _view_get_text_formatter(view: _View) -> _TextFormatter:
    if mixin_is_override(view):
        return mixin_call_override(view)
    return view["textFormatter"]
def _view_get_layout_mode(view: _View) -> _LayoutMode:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if _pos_as_absolute(view["x"]) is None or _pos_as_absolute(view["y"]) is None:
        return "Computed"
    if _dim_as_absolute(view["width"]) is None or _dim_as_absolute(view["height"]) is None:
        return "Computed"
    return "Absolute"
def _view_set_x(view: _View, x: _Pos) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    view["x"] = x
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)
def _view_set_y(view: _View, y: _Pos) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    view["y"] = y
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)
def _view_set_width(view: _View, width: _Dim) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    view["width"] = width
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)
def _view_set_height(view: _View, height: _Dim) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    view["height"] = height
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)
def _view_set_frame(view: _View, frame: Rectangle) -> None:
    # Side effect: layoutMode changes to "absolute"
    if mixin_is_override(view):
        return mixin_call_override(view)
    view["frame"] = frame
    view["x"] = _pos_from_absolute(frame.x)
    view["y"] = _pos_from_absolute(frame.y)
    view["width"] = _pos_from_absolute(frame.w)
    view["height"] = _pos_from_absolute(frame.h)
    _view_mark_recompute_viewport_size(view)
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)
def _view_set_content_size(view: _View, contentSize: Size) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    view["contentSize"] = contentSize
    _view_mark_recompute_layout(view)
def _view_set_viewport_position(view: _View, viewportPosition: Point) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    view["viewportPosition"] = viewportPosition
    _view_mark_recompute_display(view)
def _view_set_viewport_size(view: _View, viewportSize: Size) -> None:
    # Side effect: layoutMode changes to "absolute" (_view_set_frame)
    if mixin_is_override(view):
        return mixin_call_override(view)
    frame = view["frame"]
    margin = view["margin"]
    border = view["border"]
    padding = view["padding"]
    _adornment_set_viewport_size(padding, viewportSize)
    _adornment_set_viewport_size(border, rectangle_get_size(_adornment_get_frame(padding)))
    _adornment_set_viewport_size(margin, rectangle_get_size(_adornment_get_frame(border)))
    newFrameSize = rectangle_get_size(_adornment_get_frame(margin))
    newFrame = rectangle_from_point_size(rectangle_get_point(frame), newFrameSize)
    _view_set_frame(newFrame)
    view["viewportSize"] = viewportSize
    view["recomputeViewportSize"] = False

def _view_has_child(view: _View, subview: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view, subview)
    subviewSuperview = subview["superview"]
    if subviewSuperview is view:
        return True
    return False
def _view_add_child(view: _View, subview: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view, subview)
    subviewSuperview = subview["superview"]
    if subviewSuperview is view:
        return
    if subviewSuperview is not None:
        _view_remove_child(subviewSuperview, subview)
    subview["superview"] = view
    array_push(view["subviews"], subview)
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)
    view["__unstable_has_changed"] = True
def _view_remove_child(view: _View, subview: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view, subview)
    subviewSuperview = subview["superview"]
    if subviewSuperview is not view:
        return
    subviews = view["subviews"]
    array_splice(subviews, array_index_of(subviews, subview), 1)
    subview["superview"] = None
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)
    view["__unstable_has_changed"] = True

def _view_resolve_computed_layout(view: _View, superviewContentSize: Size) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    x = view["x"]
    y = view["y"]
    width = view["width"]
    height = view["height"]
    computedX = _pos_calculate(x, superviewContentSize.w, "Abscissa", width, view)
    computedY = _pos_calculate(y, superviewContentSize.h, "Ordinate", height, view)
    computedWidth = _dim_calculate(width, superviewContentSize.w, "Abscissa", computedX, view)
    computedHeight = _dim_calculate(height, superviewContentSize.h, "Abscissa", computedY, view)
    newFrame = Rectangle(computedX, computedY, computedWidth, computedHeight)
    if rectangle_eq(view["frame"], newFrame):
        return
    view["frame"] = newFrame
    _view_mark_recompute_viewport_size(view)
    _view_recompute_viewport_size(view)
    _view_mark_recompute_layout(view)
    _view_mark_recompute_display(view)

def _view_mark_recompute_viewport_size(view: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if view["recomputeViewportSize"]:
        return
    view["recomputeViewportSize"] = True
    _view_mark_recompute_layout(view)
def _view_recompute_viewport_size(view: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if not view["recomputeViewportSize"]:
        return
    view["recomputeViewportSize"] = False
    frame = view["frame"]
    margin = view["margin"]
    border = view["border"]
    padding = view["padding"]
    marginFrame = rectangle_from_point_size(EmptyPoint, rectangle_get_size(frame))
    borderFrame = _thickness_compute_inside(_adornment_get_thickness(margin), marginFrame)
    paddingFrame = _thickness_compute_inside(_adornment_get_thickness(border), borderFrame)
    _adornment_set_frame(margin, marginFrame)
    _adornment_set_frame(border, borderFrame)
    _adornment_set_frame(padding, paddingFrame)
    view["viewportSize"] = _adornment_get_viewport_size(padding)

def _view_mark_recompute_layout(view: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if view["recomputeLayout"]:
        return
    view["recomputeLayout"] = True
    for subview in view["subviews"]:
        _view_mark_recompute_layout(subview)
    if view["superview"] is not None:
        _view_mark_recompute_layout(view["superview"])
def _view_recompute_layout(view: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if not view["recomputeLayout"]:
        return
    view["recomputeLayout"] = False
    width = view["width"]
    height = view["height"]
    margin = view["margin"]
    border = view["border"]
    padding = view["padding"]
    contentSize = _view_get_content_size(view)
    subviews = view["subviews"]
    def assertPosStatic(pos: _Pos) -> None:
        if _pos_as_absolute(pos) is not None:
            return
        if _pos_as_combine(pos) is not None:
            p: _PosCombine = pos
            assertPosStatic(p["left"])
            assertPosStatic(p["right"])
            return
        if _pos_as_view(pos) is not None:
            return
        raise "Pos is not static"
    def assertDimStatic(dim: _Dim) -> None:
        if _dim_as_absolute(dim) is not None:
            return
        if _dim_as_combine(dim) is not None:
            d: _DimCombine = dim
            assertDimStatic(d["left"])
            assertDimStatic(d["right"])
            return
        if _dim_as_view(dim) is not None:
            return
        raise "Dim is not static"
    if _dim_as_auto(width) is not None and width["min"] is None:
        for subview in subviews:
            assertPosStatic(subview["x"])
            assertDimStatic(subview["width"])
    if _dim_as_auto(height) is not None and height["min"] is None:
        for subview in subviews:
            assertPosStatic(subview["y"])
            assertDimStatic(subview["height"])
    _adornment_recompute_layout(margin)
    _adornment_recompute_layout(border)
    _adornment_recompute_layout(padding)
    for subview in subviews:
        _view_resolve_computed_layout(subview, contentSize)
        _view_recompute_layout(subview)
    pass

def _view_mark_recompute_display(view: _View, region: Rectangle = None) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    if region is None:
        region = view["frame"]
    view["recomputeDisplay"] = rectangle_union(view["recomputeDisplay"], region)
    _adornment_mark_recompute_display(view["margin"])
    _adornment_mark_recompute_display(view["border"])
    _adornment_mark_recompute_display(view["padding"])
    for subview in view["subviews"]:
        subviewFrame = subview["frame"]
        intersection = rectangle_intersect(subviewFrame, region)
        if intersection.w < 0 or intersection.h < 0:
            continue
        subviewRegion = Rectangle(
            intersection.x - subviewFrame.x, 
            intersection.y - subviewFrame.y, 
            intersection.w, intersection.h
        )
        _view_mark_recompute_display(subview, subviewRegion)

# def _view_recompute_resize(view: _View) -> None:
#     if mixin_is_override(view):
#         return mixin_call_override(view)
#     _view_recompute_layout()
#     _view_recompute_display()

def _view_transform_frame_to_screen(view: _View) -> Point:
    result = rectangle_get_point(view["frame"])
    current = view["superview"]
    while current is not None:
        currentFrame = current["frame"]
        currentViewportPosition = current["viewportPosition"]
        currentPadding = current["padding"]
        currentViewportOffset = _thickness_compute_inside(_adornment_get_thickness(currentPadding), _adornment_get_frame(currentPadding))
        result = Point(result.x + currentViewportOffset.x + currentFrame.x - currentViewportPosition.x, result.y + currentViewportOffset.y + currentFrame.y - currentViewportPosition.y)
        current = current["superview"]
    return result
def _view_transform_frame_to_superview(view: _View, superview: _View) -> Point:
    result = rectangle_get_point(view["frame"])
    current = view["superview"]
    while current is not None and current is not superview:
        currentFrame = current["frame"]
        currentViewportPosition = current["viewportPosition"]
        currentPadding = current["padding"]
        currentViewportOffset = _thickness_compute_inside(_adornment_get_thickness(currentPadding), _adornment_get_frame(currentPadding))
        result = Point(result.x + currentViewportOffset.x + currentFrame.x - currentViewportPosition.x, result.y + currentViewportOffset.y + currentFrame.y - currentViewportPosition.y)
        current = current["superview"]
    if current is not superview:
        return None
    return result
def _view_transform_viewport_to_screen(view: _View, point: Point) -> Point:
    screen = _view_transform_frame_to_screen(view)
    padding = view["padding"]
    viewportOffset = _thickness_compute_inside(_adornment_get_thickness(padding), _adornment_get_frame(padding))
    return Point(screen.x + viewportOffset.x + point.x, screen.y + viewportOffset.y + point.y)
def _view_transform_content_to_screen(view: _View, point: Point) -> Point:
    viewport = view["viewportPosition"]
    return _view_transform_viewport_to_screen(view, Point(point.x - viewport.x, point.y - viewport.y))

def _view_draw(view: _View) -> None:
    if mixin_is_override(view):
        return mixin_call_override(view)
    driver = view["driver"]
    frame = view["frame"]
    margin = view["margin"]
    border = view["border"]
    padding = view["padding"]
    superview = view["superview"]
    subviews = view["subviews"]
    textFormatter = view["textFormatter"]
    
    frameToScreenPoint = _view_transform_frame_to_screen(view)
    _view_recompute_viewport_size(view)
    if(
        ("__unstable_has_changed" in view and view["__unstable_has_changed"]) or
        ("__unstable_has_changed" in textFormatter and textFormatter["__unstable_has_changed"]) or
        (superview is not None and "__unstable_has_changed" in superview and superview["__unstable_has_changed"])
    ):
        view["__unstable_has_changed"] = True
        textFormatter["__unstable_has_changed"] = True

        _driver_clear_rect(driver, rectangle_from_point_size(frameToScreenPoint, rectangle_get_size(frame)))
        _adornment_draw(margin, frameToScreenPoint)
        _adornment_draw(border, frameToScreenPoint)
        _adornment_draw(padding, frameToScreenPoint)

        if superview is not None:
            # Unstable: Edge case, we support overlapping by putting the most-front element to be the last in the subviews array.
            # We need to mark the superview to __unstable_has_changed, to make the next our siblings to redraw. Thus we are overlapped.
            superview["__unstable_has_changed"] = True
            superview["__unstable_overlap_force_redraw_next"] = True
    
    paddingInside = _thickness_compute_inside(_adornment_get_thickness(padding), _adornment_get_frame(padding))
    newPoint = Point(frameToScreenPoint.x + paddingInside.x, frameToScreenPoint.y + paddingInside.y)
    inner = rectangle_from_point_size(newPoint, rectangle_get_size(paddingInside))
    _text_formatter_set_size(textFormatter, rectangle_get_size(inner))
    _text_formatter_draw(textFormatter, inner)
    
    for subview in subviews:
        _view_draw(subview)
    if "__unstable_overlap_force_redraw_next" in view and view["__unstable_overlap_force_redraw_next"]:
        # Recursively force call redraw on our next siblings.
        view["__unstable_overlap_force_redraw_next"] = False
        if superview is not None:
            superview["__unstable_has_changed"] = True
            superview["__unstable_overlap_force_redraw_next"] = True
    view["__unstable_has_changed"] = False
