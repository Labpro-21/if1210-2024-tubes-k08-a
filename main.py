from utils.primordials import *
from utils.coroutines import *

def loop():
    pass

if __name__ == "__main__":
    looper = looper_new("Main")
    with looper_closure(looper):
        set_interval(loop, 15)
    while True:
        looper_tick(looper)
