import msvcrt
import os
from utils.primordials import *
from typing import NamedTuple, Union

_KeyEvent = NamedTuple("KeyEvent", [
    ("which", Union[int, tuple[int, int]]),
    ("key", str),
    ("code", str),
    ("shiftKey", bool),
    ("ctrlKey", bool),
    ("altKey", bool),
    ("metaKey", bool),
    ("repeat", bool),
])
__keyevent_table = [
    _KeyEvent(27, "ControlESC", "KeyESC", None, None, None, None, None),
    _KeyEvent(8, "ControlCR", "Enter", None, False, None, None, None), _KeyEvent(127, "ControlLF", "Enter", None, True, False, None, None), _KeyEvent((0, 28), "ControlNUL", "Enter", None, True, True, None, None), 
    _KeyEvent(8, "ControlCR", "NumpadEnter", None, False, None, None, None), _KeyEvent(127, "ControlLF", "NumpadEnter", None, True, False, None, None), _KeyEvent((0, 166), "ControlNUL", "NumpadEnter", None, True, True, None, None),
    _KeyEvent(49, "1", "Digit1", False, None, None, None, None), _KeyEvent(33, "!", "Digit1", True, None, None, None, None), _KeyEvent((0, 120), "ControlNUL", "Digit1", None, True, True, None, None),
    _KeyEvent(50, "2", "Digit2", False, None, None, None, None), _KeyEvent(64, "@", "Digit2", True, None, None, None, None), _KeyEvent(3, "ControlETX", "Digit2", None, True, False, None, None), _KeyEvent((0, 121), "ControlNUL", "Digit2", None, True, True, None, None),
    _KeyEvent(51, "3", "Digit3", False, None, None, None, None), _KeyEvent(35, "#", "Digit3", True, None, None, None, None), _KeyEvent((0, 122), "ControlNUL", "Digit3", None, True, True, None, None),
    _KeyEvent(52, "4", "Digit4", False, None, None, None, None), _KeyEvent(36, "$", "Digit4", True, None, None, None, None), _KeyEvent((0, 123), "ControlNUL", "Digit4", None, True, True, None, None),
    _KeyEvent(53, "5", "Digit5", False, None, None, None, None), _KeyEvent(37, "%", "Digit5", True, None, None, None, None), _KeyEvent((0, 124), "ControlNUL", "Digit5", None, True, True, None, None),
    _KeyEvent(54, "6", "Digit6", False, None, None, None, None), _KeyEvent(94, "^", "Digit6", True, None, None, None, None), _KeyEvent(31, "ControlRS", "Digit6", None, True, False, None, None), _KeyEvent((0, 125), "ControlNUL", "Digit6", None, True, True, None, None),
    _KeyEvent(55, "7", "Digit7", False, None, None, None, None), _KeyEvent(38, "&", "Digit7", True, None, None, None, None), _KeyEvent((0, 126), "ControlNUL", "Digit7", None, True, True, None, None),
    _KeyEvent(56, "8", "Digit8", False, None, None, None, None), _KeyEvent(42, "*", "Digit8", True, None, None, None, None), _KeyEvent((0, 127), "ControlNUL", "Digit8", None, True, True, None, None),
    _KeyEvent(57, "9", "Digit9", False, None, None, None, None), _KeyEvent(40, "(", "Digit9", True, None, None, None, None), _KeyEvent((0, 128), "ControlNUL", "Digit9", None, True, True, None, None),
    _KeyEvent(48, "0", "Digit0", False, None, None, None, None), _KeyEvent(41, ")", "Digit0", True, None, None, None, None), _KeyEvent((0, 129), "ControlNUL", "Digit0", None, True, True, None, None),
    _KeyEvent(45, "-", "Minus", False, None, None, None, None), _KeyEvent(95, "_", "Minus", True, None, None, None, None), _KeyEvent(45, "ControlUS", "Minus", None, True, False, None, None), _KeyEvent((0, 130), "-", "Minus", False, None, None, None, None),
    _KeyEvent(61, "=", "Equal", False, None, None, None, None), _KeyEvent(43, "+", "Equal", True, None, None, None, None), _KeyEvent((0, 131), "=", "Equal", False, None, None, None, None),
    _KeyEvent(8, "ControlBS", "Backspace", None, False, None, None, None), _KeyEvent(127, "ControlDEL", "Backspace", None, True, False, None, None), _KeyEvent((0, 14), "ControlNUL", "Backspace", None, True, True, None, None), 
    _KeyEvent(113, "q", "KeyQ", False, False, None, None, None), _KeyEvent(81, "Q", "KeyQ", True, False, None, None, None), _KeyEvent(17, "ControlDC1", "KeyQ", None, True, False, None, None), _KeyEvent((0, 16), "ControlNUL", "KeyQ", None, True, True, None, None),
    _KeyEvent(119, "w", "KeyW", False, False, None, None, None), _KeyEvent(87, "W", "KeyW", True, False, None, None, None), _KeyEvent(23, "ControlETB", "KeyW", None, True, False, None, None), _KeyEvent((0, 17), "ControlNUL", "KeyW", None, True, True, None, None),
    _KeyEvent(101, "e", "KeyE", False, False, None, None, None), _KeyEvent(69, "E", "KeyE", True, False, None, None, None), _KeyEvent(5, "ControlENQ", "KeyE", None, True, False, None, None), _KeyEvent((0, 18), "ControlNUL", "KeyE", None, True, True, None, None),
    _KeyEvent(114, "r", "KeyR", False, False, None, None, None), _KeyEvent(82, "R", "KeyR", True, False, None, None, None), _KeyEvent(18, "ControlDC2", "KeyR", None, True, False, None, None), _KeyEvent((0, 19), "ControlNUL", "KeyR", None, True, True, None, None),
    _KeyEvent(116, "t", "KeyT", False, False, None, None, None), _KeyEvent(84, "T", "KeyT", True, False, None, None, None), _KeyEvent(20, "ControlSO", "KeyT", None, True, False, None, None), _KeyEvent((0, 20), "ControlNUL", "KeyT", None, True, True, None, None),
    _KeyEvent(121, "y", "KeyY", False, False, None, None, None), _KeyEvent(89, "Y", "KeyY", True, False, None, None, None), _KeyEvent(25, "ControlEM", "KeyY", None, True, False, None, None), _KeyEvent((0, 21), "ControlNUL", "KeyY", None, True, True, None, None),
    _KeyEvent(117, "u", "KeyU", False, False, None, None, None), _KeyEvent(85, "U", "KeyU", True, False, None, None, None), _KeyEvent(21, "ControlNAK", "KeyU", None, True, False, None, None), _KeyEvent((0, 22), "ControlNUL", "KeyU", None, True, True, None, None),
    _KeyEvent(105, "i", "KeyI", False, False, None, None, None), _KeyEvent(73, "I", "KeyI", True, False, None, None, None), _KeyEvent(9, "ControlIAB", "KeyI", None, True, False, None, None), _KeyEvent((0, 23), "ControlNUL", "KeyI", None, True, True, None, None),
    _KeyEvent(111, "o", "KeyO", False, False, None, None, None), _KeyEvent(79, "O", "KeyO", True, False, None, None, None), _KeyEvent(15, "ControlSI", "KeyO", None, True, False, None, None), _KeyEvent((0, 24), "ControlNUL", "KeyO", None, True, True, None, None),
    _KeyEvent(112, "p", "KeyP", False, False, None, None, None), _KeyEvent(80, "P", "KeyP", True, False, None, None, None), _KeyEvent(16, "ControlDLE", "KeyP", None, True, False, None, None), _KeyEvent((0, 25), "ControlNUL", "KeyP", None, True, True, None, None),
    _KeyEvent(91, "[", "BracketLeft", False, False, None, None, None), _KeyEvent(123, "{", "BracketLeft", True, False, None, None, None), _KeyEvent(27, "ControlESC", "BracketLeft", None, True, False, None, None), _KeyEvent((0, 26), "ControlNUL", "BracketLeft", None, True, True, None, None),
    _KeyEvent(93, "]", "BracketRight", False, False, None, None, None), _KeyEvent(125, "}", "BracketRight", True, False, None, None, None), _KeyEvent(29, "ControlGS", "BracketRight", None, True, False, None, None), _KeyEvent((0, 27), "ControlNUL", "BracketRight", None, True, True, None, None),
    _KeyEvent(97, "a", "KeyA", False, False, None, None, None), _KeyEvent(65, "A", "KeyA", True, False, None, None, None), _KeyEvent(1, "ControlSOH", "KeyA", None, True, False, None, None), _KeyEvent((0, 30), "ControlNUL", "KeyA", None, True, True, None, None),
    _KeyEvent(115, "s", "KeyS", False, False, None, None, None), _KeyEvent(83, "S", "KeyS", True, False, None, None, None), _KeyEvent(19, "ControlDC3", "KeyS", None, True, False, None, None), _KeyEvent((0, 31), "ControlNUL", "KeyS", None, True, True, None, None),
    _KeyEvent(100, "d", "KeyD", False, False, None, None, None), _KeyEvent(68, "D", "KeyD", True, False, None, None, None), _KeyEvent(4, "ControlEOT", "KeyD", None, True, False, None, None), _KeyEvent((0, 32), "ControlNUL", "KeyD", None, True, True, None, None),
    _KeyEvent(102, "f", "KeyF", False, False, None, None, None), _KeyEvent(70, "F", "KeyF", True, False, None, None, None), _KeyEvent(6, "ControlACK", "KeyF", None, True, False, None, None), _KeyEvent((0, 33), "ControlNUL", "KeyF", None, True, True, None, None),
    _KeyEvent(103, "g", "KeyG", False, False, None, None, None), _KeyEvent(71, "G", "KeyG", True, False, None, None, None), _KeyEvent(7, "ControlBEL", "KeyG", None, True, False, None, None), _KeyEvent((0, 34), "ControlNUL", "KeyG", None, True, True, None, None),
    _KeyEvent(104, "h", "KeyH", False, False, None, None, None), _KeyEvent(72, "H", "KeyH", True, False, None, None, None), _KeyEvent(8, "ControlBS", "KeyH", None, True, False, None, None), _KeyEvent((0, 35), "ControlNUL", "KeyH", None, True, True, None, None),
    _KeyEvent(106, "j", "KeyJ", False, False, None, None, None), _KeyEvent(74, "J", "KeyJ", True, False, None, None, None), _KeyEvent(10, "ControlLF", "KeyJ", None, True, False, None, None), _KeyEvent((0, 36), "ControlNUL", "KeyJ", None, True, True, None, None),
    _KeyEvent(107, "k", "KeyK", False, False, None, None, None), _KeyEvent(75, "K", "KeyK", True, False, None, None, None), _KeyEvent(11, "ControlVT", "KeyK", None, True, False, None, None), _KeyEvent((0, 37), "ControlNUL", "KeyK", None, True, True, None, None),
    _KeyEvent(108, "l", "KeyL", False, False, None, None, None), _KeyEvent(76, "L", "KeyL", True, False, None, None, None), _KeyEvent(12, "ControlFF", "KeyL", None, True, False, None, None), _KeyEvent((0, 38), "ControlNUL", "KeyL", None, True, True, None, None),
    _KeyEvent(91, ";", "Semicolon", False, None, None, None, None), _KeyEvent(123, ":", "Semicolon", True, None, None, None, None), _KeyEvent((0, 39), "ControlNUL", "Semicolon", None, True, True, None, None),
    _KeyEvent(39, "'", "Quote", False, None, None, None, None), _KeyEvent(34, "\"", "Quote", True, None, None, None, None), _KeyEvent((0, 40), "ControlNUL", "Quote", None, True, True, None, None),
    _KeyEvent(96, "`", "Backquote", False, None, None, None, None), _KeyEvent(126, "~", "Backquote", True, None, None, None, None), _KeyEvent((0, 41), "ControlNUL", "Backquote", None, True, True, None, None),
    _KeyEvent(92, "\\", "Backslash", False, False, None, None, None), _KeyEvent(124, "|", "Backslash", True, False, None, None, None), _KeyEvent(28, "ControlFS", "Backslash", None, True, False, None, None),
    _KeyEvent(122, "z", "KeyZ", False, False, None, None, None), _KeyEvent(90, "Z", "KeyZ", True, False, None, None, None), _KeyEvent(26, "ControlSUB", "KeyZ", None, True, False, None, None), _KeyEvent((0, 44), "ControlNUL", "KeyZ", None, True, True, None, None),
    _KeyEvent(120, "x", "KeyX", False, False, None, None, None), _KeyEvent(88, "X", "KeyX", True, False, None, None, None), _KeyEvent(24, "ControlCAN", "KeyX", None, True, False, None, None), _KeyEvent((0, 45), "ControlNUL", "KeyX", None, True, True, None, None),
    _KeyEvent(99, "c", "KeyC", False, False, None, None, None), _KeyEvent(67, "C", "KeyC", True, False, None, None, None), _KeyEvent(3, "ControlETX", "KeyC", None, True, False, None, None), _KeyEvent((0, 46), "ControlNUL", "KeyC", None, True, True, None, None),
    _KeyEvent(118, "v", "KeyV", False, False, None, None, None), _KeyEvent(86, "V", "KeyV", True, False, None, None, None), _KeyEvent(22, "ControlSYN", "KeyV", None, True, False, None, None), _KeyEvent((0, 47), "ControlNUL", "KeyV", None, True, True, None, None),
    _KeyEvent(98, "b", "KeyB", False, False, None, None, None), _KeyEvent(66, "B", "KeyB", True, False, None, None, None), _KeyEvent(2, "ControlSTX", "KeyB", None, True, False, None, None), _KeyEvent((0, 48), "ControlNUL", "KeyB", None, True, True, None, None),
    _KeyEvent(110, "n", "KeyN", False, False, None, None, None), _KeyEvent(78, "N", "KeyN", True, False, None, None, None), _KeyEvent(14, "ControlSO", "KeyN", None, True, False, None, None), _KeyEvent((0, 49), "ControlNUL", "KeyN", None, True, True, None, None),
    _KeyEvent(109, "m", "KeyM", False, False, None, None, None), _KeyEvent(77, "M", "KeyM", True, False, None, None, None), _KeyEvent(13, "ControlCR", "KeyM", None, True, False, None, None), _KeyEvent((0, 50), "ControlNUL", "KeyM", None, True, True, None, None),
    _KeyEvent(44, ",", "Comma", False, None, None, None, None), _KeyEvent(60, "<", "Comma", True, None, None, None, None), _KeyEvent((0, 51), "ControlNUL", "Comma", None, True, True, None, None),
    _KeyEvent(46, ".", "Period", False, None, None, None, None), _KeyEvent(62, ">", "Period", True, None, None, None, None), _KeyEvent((0, 52), "ControlNUL", "Period", None, True, True, None, None),
    _KeyEvent(47, "/", "Slash", False, None, None, None, None), _KeyEvent(63, "?", "Slash", True, None, None, None, None), _KeyEvent((0, 53), "ControlNUL", "Slash", None, True, True, None, None),
    _KeyEvent(47, "/", "NumpadDivide", False, False, None, None, None), _KeyEvent(63, "?", "NumpadDivide", True, False, None, None, None), _KeyEvent((0, 149), "ControlNUL", "NumpadDivide", None, True, False, None, None), _KeyEvent((0, 164), "ControlNUL", "NumpadDivide", None, True, True, None, None),
    _KeyEvent(42, "*", "NumpadMultiply", None, False, None, None, None), _KeyEvent(16, "ControlDLE", "NumpadMultiply", None, True, None, None, None),
    _KeyEvent(32, " ", "Space", None, None, None, None, None),
    _KeyEvent((0, 59), "F1", "F1", False, False, None, None, None), _KeyEvent((0, 84), "F1", "F1", True, False, None, None, None), _KeyEvent((0, 94), "F1", "F1", None, True, False, None, None), _KeyEvent((0, 104), "F1", "F1", None, True, True, None, None),
    _KeyEvent((0, 60), "F2", "F2", False, False, None, None, None), _KeyEvent((0, 85), "F2", "F2", True, False, None, None, None), _KeyEvent((0, 95), "F2", "F2", None, True, False, None, None), _KeyEvent((0, 105), "F2", "F2", None, True, True, None, None),
    _KeyEvent((0, 61), "F3", "F3", False, False, None, None, None), _KeyEvent((0, 86), "F3", "F3", True, False, None, None, None), _KeyEvent((0, 96), "F3", "F3", None, True, False, None, None), _KeyEvent((0, 106), "F3", "F3", None, True, True, None, None),
    _KeyEvent((0, 62), "F4", "F4", False, False, None, None, None), _KeyEvent((0, 87), "F4", "F4", True, False, None, None, None), _KeyEvent((0, 97), "F4", "F4", None, True, False, None, None), _KeyEvent((0, 107), "F4", "F4", None, True, True, None, None),
    _KeyEvent((0, 63), "F5", "F5", False, False, None, None, None), _KeyEvent((0, 88), "F5", "F5", True, False, None, None, None), _KeyEvent((0, 98), "F5", "F5", None, True, False, None, None), _KeyEvent((0, 108), "F5", "F5", None, True, True, None, None),
    _KeyEvent((0, 64), "F6", "F6", False, False, None, None, None), _KeyEvent((0, 89), "F6", "F6", True, False, None, None, None), _KeyEvent((0, 99), "F6", "F6", None, True, False, None, None), _KeyEvent((0, 109), "F6", "F6", None, True, True, None, None),
    _KeyEvent((0, 65), "F7", "F7", False, False, None, None, None), _KeyEvent((0, 90), "F7", "F7", True, False, None, None, None), _KeyEvent((0, 100), "F7", "F7", None, True, False, None, None), _KeyEvent((0, 110), "F7", "F7", None, True, True, None, None),
    _KeyEvent((0, 66), "F8", "F8", False, False, None, None, None), _KeyEvent((0, 91), "F8", "F8", True, False, None, None, None), _KeyEvent((0, 101), "F8", "F8", None, True, False, None, None), _KeyEvent((0, 111), "F8", "F8", None, True, True, None, None),
    _KeyEvent((0, 67), "F9", "F9", False, False, None, None, None), _KeyEvent((0, 92), "F9", "F9", True, False, None, None, None), _KeyEvent((0, 102), "F9", "F9", None, True, False, None, None), _KeyEvent((0, 112), "F9", "F9", None, True, True, None, None),
    _KeyEvent((0, 68), "F10", "F10", False, False, None, None, None), _KeyEvent((0, 93), "F10", "F10", True, False, None, None, None), _KeyEvent((0, 103), "F10", "F10", None, True, False, None, None), _KeyEvent((0, 113), "F10", "F10", None, True, True, None, None),
    _KeyEvent((224, 133), "F11", "F11", False, False, None, None, None), _KeyEvent((224, 135), "F11", "F11", True, False, None, None, None), _KeyEvent((224, 137), "F11", "F11", None, True, False, None, None), _KeyEvent((224, 139), "F11", "F11", None, True, True, None, None),
    _KeyEvent((224, 134), "F12", "F12", False, False, None, None, None), _KeyEvent((224, 136), "F12", "F12", True, False, None, None, None), _KeyEvent((224, 138), "F12", "F12", None, True, False, None, None), _KeyEvent((224, 140), "F12", "F12", None, True, True, None, None),
    _KeyEvent((0, 71), "Home", "Numpad7", False, False, None, None, None), _KeyEvent(55, "7", "Numpad7", True, False, None, None, None), _KeyEvent((0, 119), "ControlNUL", "Numpad7", None, True, None, None, None),
    _KeyEvent((0, 71), "Home", "Home", None, False, False, None, None), _KeyEvent((0, 119), "ControlNUL", "Home", None, True, False, None, None), _KeyEvent((0, 151), "ControlNUL", "Home", None, None, True, None, None),
    _KeyEvent((0, 72), "Up", "Numpad8", False, False, None, None, None), _KeyEvent(56, "8", "Numpad8", True, False, None, None, None), _KeyEvent((0, 141), "ControlNUL", "Numpad8", None, True, None, None, None),
    _KeyEvent((224, 72), "Up", "Up", None, False, False, None, None), _KeyEvent((224, 141), "ControlNUL", "Up", None, True, False, None, None), _KeyEvent((0, 152), "ControlNUL", "Up", None, None, True, None, None),
    _KeyEvent((0, 73), "PageUp", "Numpad9", False, False, None, None, None), _KeyEvent(57, "9", "Numpad9", True, False, None, None, None), _KeyEvent((0, 132), "ControlNUL", "Numpad9", None, True, None, None, None),
    _KeyEvent((0, 73), "PageUp", "PageUp", None, False, False, None, None), _KeyEvent((0, 132), "ControlNUL", "PageUp", None, True, False, None, None), _KeyEvent((0, 153), "ControlNUL", "PageUp", None, None, True, None, None),
    _KeyEvent(53, "-", "NumpadMinus", True, None, None, None, None),
    _KeyEvent((0, 75), "Left", "Numpad4", False, False, None, None, None), _KeyEvent(52, "4", "Numpad4", True, False, None, None, None), _KeyEvent((0, 115), "ControlNUL", "Numpad4", None, True, None, None, None),
    _KeyEvent((224, 75), "Left", "Left", None, False, False, None, None), _KeyEvent((224, 115), "ControlNUL", "Left", None, True, False, None, None), _KeyEvent((0, 155), "ControlNUL", "Left", None, None, True, None, None),
    _KeyEvent(53, "5", "Numpad5", True, None, None, None, None),
    _KeyEvent((0, 77), "Right", "Numpad6", False, False, None, None, None), _KeyEvent(54, "4", "Numpad6", True, False, None, None, None), _KeyEvent((0, 116), "ControlNUL", "Numpad6", None, True, None, None, None),
    _KeyEvent((224, 77), "Right", "Right", None, False, False, None, None), _KeyEvent((224, 116), "ControlNUL", "Right", None, True, False, None, None), _KeyEvent((0, 157), "ControlNUL", "Right", None, None, True, None, None),
    _KeyEvent(43, "+", "NumpadPlus", True, None, None, None, None),
    _KeyEvent((0, 79), "End", "Numpad1", False, False, None, None, None), _KeyEvent(49, "1", "Numpad1", True, False, None, None, None), _KeyEvent((0, 117), "ControlNUL", "Numpad1", None, True, None, None, None),
    _KeyEvent((0, 79), "End", "End", None, False, False, None, None), _KeyEvent((0, 117), "ControlNUL", "End", None, True, False, None, None), _KeyEvent((0, 159), "ControlNUL", "End", None, None, True, None, None),
    _KeyEvent((0, 80), "Down", "Numpad2", False, False, None, None, None), _KeyEvent(50, "2", "Numpad2", True, False, None, None, None), _KeyEvent((0, 145), "ControlNUL", "Numpad2", None, True, None, None, None),
    _KeyEvent((224, 80), "Down", "Down", None, False, False, None, None), _KeyEvent((224, 145), "ControlNUL", "Down", None, True, False, None, None), _KeyEvent((0, 160), "ControlNUL", "Down", None, None, True, None, None),
    _KeyEvent((0, 81), "PageDown", "Numpad3", False, False, None, None, None), _KeyEvent(51, "3", "Numpad3", True, False, None, None, None), _KeyEvent((0, 118), "ControlNUL", "Numpad3", None, True, None, None, None),
    _KeyEvent((0, 81), "PageDown", "PageDown", None, False, False, None, None), _KeyEvent((0, 118), "ControlNUL", "PageDown", None, True, False, None, None), _KeyEvent((0, 161), "ControlNUL", "PageDown", None, None, True, None, None),
    _KeyEvent((0, 82), "Insert", "Numpad0", False, False, None, None, None), _KeyEvent(48, "3", "Numpad0", True, False, None, None, None), _KeyEvent((0, 146), "ControlNUL", "Numpad0", None, True, None, None, None),
    _KeyEvent((0, 82), "Insert", "Insert", None, False, False, None, None), _KeyEvent((0, 146), "ControlNUL", "Insert", None, True, False, None, None), _KeyEvent((0, 162), "ControlNUL", "Insert", None, None, True, None, None),
    _KeyEvent((0, 83), "Delete", "NumpadDecimal", False, False, None, None, None), _KeyEvent(46, "3", "NumpadDecimal", True, False, None, None, None), _KeyEvent((0, 147), "ControlNUL", "NumpadDecimal", None, True, None, None, None),
    _KeyEvent((0, 83), "Delete", "Delete", None, False, False, None, None), _KeyEvent((0, 147), "ControlNUL", "Delete", None, True, False, None, None), _KeyEvent((0, 163), "ControlNUL", "Delete", None, None, True, None, None),
]

os.system('cls')
print(len(__keyevent_table))
while True:
    print('Press key: ', end='', flush=True)

    # key = msvcrt.getwch()
    # num = ord(key)
    # if num in (0, 224):
    #     ext = msvcrt.getwch()
    #     print(f'prefix: {num}   -   key: {ext!r}   -   unicode: {ord(ext)}')
    # else:
    #     print(f'key: {key!r}   -   unicode: {ord(key)}')

    key = ord(msvcrt.getwch())
    if key == 0 or key == 224:
        key = (key, ord(msvcrt.getwch()))
    keyevent = array_find(__keyevent_table, lambda e, *_: e[0] == key)
    if keyevent == None:
        print(f"Unrecognized event: {str(key)}")
        continue
    print(f"Event: {str(keyevent)}")
