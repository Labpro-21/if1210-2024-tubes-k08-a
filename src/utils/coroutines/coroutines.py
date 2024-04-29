from utils.primordials import *
from typing import TypedDict, Callable, Any
import time

_Timer = TypedDict("Timer",
    id=int,
    callback=Callable[[], Any],
    timeout=int,
    repeat=bool,
    anchor=int
)

_Pollable = TypedDict("Pollable",
    callback=Callable[[], bool],
    
)

_Looper = TypedDict("Looper", 
    id=int,
    name=str,
    timerIdCounter=int,
    timers="list[_Timer]",
    pollables="list[_Pollable]",
    microtasks="list[Callable[[], Any]]"
)

_looper_id_counter = 0
_looper_current_id = -1
_loopers: "dict[int, _Looper]" = {}

def _looper_new(name: str) -> int:
    global _looper_id_counter, _loopers
    looperId = _looper_id_counter
    _looper_id_counter += 1
    looper: _Looper = dict(
        id=looperId,
        name=name,
        timerIdCounter=0,
        timers=[],
        pollables=[],
        microtasks=[]
    )
    _loopers[looperId] = looper
    return looperId

def _looper_get_current() -> _Looper:
    global _looper_current_id, _loopers
    return _loopers[_looper_current_id]

def _looper_closure(looperId: int) -> Any:
    closure = dict()
    def saveLastLooperId(self):
        global _looper_current_id
        self["lastLooperId"] = _looper_current_id
        _looper_current_id = looperId
    def restoreLastLooperId(self):
        global _looper_current_id
        _looper_current_id = self["lastLooperId"]
        self["lastLooperId"] = None
    setattr(closure, "__enter__", saveLastLooperId)
    setattr(closure, "__exit__", restoreLastLooperId)
    return closure

def _looper_tick(looperId: int) -> None:
    global _looper_current_id
    lastLooperId = _looper_current_id
    _looper_current_id = looperId
    try:
        looper = _looper_get_current()
        _looper_tick_timers(looper)
        _looper_tick_microtasks(looper)
        _looper_tick_pollables(looper)
        _looper_tick_microtasks(looper)
    finally:
        _looper_current_id = lastLooperId

def _looper_tick_timers(looper: _Looper) -> None:
    timers = looper["timers"]
    timersCopy = array_slice(timers)
    now = _now()
    for timer in timersCopy:
        if now - timer["anchor"] < timer["timeout"]:
            continue
        timer["callback"]()
        now = _now()
        if not timer["repeat"]:
            array_splice(timers, array_index_of(timers, timer), 1)

def _looper_tick_pollables(looper: _Looper) -> None:
    pollables = looper["pollables"]
    nextPollables = array_map(pollables, lambda p: p["callback"]())
    for i in range(len(nextPollables) - 1, -1, -1):
        if nextPollables:
           continue
        array_splice(pollables, i, 1)

def _looper_tick_microtasks(looper: _Looper) -> None:
    microtasks = array_splice(looper["microtasks"], 0)
    for microtask in microtasks:
        microtask()

def _looper_next_timer_id(looper: _Looper) -> int:
    timerId = looper["timerIdCounter"]
    looper["timerIdCounter"] += 1
    return timerId

def _set_timeout(callback: Callable[[], Any], timeout: int) -> int:
    looper = _looper_get_current()
    timers = looper["timers"]
    timerId = _looper_next_timer_id(looper)
    timer: _Timer = dict(
        id=timerId,
        callback=callback,
        timeout=timeout,
        repeat=False,
        anchor=_now()
    )
    array_push(timers, timer)
    return timerId

def _set_interval(callback: Callable[[], Any], timeout: int) -> int:
    looper = _looper_get_current()
    timers = looper["timers"]
    timerId = _looper_next_timer_id(looper)
    timer: _Timer = dict(
        id=timerId,
        callback=callback,
        timeout=timeout,
        repeat=True,
        anchor=_now()
    )
    array_push(timers, timer)
    return timerId

def _clear_timeout(id: int) -> None:
    looper = _looper_get_current()
    timers = looper["timers"]
    index = array_find_index(timers, lambda t: not t["repeat"] and t["id"] == id)
    if index == -1:
        return
    array_splice(timers, index, 1)

def _clear_interval(id: int) -> None:
    looper = _looper_get_current()
    timers = looper["timers"]
    index = array_find_index(timers, lambda t: t["repeat"] and t["id"] == id)
    if index == -1:
        return
    array_splice(timers, index, 1)

def _set_immediate(callback: Callable[[], Any]) -> None:
    looper = _looper_get_current()
    microtasks = looper["microtasks"]
    array_push(microtasks, callback)

def _panic(message: str) -> None:
    print(message)
    exit()

def _now() -> float:
    return time.monotonic() * 1000
