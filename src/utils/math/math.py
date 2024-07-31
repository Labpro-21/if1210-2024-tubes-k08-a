from utils.primordials import *
from typing import NamedTuple, Union
import time
import math

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

def __lcg(seed: int) -> tuple[int, float]:
    # LCG function that produces the next seed and r (a float in range [0,1))
    # a, c, and m are arbitrary
    a: int = 423
    c: int = 532
    m: int = 623
    
    seed: int = (a * seed + c) % m
    r: float = seed / m
    
    return seed, r

def __cycle_list(seed: int, size: int) -> list[float]:
    # cycle_list and randList are to create a list of random integers
    # cycle_list() will repeat lcg() size times and store each value of r in the list y
    res: list[float] = []
    for i in range(size):
        seed, r = __lcg(seed)
        array_push(res, r)
    return res

def _rand_list(seed: int, size: int, min: int, max: int) -> list[int]:
    # rand_list() seed and size are arbitrary it only affects the randomizer
    # rand_list() will use the list from cycle_list() to create a list of random in range [min,max]
    res: list[int] = []
    for i in range(size):
        # TODO Nadhif: This is inefficient
        rand = int(min + (max - min + 1) * __cycle_list(seed, size)[i])
        array_push(res, rand)
    return res

def __cycle(seed: int, size: int) -> float:
    # cycle and randInt are to produce a random integer in range [min,max]
    # cycle() will repeat lcg() size times
    for i in range (size):
        seed, r = __lcg(seed)
    return r

# Declaring initial seed and size for ran_int
__rand_seed: int = math.floor(time.time())
__rand_size: int = math.floor(time.time()) % 5 

def _rand_int(min: int, max: int) -> int:
    # (NEW) rand_int() will have a predetermined seed and size using current time to make it more randomized
    # rand_int() produces a random integer in range [min,max] 
    rand: int
    for i in range(__rand_size):
        # TODO Nadhif: This is inefficient
        rand = int(min + (max - min + 1) * __cycle(__rand_seed, __rand_size))
    return rand

# NOTE USAGE EXAMPLE
# The code below: 8 and 50 are arbitrary, this will produce an array with 50 elements with the elements being in the range [20,30]
# print(rand_list(8,50,20,30)) 
# The code below: 6 and 30 are arbitrary, this will produce an integer in range [10,100]
# print(rand_int(10,100)) 

def _rand() -> float:
    global __rand_seed
    __rand_seed, result = __lcg(__rand_seed)
    return result

def _rand_uniq_int_array(min: int, max: int, pick: int) -> list[int]:
    result: list[int] = []
    while True:
        random = int(_rand() * (max - min) + min)
        if array_includes(result, random):
            continue
        array_push(result, random)
        pick -= 1
        if pick > 0:
            continue
        break
    return result
