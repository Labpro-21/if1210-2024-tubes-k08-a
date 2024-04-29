from .coroutines import _looper_new, _looper_get_current, _looper_closure, _looper_tick, _set_timeout, _set_interval, _clear_timeout, _clear_interval, _set_immediate

looper_new = _looper_new
looper_get_current = _looper_get_current
looper_closure = _looper_closure
looper_tick = _looper_tick
set_timeout = _set_timeout
set_interval = _set_interval
clear_timeout = _clear_timeout
clear_interval = _clear_interval
set_immediate = _set_immediate
