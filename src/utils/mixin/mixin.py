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

def _mixin_set_override(internal: dict[str, Any], **overrides) -> None:
    for methodName, override in overrides.items():
        internalMethodName = f"__mixin_${methodName}"
        if override is None:
            if internalMethodName in internal:
                del internal[internalMethodName]
            continue
        if not callable(override):
            raise f"{methodName} is not callable"
        internal[internalMethodName] = override

def _mixin_get_override(internal: dict[str, Any], methodName) -> Any:
    internalMethodName = f"__mixin_${methodName}"
    if internalMethodName not in internal:
        return None
    override = internal[internalMethodName]
    return override

def _mixin_is_override(internal: dict[str, Any]) -> bool:
    stack = internal["__mixin_stack"]
    frame = sys._getframe(1)
    methodName = frame.f_code.co_name
    internalMethodName = f"__mixin_${methodName}"
    if internalMethodName not in internal:
        return False
    if len(stack) == 0:
        return True
    override = internal[internalMethodName]
    overrideName = override.__name__
    isCallSuper = stack[len(stack) - 1][0] == f"{overrideName}#callSuper"
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

def _mixin_call_super(internal: dict[str, Any], *args, __mixin_self = None, **kwargs) -> Any:
    stack = internal["__mixin_stack"]
    frame = sys._getframe(1)
    overrideName = frame.f_code.co_name
    alternateOverrideName = f"__mixin_{overrideName}"
    override = __mixin_self if __mixin_self is not None else frame.f_locals[alternateOverrideName] if alternateOverrideName in frame.f_locals else frame.f_globals[overrideName]
    internalMethodName = dict_key_of(internal, override)
    methodName = string_slice(internalMethodName, len("__mixin_$"))
    method = array_find_last(stack, lambda s, *_: s[0] == methodName)[1]
    array_push(stack, (f"{overrideName}#callSuper", override))
    try:
        return method(internal, *args, **kwargs)
    finally:
        array_pop(stack)
