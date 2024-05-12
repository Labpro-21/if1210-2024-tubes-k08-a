from typing import NamedTuple, Union

_Number = Union[int, float]
_Point = NamedTuple("Point", [("x", _Number), ("y", _Number)])
_Size = NamedTuple("Size", [("w", _Number), ("h", _Number)])
_Rectangle = NamedTuple("Rect", [("x", _Number), ("y", _Number), ("w", _Number), ("h", _Number)])
_EmptyPoint = _Point(0, 0)
_EmptySize = _Size(0, 0)
_EmptyRectangle = _Rectangle(0, 0, 0, 0)

def _point_eq(left: _Point, right: _Point) -> bool:
    return left.x == right.x and left.y == right.y
def _point_neq(left: _Point, right: _Point) -> bool:
    return left.x != right.x or left.y != right.y
def _point_add(left: _Point, right: _Point) -> _Point:
    return _Point(left.x + right.x, left.y + right.y)
def _point_sub(left: _Point, right: _Point) -> _Point:
    return _Point(left.x - right.x, left.y - right.y)

def _size_eq(left: _Size, right: _Size) -> bool:
    return left.x == right.x and left.y == right.y
def _size_neq(left: _Size, right: _Size) -> bool:
    return left.x != right.x or left.y != right.y
def _size_add(left: _Size, right: _Size) -> _Size:
    return _Size(left.x + right.x, left.y + right.y)
def _size_sub(left: _Size, right: _Size) -> _Size:
    return _Size(left.x - right.x, left.y - right.y)
def _size_from_point(point: _Point) -> _Size:
    return _Size(point.x, point.y)
def _size_as_point(size: _Size) -> _Point:
    return _Point(size.w, size.h)

def _rectangle_eq(left: _Rectangle, right: _Rectangle) -> bool:
    return left.x == right.x and left.y == right.y and left.w == right.w and left.h == right.h
def _rectangle_neq(left: _Rectangle, right: _Rectangle) -> bool:
    return left.x != right.x or left.y != right.y or left.w != right.w or left.h != right.h
def _rectangle_from_point_size(point: _Point, size: _Size):
    return _Rectangle(point.x, point.y, size.w, size.h)
def _rectangle_from_ltrb(left: _Number, top: _Number, right: _Number, bottom: _Number) -> _Rectangle:
    return _Rectangle(left, top, right - left, bottom - top)
def _rectangle_get_point(rect: _Rectangle) -> _Point:
    return _Point(rect.x, rect.y)
def _rectangle_get_size(rect: _Rectangle) -> _Size:
    return _Size(rect.w, rect.h)
def _rectangle_union(left: _Rectangle, right: _Rectangle) -> _Rectangle:
    return _rectangle_from_ltrb(
        min(left.x, right.x),
        min(left.y, right.y),
        max(left.x + left.w, right.x + right.w),
        max(left.y + left.h, right.y + right.h)
    )
def _rectangle_intersect(left: _Rectangle, right: _Rectangle) -> _Rectangle:
    return _rectangle_from_ltrb(
        max(left.x, right.x),
        max(left.y, right.y),
        min(left.x + left.w, right.x + right.w),
        min(left.y + left.h, right.y + right.h)
    )
def _rectangle_inflate(rect: _Rectangle, size: _Size) -> _Rectangle:
    return _Rectangle(
        rect.x - size.w,
        rect.y - size.h,
        rect.w + size.w * 2,
        rect.h + size.h * 2
    )
