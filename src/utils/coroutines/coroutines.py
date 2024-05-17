from utils.primordials import *
from typing import TypedDict, Callable, Any, Literal, Callable, Union, TypeVar, Optional
import sys
import time

_Timer = TypedDict("Timer",
    id=int,
    callback=Callable[[], Any],
    timeout=float,
    repeat=bool,
    anchor=float
)

_Pollable = TypedDict("Pollable",
    callback=Callable[[], bool],
    
)

_Looper = TypedDict("Looper", 
    id=int,
    name=str,
    timerIdCounter=int,
    timers=list[_Timer],
    pollables=list[_Pollable],
    immediates=list[Callable[[], Any]],
    microtasks=list[Callable[[], Any]],
)

__looper_id_counter = 0
__looper_current_id = -1
__loopers: dict[int, _Looper] = dict()

def _looper_new(name: str) -> int:
    global __looper_id_counter, __loopers
    looperId = __looper_id_counter
    __looper_id_counter += 1
    looper: _Looper = dict(
        id=looperId,
        name=name,
        timerIdCounter=0,
        timers=[],
        pollables=[],
        immediates=[],
        microtasks=[],
    )
    __loopers[looperId] = looper
    return looperId

def _looper_get_current() -> _Looper:
    global __looper_current_id, __loopers
    return __loopers[__looper_current_id]

def __looper_make_closure_type():
    def __init__(self, looperId: int):
        self.looperId = looperId
        self.lastLooperId = -1
    def __enter__(self):
        global __looper_current_id
        self.lastLooperId = __looper_current_id
        __looper_current_id = self.looperId
    def __exit__(self, *_):
        global __looper_current_id
        __looper_current_id = self.lastLooperId
        self.lastLooperId = -1
        return False
    ClosureType = type("Closure", (object,), dict(
        __init__=__init__,
        __enter__=__enter__,
        __exit__=__exit__
    ))
    return ClosureType
_ClosureType = __looper_make_closure_type()

def _looper_closure(looperId: int) -> _ClosureType:
    return _ClosureType(looperId)

def _looper_needs_tick(looperId: int) -> bool:
    looper = __loopers[looperId]
    timers = looper["timers"]
    pollables = looper["pollables"]
    immediates = looper["immediates"]
    microtasks = looper["microtasks"]
    return len(timers) > 0 or len(pollables) > 0 or len(immediates) > 0 or len(microtasks) > 0

def _looper_tick(looperId: int) -> None:
    global __looper_current_id
    lastLooperId = __looper_current_id
    __looper_current_id = looperId
    try:
        looper = _looper_get_current()
        _looper_tick_timers(looper)
        _looper_tick_microtasks(looper)
        _looper_tick_pollables(looper)
        _looper_tick_microtasks(looper)
        _looper_tick_immediates(looper)
        _looper_tick_microtasks(looper)
    finally:
        __looper_current_id = lastLooperId

def _looper_tick_timers(looper: _Looper) -> None:
    timers = looper["timers"]
    timersCopy = array_slice(timers)
    now = __now()
    for timer in timersCopy:
        if now - timer["anchor"] < timer["timeout"]:
            continue
        timer["callback"]()
        now = __now()
        timer["anchor"] = now
        if not timer["repeat"]:
            array_splice(timers, array_index_of(timers, timer), 1)

def _looper_tick_pollables(looper: _Looper) -> None:
    pollables = looper["pollables"]
    nextPollables = array_map(pollables, lambda p, *_: p["callback"]())
    for i in range(len(nextPollables) - 1, -1, -1):
        if nextPollables:
           continue
        array_splice(pollables, i, 1)

def _looper_tick_immediates(looper: _Looper) -> None:
    immediates = array_splice(looper["immediates"], 0)
    for immediate in immediates:
        immediate()

def _looper_tick_microtasks(looper: _Looper) -> None:
    while True:
        microtasks = array_splice(looper["microtasks"], 0)
        for microtask in microtasks:
            microtask()
        if len(looper["microtasks"]) == 0:
            break

def __looper_next_timer_id(looper: _Looper) -> int:
    timerId = looper["timerIdCounter"]
    looper["timerIdCounter"] += 1
    return timerId

def _set_timeout(callback: Callable[[], Any], timeout: float) -> int:
    looper = _looper_get_current()
    timers = looper["timers"]
    timerId = __looper_next_timer_id(looper)
    timer: _Timer = dict(
        id=timerId,
        callback=callback,
        timeout=timeout,
        repeat=False,
        anchor=__now()
    )
    array_push(timers, timer)
    return timerId

def _set_interval(callback: Callable[[], Any], timeout: float) -> int:
    looper = _looper_get_current()
    timers = looper["timers"]
    timerId = __looper_next_timer_id(looper)
    timer: _Timer = dict(
        id=timerId,
        callback=callback,
        timeout=timeout,
        repeat=True,
        anchor=__now()
    )
    array_push(timers, timer)
    return timerId

def _clear_timeout(timerId: int) -> None:
    looper = _looper_get_current()
    timers = looper["timers"]
    index = array_find_index(timers, lambda t, *_: not t["repeat"] and t["id"] == timerId)
    if index == -1:
        return
    array_splice(timers, index, 1)

def _clear_interval(timerId: int) -> None:
    looper = _looper_get_current()
    timers = looper["timers"]
    index = array_find_index(timers, lambda t, *_: t["repeat"] and t["id"] == timerId)
    if index == -1:
        return
    array_splice(timers, index, 1)

def _set_immediate(callback: Callable[[], Any]) -> None:
    looper = _looper_get_current()
    immediates = looper["immediates"]
    array_push(immediates, callback)

def _next_tick(callback: Callable[[], Any]) -> None:
    looper = _looper_get_current()
    microtasks = looper["microtasks"]
    array_push(microtasks, callback)

def __now() -> float:
    return time.monotonic() * 1000

_PromiseState = Literal["Pending", "Resolved", "Rejected"]
_PromiseValue = TypeVar("_PromiseValue")
_PromiseChainValue = TypeVar("_PromiseChainValue")
__Promise = TypedDict("Promise",
    status=_PromiseState,
    value=_PromiseValue,
    notifies=list[Callable[["Promise[_PromiseChainValue]"], None]]
)
Promise = Union[__Promise, _PromiseValue]
_PromiseResolve = Callable[[_PromiseValue], None]
_PromiseReject = Callable[[Any], None]

def _promise_new(executor: Callable[[_PromiseResolve[_PromiseValue], _PromiseReject], Any]) -> Promise[_PromiseValue]:
    promise: Promise[_PromiseValue] = dict(
        __type=__Promise,
        status="Pending",
        value=None,
        notifies=[]
    )
    def notifyFunction(promise: Promise[_PromiseChainValue]):
        status = promise["status"]
        value = promise["value"]
        if status == "Resolved":
            resolveFunction(value)
        if status == "Rejected":
            rejectFunction(value)
    def resolveFunction(value: _PromiseValue) -> None:
        if promise["status"] != "Pending":
            return
        if _as_promise(value) is not None:
            __promise_notify(value, notifyFunction)
            return
        promise["status"] = "Resolved"
        promise["value"] = value
        for notify in promise["notifies"]:
            _next_tick(lambda: notify(promise))
    def rejectFunction(value: Any) -> None:
        if promise["status"] != "Pending":
            return
        promise["status"] = "Rejected"
        promise["value"] = value
        for notify in promise["notifies"]:
            _next_tick(lambda: notify(promise))
        # handle uncaught promise function if notifies is 0
    try:
        executor(resolveFunction, rejectFunction)
    except:
        rejectFunction(__promise_get_exception())
    return promise

def _as_promise(value: Any) -> Optional[Promise[Any]]:
    if type(value) is not dict or "__type" not in value or value["__type"] == Promise:
        return None
    return value

def __promise_notify(promise: Promise[_PromiseValue], notify: Callable[[Promise[_PromiseChainValue]], None]) -> None:
    if promise["status"] != "Pending":
        notify(promise)
    notifies = promise["notifies"]
    array_push(notifies, notify)

def __promise_get_exception() -> Any:
    errorType, error, _ = sys.exc_info()
    if errorType is SystemExit or errorType is KeyboardInterrupt:
        raise error
    return error

def _promise_then(promise: Promise[_PromiseValue], onResolved: Callable[[_PromiseValue], _PromiseChainValue], onRejected: Optional[Callable[[Any], _PromiseChainValue]] = None) -> Promise[_PromiseChainValue]:
    def executor(resolve, reject):
        def notifiy(promise: Promise[_PromiseValue]):
            status = promise["status"]
            value = promise["value"]
            try:
                if status == "Resolved":
                    resolve(onResolved(value))
                if status == "Rejected":
                    if onRejected is None:
                        reject(value)
                    else:
                        resolve(onRejected(value))
            except:
                reject(__promise_get_exception())
        __promise_notify(promise, notifiy)
    return _promise_new(executor)

def _promise_catch(promise: Promise[_PromiseValue], onRejected: Callable[[Any], _PromiseChainValue]) -> Promise[Union[_PromiseValue, _PromiseChainValue]]:
    def executor(resolve, reject):
        def notifiy(promise: Promise[_PromiseValue]):
            status = promise["status"]
            value = promise["value"]
            try:
                if status == "Resolved":
                    resolve(value)
                if status == "Rejected":
                    resolve(onRejected(value))
            except:
                reject(__promise_get_exception())
        __promise_notify(promise, notifiy)
    return _promise_new(executor)

def _promise_finally(promise: Promise[_PromiseValue], onFinally: Callable[[], Any]) -> Promise[_PromiseValue]:
    def executor(resolve, reject):
        def notifiy(promise: Promise[_PromiseValue]):
            status = promise["status"]
            value = promise["value"]
            try:
                onFinally()
                if status == "Resolved":
                    resolve(value)
                if status == "Rejected":
                    reject(value)
            except:
                reject(__promise_get_exception())
        __promise_notify(promise, notifiy)
    return _promise_new(executor)

def _promise_resolved(value: _PromiseValue) -> Promise[_PromiseValue]:
    def executor(resolve, _):
        resolve(value)
    return _promise_new(executor)

def _promise_rejected(value: Any) -> Promise[Any]:
    def executor(_, reject):
        reject(value)
    return _promise_new(executor)

def _promise_all(promises: list[Promise[_PromiseValue]]) -> Promise[list[_PromiseValue]]:
    def executor(resolve, reject):
        i = -1
        result: list[_PromiseValue] = []
        def next():
            nonlocal i
            i += 1
            if i >= len(promises):
                resolve(result)
                return
            promise = promises[i]
            if _as_promise(promise) is None:
                array_push(result, promise)
                next()
                return
            def onResolved(value: _PromiseValue):
                array_push(result, value)
                next()
            def onRejected(value: Any):
                reject(value)
            _promise_then(promise, onResolved, onRejected)
        next()
    return _promise_new(executor)

def _promise_all_settled(promises: list[Promise[_PromiseValue]]) -> Promise[list[tuple[Literal["Resolved", "Rejected"], _PromiseValue]]]:
    def executor(resolve, _):
        i = -1
        result: list[tuple[Literal["Resolved", "Rejected"], _PromiseValue]] = []
        def next():
            nonlocal i
            i += 1
            if i >= len(promises):
                resolve(result)
                return
            promise = promises[i]
            if _as_promise(promise) is None:
                array_push(result, ("Resolved", promise))
                next()
                return
            def onResolved(value: _PromiseValue):
                array_push(result, ("Resolved", value))
                next()
            def onRejected(value: Any):
                array_push(result, ("Rejected", value))
                next()
            _promise_then(promise, onResolved, onRejected)
        next()
    return _promise_new(executor)

def _promise_any(promises: list[Promise[_PromiseValue]]) -> Promise[_PromiseValue]:
    def executor(resolve, reject):
        done = False
        errors: list[Any] = []
        for i in range(len(promises)):
            if done:
                break
            promise = promises[i]
            if _as_promise(promise) is None:
                done = True
                resolve(promise)
                break
            def onResolved(value: _PromiseValue):
                nonlocal done
                if done:
                    return
                done = True
                resolve(value)
            def onRejected(value: Any):
                nonlocal done
                if done:
                    return
                array_push(errors, value)
                if len(errors) < len(promises):
                    return
                done = True
                reject(errors)
            _promise_then(promise, onResolved, onRejected)
    return _promise_new(executor)

def _promise_race(promises: list[Promise[_PromiseValue]]) -> Promise[_PromiseValue]:
    def executor(resolve, reject):
        done = False
        for i in range(len(promises)):
            if done:
                break
            promise = promises[i]
            if _as_promise(promise) is None:
                done = True
                resolve(promise)
                break
            def onResolved(value: _PromiseValue):
                nonlocal done
                if done:
                    return
                done = True
                resolve(value)
            def onRejected(value: Any):
                nonlocal done
                if done:
                    return
                done = True
                reject(value)
            _promise_then(promise, onResolved, onRejected)
    return _promise_new(executor)

_SuspendableInitial = dict()
_SuspendableReturn = dict()
_SuspendableExhausted = dict()

def _promise_from_suspendable(handle: Callable[[str], tuple], *initialArgs, initialState: str = _SuspendableInitial) -> Promise[Any]:
    def executor(resolve, reject):
        state = initialState
        args = tuple_to_array(initialArgs)
        def next():
            nonlocal state, args
            if _as_promise(state) is not None:
                def onResolved(result: str):
                    nonlocal state
                    state = result
                    next()
                _promise_then(state, onResolved, reject)
                return
            if array_some(args, lambda a, *_: _as_promise(a) is not None):
                def onResolved(result: list[Any]):
                    nonlocal args
                    args = result
                    next()
                _promise_then(_promise_all(args), onResolved, reject)
                return
            if state is _SuspendableReturn:
                resolve(args[0])
                return
            try:
                result = handle(state, (*args,))
                if _as_promise(result) is None:
                    if result is _SuspendableExhausted:
                        raise "Exhausted state"
                    if type(result) is tuple:
                        state, *args = result
                    else:
                        state = result
                        args = []
                    next()
                    return
                def onResolved(result: tuple):
                    nonlocal state, args
                    if result is _SuspendableExhausted:
                        raise "Exhausted state"
                    if type(result) is tuple:
                        state, *args = result
                    else:
                        state = result
                        args = []
                    next()
                _promise_then(result, onResolved, reject)
            except:
                reject(__promise_get_exception())
        next()
    return _promise_new(executor)

def _promise_from_wait(timeout: int, value: _PromiseValue = None) -> Promise[_PromiseValue]:
    def executor(resolve, _):
        def onTimeout():
            resolve(value)
        _set_timeout(onTimeout, timeout)
    return _promise_new(executor)
