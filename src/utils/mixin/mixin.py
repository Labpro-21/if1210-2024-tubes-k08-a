from utils.primordials import *
from typing import Any
import sys

def _mixin_new(overrides: dict[str, Any]) -> dict[str, Any]:
    internal = dict()
    internal["__mixin_stack"] = []
    for methodName, override in overrides.items():
        if not callable(override):
            raise f"{methodName} is not callable"
        internalMethodName = f"__mixin_${methodName}"
        if dict_key_of(internal, internalMethodName) is not None:
            raise f"{methodName} duplicate overridables"
        internal[internalMethodName] = override
    return internal

def _mixin_is_override(internal: dict[str, Any]) -> bool:
    stack = internal["__mixin_stack"]
    frame = sys._getframe(1)
    methodName = frame.f_code.co_name
    if f"__mixin_${methodName}" not in internal:
        return False
    internalMethodName = f"__mixin_${methodName}"
    override = internal[internalMethodName]
    overrideName = override.__name__
    isCallSuper = array_find_index(stack, lambda s, *_: s[0] == f"{overrideName}#callSuper") != -1
    return not isCallSuper

def _mixin_call_override(internal: dict[str, Any], *args, **kwargs) -> Any:
    stack = internal["__mixin_stack"]
    frame = sys._getframe(1)
    methodName = frame.f_code.co_name
    method = frame.f_globals[methodName]
    internalMethodName = f"__mixin_${methodName}"
    override = internal[internalMethodName]
    array_push(stack, (methodName, method))
    try:
        return override(internal, *args, **kwargs)
    finally:
        array_pop(stack)

def _mixin_call_super(internal: dict[str, Any], *args, **kwargs) -> Any:
    stack = internal["__mixin_stack"]
    frame = sys._getframe(1)
    overrideName = frame.f_code.co_name
    override = frame.f_globals[overrideName]
    internalMethodName = dict_key_of(internal, override)
    methodName = string_slice(internalMethodName, len("__mixin_$"))
    method = array_find_last(stack, lambda s, *_: s[0] == methodName)[1]
    array_push(stack, (f"{overrideName}#callSuper", override))
    try:
        return method(internal, *args, **kwargs)
    finally:
        array_pop(stack)
