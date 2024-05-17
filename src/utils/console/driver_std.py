from utils.primordials import *
from utils.math import *
from typing import TypedDict, NamedTuple, Union, Callable, Any
from .console import _Driver, _DriverAttribute, _driver_new, _driver_set_size, _Rune, _RuneAttribute, _RuneAttribute_clear
import sys
import os

_GetchKeyEvent = NamedTuple("KeyEvent", [
    ("which", Union[int, tuple[int, int]]),
    ("key", str),
    ("code", str),
    ("shiftKey", bool),
    ("ctrlKey", bool),
    ("altKey", bool),
    ("metaKey", bool),
    ("repeat", bool),
])
__GetchKeyEvent_table = [
    _GetchKeyEvent(27, "ControlESC", "KeyESC", None, None, None, None, None),
    _GetchKeyEvent(13, "ControlCR", "Enter", None, False, None, None, None), _GetchKeyEvent(10, "ControlLF", "Enter", None, True, False, None, None), _GetchKeyEvent((0, 28), "ControlNUL", "Enter", None, True, True, None, None), 
    _GetchKeyEvent(13, "ControlCR", "NumpadEnter", None, False, None, None, None), _GetchKeyEvent(10, "ControlLF", "NumpadEnter", None, True, False, None, None), _GetchKeyEvent((0, 166), "ControlNUL", "NumpadEnter", None, True, True, None, None),
    _GetchKeyEvent(49, "1", "Digit1", False, None, None, None, None), _GetchKeyEvent(33, "!", "Digit1", True, None, None, None, None), _GetchKeyEvent((0, 120), "ControlNUL", "Digit1", None, True, True, None, None),
    _GetchKeyEvent(50, "2", "Digit2", False, None, None, None, None), _GetchKeyEvent(64, "@", "Digit2", True, None, None, None, None), _GetchKeyEvent(3, "ControlETX", "Digit2", None, True, False, None, None), _GetchKeyEvent((0, 121), "ControlNUL", "Digit2", None, True, True, None, None),
    _GetchKeyEvent(51, "3", "Digit3", False, None, None, None, None), _GetchKeyEvent(35, "#", "Digit3", True, None, None, None, None), _GetchKeyEvent((0, 122), "ControlNUL", "Digit3", None, True, True, None, None),
    _GetchKeyEvent(52, "4", "Digit4", False, None, None, None, None), _GetchKeyEvent(36, "$", "Digit4", True, None, None, None, None), _GetchKeyEvent((0, 123), "ControlNUL", "Digit4", None, True, True, None, None),
    _GetchKeyEvent(53, "5", "Digit5", False, None, None, None, None), _GetchKeyEvent(37, "%", "Digit5", True, None, None, None, None), _GetchKeyEvent((0, 124), "ControlNUL", "Digit5", None, True, True, None, None),
    _GetchKeyEvent(54, "6", "Digit6", False, None, None, None, None), _GetchKeyEvent(94, "^", "Digit6", True, None, None, None, None), _GetchKeyEvent(31, "ControlRS", "Digit6", None, True, False, None, None), _GetchKeyEvent((0, 125), "ControlNUL", "Digit6", None, True, True, None, None),
    _GetchKeyEvent(55, "7", "Digit7", False, None, None, None, None), _GetchKeyEvent(38, "&", "Digit7", True, None, None, None, None), _GetchKeyEvent((0, 126), "ControlNUL", "Digit7", None, True, True, None, None),
    _GetchKeyEvent(56, "8", "Digit8", False, None, None, None, None), _GetchKeyEvent(42, "*", "Digit8", True, None, None, None, None), _GetchKeyEvent((0, 127), "ControlNUL", "Digit8", None, True, True, None, None),
    _GetchKeyEvent(57, "9", "Digit9", False, None, None, None, None), _GetchKeyEvent(40, "(", "Digit9", True, None, None, None, None), _GetchKeyEvent((0, 128), "ControlNUL", "Digit9", None, True, True, None, None),
    _GetchKeyEvent(48, "0", "Digit0", False, None, None, None, None), _GetchKeyEvent(41, ")", "Digit0", True, None, None, None, None), _GetchKeyEvent((0, 129), "ControlNUL", "Digit0", None, True, True, None, None),
    _GetchKeyEvent(45, "-", "Minus", False, None, None, None, None), _GetchKeyEvent(95, "_", "Minus", True, None, None, None, None), _GetchKeyEvent(45, "ControlUS", "Minus", None, True, False, None, None), _GetchKeyEvent((0, 130), "-", "Minus", False, None, None, None, None),
    _GetchKeyEvent(61, "=", "Equal", False, None, None, None, None), _GetchKeyEvent(43, "+", "Equal", True, None, None, None, None), _GetchKeyEvent((0, 131), "=", "Equal", False, None, None, None, None),
    _GetchKeyEvent(8, "ControlBS", "Backspace", None, False, None, None, None), _GetchKeyEvent(127, "ControlDEL", "Backspace", None, True, False, None, None), _GetchKeyEvent((0, 14), "ControlNUL", "Backspace", None, True, True, None, None), 
    _GetchKeyEvent(113, "q", "KeyQ", False, False, None, None, None), _GetchKeyEvent(81, "Q", "KeyQ", True, False, None, None, None), _GetchKeyEvent(17, "ControlDC1", "KeyQ", None, True, False, None, None), _GetchKeyEvent((0, 16), "ControlNUL", "KeyQ", None, True, True, None, None),
    _GetchKeyEvent(119, "w", "KeyW", False, False, None, None, None), _GetchKeyEvent(87, "W", "KeyW", True, False, None, None, None), _GetchKeyEvent(23, "ControlETB", "KeyW", None, True, False, None, None), _GetchKeyEvent((0, 17), "ControlNUL", "KeyW", None, True, True, None, None),
    _GetchKeyEvent(101, "e", "KeyE", False, False, None, None, None), _GetchKeyEvent(69, "E", "KeyE", True, False, None, None, None), _GetchKeyEvent(5, "ControlENQ", "KeyE", None, True, False, None, None), _GetchKeyEvent((0, 18), "ControlNUL", "KeyE", None, True, True, None, None),
    _GetchKeyEvent(114, "r", "KeyR", False, False, None, None, None), _GetchKeyEvent(82, "R", "KeyR", True, False, None, None, None), _GetchKeyEvent(18, "ControlDC2", "KeyR", None, True, False, None, None), _GetchKeyEvent((0, 19), "ControlNUL", "KeyR", None, True, True, None, None),
    _GetchKeyEvent(116, "t", "KeyT", False, False, None, None, None), _GetchKeyEvent(84, "T", "KeyT", True, False, None, None, None), _GetchKeyEvent(20, "ControlSO", "KeyT", None, True, False, None, None), _GetchKeyEvent((0, 20), "ControlNUL", "KeyT", None, True, True, None, None),
    _GetchKeyEvent(121, "y", "KeyY", False, False, None, None, None), _GetchKeyEvent(89, "Y", "KeyY", True, False, None, None, None), _GetchKeyEvent(25, "ControlEM", "KeyY", None, True, False, None, None), _GetchKeyEvent((0, 21), "ControlNUL", "KeyY", None, True, True, None, None),
    _GetchKeyEvent(117, "u", "KeyU", False, False, None, None, None), _GetchKeyEvent(85, "U", "KeyU", True, False, None, None, None), _GetchKeyEvent(21, "ControlNAK", "KeyU", None, True, False, None, None), _GetchKeyEvent((0, 22), "ControlNUL", "KeyU", None, True, True, None, None),
    _GetchKeyEvent(105, "i", "KeyI", False, False, None, None, None), _GetchKeyEvent(73, "I", "KeyI", True, False, None, None, None), _GetchKeyEvent(9, "ControlIAB", "KeyI", None, True, False, None, None), _GetchKeyEvent((0, 23), "ControlNUL", "KeyI", None, True, True, None, None),
    _GetchKeyEvent(111, "o", "KeyO", False, False, None, None, None), _GetchKeyEvent(79, "O", "KeyO", True, False, None, None, None), _GetchKeyEvent(15, "ControlSI", "KeyO", None, True, False, None, None), _GetchKeyEvent((0, 24), "ControlNUL", "KeyO", None, True, True, None, None),
    _GetchKeyEvent(112, "p", "KeyP", False, False, None, None, None), _GetchKeyEvent(80, "P", "KeyP", True, False, None, None, None), _GetchKeyEvent(16, "ControlDLE", "KeyP", None, True, False, None, None), _GetchKeyEvent((0, 25), "ControlNUL", "KeyP", None, True, True, None, None),
    _GetchKeyEvent(91, "[", "BracketLeft", False, False, None, None, None), _GetchKeyEvent(123, "{", "BracketLeft", True, False, None, None, None), _GetchKeyEvent(27, "ControlESC", "BracketLeft", None, True, False, None, None), _GetchKeyEvent((0, 26), "ControlNUL", "BracketLeft", None, True, True, None, None),
    _GetchKeyEvent(93, "]", "BracketRight", False, False, None, None, None), _GetchKeyEvent(125, "}", "BracketRight", True, False, None, None, None), _GetchKeyEvent(29, "ControlGS", "BracketRight", None, True, False, None, None), _GetchKeyEvent((0, 27), "ControlNUL", "BracketRight", None, True, True, None, None),
    _GetchKeyEvent(97, "a", "KeyA", False, False, None, None, None), _GetchKeyEvent(65, "A", "KeyA", True, False, None, None, None), _GetchKeyEvent(1, "ControlSOH", "KeyA", None, True, False, None, None), _GetchKeyEvent((0, 30), "ControlNUL", "KeyA", None, True, True, None, None),
    _GetchKeyEvent(115, "s", "KeyS", False, False, None, None, None), _GetchKeyEvent(83, "S", "KeyS", True, False, None, None, None), _GetchKeyEvent(19, "ControlDC3", "KeyS", None, True, False, None, None), _GetchKeyEvent((0, 31), "ControlNUL", "KeyS", None, True, True, None, None),
    _GetchKeyEvent(100, "d", "KeyD", False, False, None, None, None), _GetchKeyEvent(68, "D", "KeyD", True, False, None, None, None), _GetchKeyEvent(4, "ControlEOT", "KeyD", None, True, False, None, None), _GetchKeyEvent((0, 32), "ControlNUL", "KeyD", None, True, True, None, None),
    _GetchKeyEvent(102, "f", "KeyF", False, False, None, None, None), _GetchKeyEvent(70, "F", "KeyF", True, False, None, None, None), _GetchKeyEvent(6, "ControlACK", "KeyF", None, True, False, None, None), _GetchKeyEvent((0, 33), "ControlNUL", "KeyF", None, True, True, None, None),
    _GetchKeyEvent(103, "g", "KeyG", False, False, None, None, None), _GetchKeyEvent(71, "G", "KeyG", True, False, None, None, None), _GetchKeyEvent(7, "ControlBEL", "KeyG", None, True, False, None, None), _GetchKeyEvent((0, 34), "ControlNUL", "KeyG", None, True, True, None, None),
    _GetchKeyEvent(104, "h", "KeyH", False, False, None, None, None), _GetchKeyEvent(72, "H", "KeyH", True, False, None, None, None), _GetchKeyEvent(8, "ControlBS", "KeyH", None, True, False, None, None), _GetchKeyEvent((0, 35), "ControlNUL", "KeyH", None, True, True, None, None),
    _GetchKeyEvent(106, "j", "KeyJ", False, False, None, None, None), _GetchKeyEvent(74, "J", "KeyJ", True, False, None, None, None), _GetchKeyEvent(10, "ControlLF", "KeyJ", None, True, False, None, None), _GetchKeyEvent((0, 36), "ControlNUL", "KeyJ", None, True, True, None, None),
    _GetchKeyEvent(107, "k", "KeyK", False, False, None, None, None), _GetchKeyEvent(75, "K", "KeyK", True, False, None, None, None), _GetchKeyEvent(11, "ControlVT", "KeyK", None, True, False, None, None), _GetchKeyEvent((0, 37), "ControlNUL", "KeyK", None, True, True, None, None),
    _GetchKeyEvent(108, "l", "KeyL", False, False, None, None, None), _GetchKeyEvent(76, "L", "KeyL", True, False, None, None, None), _GetchKeyEvent(12, "ControlFF", "KeyL", None, True, False, None, None), _GetchKeyEvent((0, 38), "ControlNUL", "KeyL", None, True, True, None, None),
    _GetchKeyEvent(91, ";", "Semicolon", False, None, None, None, None), _GetchKeyEvent(123, ":", "Semicolon", True, None, None, None, None), _GetchKeyEvent((0, 39), "ControlNUL", "Semicolon", None, True, True, None, None),
    _GetchKeyEvent(39, "'", "Quote", False, None, None, None, None), _GetchKeyEvent(34, "\"", "Quote", True, None, None, None, None), _GetchKeyEvent((0, 40), "ControlNUL", "Quote", None, True, True, None, None),
    _GetchKeyEvent(96, "`", "Backquote", False, None, None, None, None), _GetchKeyEvent(126, "~", "Backquote", True, None, None, None, None), _GetchKeyEvent((0, 41), "ControlNUL", "Backquote", None, True, True, None, None),
    _GetchKeyEvent(92, "\\", "Backslash", False, False, None, None, None), _GetchKeyEvent(124, "|", "Backslash", True, False, None, None, None), _GetchKeyEvent(28, "ControlFS", "Backslash", None, True, False, None, None),
    _GetchKeyEvent(122, "z", "KeyZ", False, False, None, None, None), _GetchKeyEvent(90, "Z", "KeyZ", True, False, None, None, None), _GetchKeyEvent(26, "ControlSUB", "KeyZ", None, True, False, None, None), _GetchKeyEvent((0, 44), "ControlNUL", "KeyZ", None, True, True, None, None),
    _GetchKeyEvent(120, "x", "KeyX", False, False, None, None, None), _GetchKeyEvent(88, "X", "KeyX", True, False, None, None, None), _GetchKeyEvent(24, "ControlCAN", "KeyX", None, True, False, None, None), _GetchKeyEvent((0, 45), "ControlNUL", "KeyX", None, True, True, None, None),
    _GetchKeyEvent(99, "c", "KeyC", False, False, None, None, None), _GetchKeyEvent(67, "C", "KeyC", True, False, None, None, None), _GetchKeyEvent(3, "ControlETX", "KeyC", None, True, False, None, None), _GetchKeyEvent((0, 46), "ControlNUL", "KeyC", None, True, True, None, None),
    _GetchKeyEvent(118, "v", "KeyV", False, False, None, None, None), _GetchKeyEvent(86, "V", "KeyV", True, False, None, None, None), _GetchKeyEvent(22, "ControlSYN", "KeyV", None, True, False, None, None), _GetchKeyEvent((0, 47), "ControlNUL", "KeyV", None, True, True, None, None),
    _GetchKeyEvent(98, "b", "KeyB", False, False, None, None, None), _GetchKeyEvent(66, "B", "KeyB", True, False, None, None, None), _GetchKeyEvent(2, "ControlSTX", "KeyB", None, True, False, None, None), _GetchKeyEvent((0, 48), "ControlNUL", "KeyB", None, True, True, None, None),
    _GetchKeyEvent(110, "n", "KeyN", False, False, None, None, None), _GetchKeyEvent(78, "N", "KeyN", True, False, None, None, None), _GetchKeyEvent(14, "ControlSO", "KeyN", None, True, False, None, None), _GetchKeyEvent((0, 49), "ControlNUL", "KeyN", None, True, True, None, None),
    _GetchKeyEvent(109, "m", "KeyM", False, False, None, None, None), _GetchKeyEvent(77, "M", "KeyM", True, False, None, None, None), _GetchKeyEvent(13, "ControlCR", "KeyM", None, True, False, None, None), _GetchKeyEvent((0, 50), "ControlNUL", "KeyM", None, True, True, None, None),
    _GetchKeyEvent(44, ",", "Comma", False, None, None, None, None), _GetchKeyEvent(60, "<", "Comma", True, None, None, None, None), _GetchKeyEvent((0, 51), "ControlNUL", "Comma", None, True, True, None, None),
    _GetchKeyEvent(46, ".", "Period", False, None, None, None, None), _GetchKeyEvent(62, ">", "Period", True, None, None, None, None), _GetchKeyEvent((0, 52), "ControlNUL", "Period", None, True, True, None, None),
    _GetchKeyEvent(47, "/", "Slash", False, None, None, None, None), _GetchKeyEvent(63, "?", "Slash", True, None, None, None, None), _GetchKeyEvent((0, 53), "ControlNUL", "Slash", None, True, True, None, None),
    _GetchKeyEvent(47, "/", "NumpadDivide", False, False, None, None, None), _GetchKeyEvent(63, "?", "NumpadDivide", True, False, None, None, None), _GetchKeyEvent((0, 149), "ControlNUL", "NumpadDivide", None, True, False, None, None), _GetchKeyEvent((0, 164), "ControlNUL", "NumpadDivide", None, True, True, None, None),
    _GetchKeyEvent(42, "*", "NumpadMultiply", None, False, None, None, None), _GetchKeyEvent(16, "ControlDLE", "NumpadMultiply", None, True, None, None, None),
    _GetchKeyEvent(32, " ", "Space", None, None, None, None, None),
    _GetchKeyEvent((0, 59), "F1", "F1", False, False, None, None, None), _GetchKeyEvent((0, 84), "F1", "F1", True, False, None, None, None), _GetchKeyEvent((0, 94), "F1", "F1", None, True, False, None, None), _GetchKeyEvent((0, 104), "F1", "F1", None, True, True, None, None),
    _GetchKeyEvent((0, 60), "F2", "F2", False, False, None, None, None), _GetchKeyEvent((0, 85), "F2", "F2", True, False, None, None, None), _GetchKeyEvent((0, 95), "F2", "F2", None, True, False, None, None), _GetchKeyEvent((0, 105), "F2", "F2", None, True, True, None, None),
    _GetchKeyEvent((0, 61), "F3", "F3", False, False, None, None, None), _GetchKeyEvent((0, 86), "F3", "F3", True, False, None, None, None), _GetchKeyEvent((0, 96), "F3", "F3", None, True, False, None, None), _GetchKeyEvent((0, 106), "F3", "F3", None, True, True, None, None),
    _GetchKeyEvent((0, 62), "F4", "F4", False, False, None, None, None), _GetchKeyEvent((0, 87), "F4", "F4", True, False, None, None, None), _GetchKeyEvent((0, 97), "F4", "F4", None, True, False, None, None), _GetchKeyEvent((0, 107), "F4", "F4", None, True, True, None, None),
    _GetchKeyEvent((0, 63), "F5", "F5", False, False, None, None, None), _GetchKeyEvent((0, 88), "F5", "F5", True, False, None, None, None), _GetchKeyEvent((0, 98), "F5", "F5", None, True, False, None, None), _GetchKeyEvent((0, 108), "F5", "F5", None, True, True, None, None),
    _GetchKeyEvent((0, 64), "F6", "F6", False, False, None, None, None), _GetchKeyEvent((0, 89), "F6", "F6", True, False, None, None, None), _GetchKeyEvent((0, 99), "F6", "F6", None, True, False, None, None), _GetchKeyEvent((0, 109), "F6", "F6", None, True, True, None, None),
    _GetchKeyEvent((0, 65), "F7", "F7", False, False, None, None, None), _GetchKeyEvent((0, 90), "F7", "F7", True, False, None, None, None), _GetchKeyEvent((0, 100), "F7", "F7", None, True, False, None, None), _GetchKeyEvent((0, 110), "F7", "F7", None, True, True, None, None),
    _GetchKeyEvent((0, 66), "F8", "F8", False, False, None, None, None), _GetchKeyEvent((0, 91), "F8", "F8", True, False, None, None, None), _GetchKeyEvent((0, 101), "F8", "F8", None, True, False, None, None), _GetchKeyEvent((0, 111), "F8", "F8", None, True, True, None, None),
    _GetchKeyEvent((0, 67), "F9", "F9", False, False, None, None, None), _GetchKeyEvent((0, 92), "F9", "F9", True, False, None, None, None), _GetchKeyEvent((0, 102), "F9", "F9", None, True, False, None, None), _GetchKeyEvent((0, 112), "F9", "F9", None, True, True, None, None),
    _GetchKeyEvent((0, 68), "F10", "F10", False, False, None, None, None), _GetchKeyEvent((0, 93), "F10", "F10", True, False, None, None, None), _GetchKeyEvent((0, 103), "F10", "F10", None, True, False, None, None), _GetchKeyEvent((0, 113), "F10", "F10", None, True, True, None, None),
    _GetchKeyEvent((224, 133), "F11", "F11", False, False, None, None, None), _GetchKeyEvent((224, 135), "F11", "F11", True, False, None, None, None), _GetchKeyEvent((224, 137), "F11", "F11", None, True, False, None, None), _GetchKeyEvent((224, 139), "F11", "F11", None, True, True, None, None),
    _GetchKeyEvent((224, 134), "F12", "F12", False, False, None, None, None), _GetchKeyEvent((224, 136), "F12", "F12", True, False, None, None, None), _GetchKeyEvent((224, 138), "F12", "F12", None, True, False, None, None), _GetchKeyEvent((224, 140), "F12", "F12", None, True, True, None, None),
    _GetchKeyEvent((0, 71), "Home", "Numpad7", False, False, None, None, None), _GetchKeyEvent(55, "7", "Numpad7", True, False, None, None, None), _GetchKeyEvent((0, 119), "ControlNUL", "Numpad7", None, True, None, None, None),
    _GetchKeyEvent((0, 71), "Home", "Home", None, False, False, None, None), _GetchKeyEvent((0, 119), "ControlNUL", "Home", None, True, False, None, None), _GetchKeyEvent((0, 151), "ControlNUL", "Home", None, None, True, None, None),
    _GetchKeyEvent((0, 72), "Up", "Numpad8", False, False, None, None, None), _GetchKeyEvent(56, "8", "Numpad8", True, False, None, None, None), _GetchKeyEvent((0, 141), "ControlNUL", "Numpad8", None, True, None, None, None),
    _GetchKeyEvent((224, 72), "Up", "Up", None, False, False, None, None), _GetchKeyEvent((224, 141), "ControlNUL", "Up", None, True, False, None, None), _GetchKeyEvent((0, 152), "ControlNUL", "Up", None, None, True, None, None),
    _GetchKeyEvent((0, 73), "PageUp", "Numpad9", False, False, None, None, None), _GetchKeyEvent(57, "9", "Numpad9", True, False, None, None, None), _GetchKeyEvent((0, 132), "ControlNUL", "Numpad9", None, True, None, None, None),
    _GetchKeyEvent((0, 73), "PageUp", "PageUp", None, False, False, None, None), _GetchKeyEvent((0, 132), "ControlNUL", "PageUp", None, True, False, None, None), _GetchKeyEvent((0, 153), "ControlNUL", "PageUp", None, None, True, None, None),
    _GetchKeyEvent(53, "-", "NumpadMinus", True, None, None, None, None),
    _GetchKeyEvent((0, 75), "Left", "Numpad4", False, False, None, None, None), _GetchKeyEvent(52, "4", "Numpad4", True, False, None, None, None), _GetchKeyEvent((0, 115), "ControlNUL", "Numpad4", None, True, None, None, None),
    _GetchKeyEvent((224, 75), "Left", "Left", None, False, False, None, None), _GetchKeyEvent((224, 115), "ControlNUL", "Left", None, True, False, None, None), _GetchKeyEvent((0, 155), "ControlNUL", "Left", None, None, True, None, None),
    _GetchKeyEvent(53, "5", "Numpad5", True, None, None, None, None),
    _GetchKeyEvent((0, 77), "Right", "Numpad6", False, False, None, None, None), _GetchKeyEvent(54, "4", "Numpad6", True, False, None, None, None), _GetchKeyEvent((0, 116), "ControlNUL", "Numpad6", None, True, None, None, None),
    _GetchKeyEvent((224, 77), "Right", "Right", None, False, False, None, None), _GetchKeyEvent((224, 116), "ControlNUL", "Right", None, True, False, None, None), _GetchKeyEvent((0, 157), "ControlNUL", "Right", None, None, True, None, None),
    _GetchKeyEvent(43, "+", "NumpadPlus", True, None, None, None, None),
    _GetchKeyEvent((0, 79), "End", "Numpad1", False, False, None, None, None), _GetchKeyEvent(49, "1", "Numpad1", True, False, None, None, None), _GetchKeyEvent((0, 117), "ControlNUL", "Numpad1", None, True, None, None, None),
    _GetchKeyEvent((0, 79), "End", "End", None, False, False, None, None), _GetchKeyEvent((0, 117), "ControlNUL", "End", None, True, False, None, None), _GetchKeyEvent((0, 159), "ControlNUL", "End", None, None, True, None, None),
    _GetchKeyEvent((0, 80), "Down", "Numpad2", False, False, None, None, None), _GetchKeyEvent(50, "2", "Numpad2", True, False, None, None, None), _GetchKeyEvent((0, 145), "ControlNUL", "Numpad2", None, True, None, None, None),
    _GetchKeyEvent((224, 80), "Down", "Down", None, False, False, None, None), _GetchKeyEvent((224, 145), "ControlNUL", "Down", None, True, False, None, None), _GetchKeyEvent((0, 160), "ControlNUL", "Down", None, None, True, None, None),
    _GetchKeyEvent((0, 81), "PageDown", "Numpad3", False, False, None, None, None), _GetchKeyEvent(51, "3", "Numpad3", True, False, None, None, None), _GetchKeyEvent((0, 118), "ControlNUL", "Numpad3", None, True, None, None, None),
    _GetchKeyEvent((0, 81), "PageDown", "PageDown", None, False, False, None, None), _GetchKeyEvent((0, 118), "ControlNUL", "PageDown", None, True, False, None, None), _GetchKeyEvent((0, 161), "ControlNUL", "PageDown", None, None, True, None, None),
    _GetchKeyEvent((0, 82), "Insert", "Numpad0", False, False, None, None, None), _GetchKeyEvent(48, "3", "Numpad0", True, False, None, None, None), _GetchKeyEvent((0, 146), "ControlNUL", "Numpad0", None, True, None, None, None),
    _GetchKeyEvent((0, 82), "Insert", "Insert", None, False, False, None, None), _GetchKeyEvent((0, 146), "ControlNUL", "Insert", None, True, False, None, None), _GetchKeyEvent((0, 162), "ControlNUL", "Insert", None, None, True, None, None),
    _GetchKeyEvent((0, 83), "Delete", "NumpadDecimal", False, False, None, None, None), _GetchKeyEvent(46, "3", "NumpadDecimal", True, False, None, None, None), _GetchKeyEvent((0, 147), "ControlNUL", "NumpadDecimal", None, True, None, None, None),
    _GetchKeyEvent((0, 83), "Delete", "Delete", None, False, False, None, None), _GetchKeyEvent((0, 147), "ControlNUL", "Delete", None, True, False, None, None), _GetchKeyEvent((0, 163), "ControlNUL", "Delete", None, None, True, None, None),
]

_KeyEvent = Union[_GetchKeyEvent]

_DriverStd = TypedDict("DriverStd",
    size=Size,
    attribute=_DriverAttribute,
    contents=list[_Rune],
    dirtyLines=list[bool],
    
    keyListeners=list[Callable[[_KeyEvent], Any]],
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
        keyListeners=[],
        lastLine=-1,
        lastAttribute=None
    )
    _driver_set_size(result, __get_terminal_size())
    return result

__driverstd_tick_keyboard = None
if os.name == "nt":
    import msvcrt
    def tickKeyboard(driverstd: _DriverStd) -> None:
        if not msvcrt.kbhit():
            return
        key = ord(msvcrt.getwch())
        if key == 0 or key == 224:
            key = (key, ord(msvcrt.getwch()))
        getchKeyEvent = array_find(__GetchKeyEvent_table, lambda e, *_: e[0] == key)
        if getchKeyEvent is None:
            return
        keyListeners = driverstd["keyListeners"]
        for keyListener in keyListeners:
            keyListener(getchKeyEvent)
    __driverstd_tick_keyboard = tickKeyboard

def _driverstd_tick(driverstd: _DriverStd) -> None:
    newSize = __get_terminal_size()
    if driverstd["size"] != newSize:
        _driver_set_size(driverstd, newSize)
    if __driverstd_tick_keyboard is not None:
        __driverstd_tick_keyboard(driverstd)
    pass

def _driverstd_add_key_listener(driverstd: _DriverStd, listener: Callable[[_KeyEvent], Any]) -> None:
    keyListeners = driverstd["keyListeners"]
    if array_includes(keyListeners, listener):
        return
    array_push(keyListeners, listener)

def _driverstd_remove_key_listener(driverstd: _DriverStd, listener: Callable[[_KeyEvent], Any]) -> None:
    keyListeners = driverstd["keyListeners"]
    listenerIndex = array_index_of(keyListeners, listener)
    if listenerIndex == -1:
        return
    array_splice(keyListeners, listenerIndex, 1)

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
    _driverstd_set_current_attribute(driverstd, _RuneAttribute_clear)
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
