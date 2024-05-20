from utils.primordials import *
from utils.coroutines import *
import traceback

def main(state, args):
    if state is SuspendableInitial:
        print("Hello world!")
        abortController = abortcontroller_new()
        abortSignal = abortcontroller_get_signal(abortController)
        promise = promise_from_suspendable(test, 1, abortSignal)
        return SuspendableReturn, promise
    return SuspendableExhausted
    
def test(state, args):
    if state is SuspendableInitial:
        testArg1, testArg2 = args
        print(testArg1)
        print(testArg2)
        return SuspendableReturn, promise_from_wait(100, "Hah")
    return SuspendableExhausted

if __name__ == "__main__":
    looper = looper_new("Main")
    with looper_closure(looper):
        promise = promise_from_suspendable(main)
        promise = promise_then(promise, lambda v: print(v))
        promise = promise_catch(promise, lambda e: traceback.print_exception(e))
        promise = promise_finally(promise, lambda: exit())
    try:
        while True:
            looper_tick(looper)
    except KeyboardInterrupt:
        exit()

