from utils.primordials import *
from utils.mixin import *
from utils.math import *
from .console import _View, _view_new, _Driver, _Pos, _Dim, _pos_from_absolute, _dim_from_absolute, _driver_get_size

_TopLevel = _View

def _toplevel_new(driver: _Driver, **kwargs) -> _TopLevel:
    return dict_with(
        _view_new(
            driver,
            _view_get_x=_toplevel_get_x,
            _view_get_y=_toplevel_get_y,
            _view_get_width=_toplevel_get_width,
            _view_get_height=_toplevel_get_height,
            _view_get_content_size=_toplevel_get_content_size,
            _view_set_x=_toplevel_set_x,
            _view_set_y=_toplevel_set_y,
            _view_set_width=_toplevel_set_width,
            _view_set_height=_toplevel_set_height,
            _view_set_content_size=_toplevel_set_content_size
        ),
        **mixin_new(kwargs)
    )
def _toplevel_get_x(toplevel: _TopLevel) -> _Pos:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    return _pos_from_absolute(0)
def _toplevel_get_y(toplevel: _TopLevel) -> _Pos:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    return _pos_from_absolute(0)
def _toplevel_get_width(toplevel: _TopLevel) -> _Dim:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    return _dim_from_absolute(_driver_get_size(toplevel["driver"]).w)
def _toplevel_get_height(toplevel: _TopLevel) -> _Dim:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    return _dim_from_absolute(_driver_get_size(toplevel["driver"]).h)
def _toplevel_get_content_size(toplevel: _TopLevel) -> Size:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    return _driver_get_size(toplevel["driver"])
def _toplevel_set_x(toplevel: _TopLevel, x: _Pos) -> None:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    raise "Not supported"
def _toplevel_set_y(toplevel: _TopLevel, y: _Pos) -> None:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    raise "Not supported"
def _toplevel_set_width(toplevel: _TopLevel, w: _Dim) -> None:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    raise "Not supported"
def _toplevel_set_height(toplevel: _TopLevel, h: _Dim) -> None:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    raise "Not supported"
def _toplevel_set_content_size(toplevel: _TopLevel, contentSize: Size) -> None:
    if mixin_is_override(toplevel):
        return mixin_call_override(toplevel)
    raise "Not supported"
