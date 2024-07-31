from utils.primordials import *
from utils.mixin import *

def a_new(a, **kwargs):
    return dict(
        a=a,
        **mixin_new(kwargs)
    )

def a_test(a, b):
    if mixin_is_override(a):
        return mixin_call_override(a, b)
    # print(mixin_call_super(a, b + " a"))
    print(a)
    return f'a {a["a"]} {b}'

def b_new(b, **kwargs):
    return dict_with(
        a_new(
            b + 1,
            a_test=b_test
        ),
        b=b,
        **mixin_new(kwargs)
    )

def b_test(b, c):
    if mixin_is_override(b):
        return mixin_call_override(b, c)
    print(mixin_call_super(b, c + " b"))
    return f'b {b["a"]} {b["b"]} {c}'

def c_new(c, **kwargs):
    return dict_with(
        b_new(
            c + 1,
            b_test=c_test
        ),
        c=c,
        **mixin_new(kwargs)
    )

def c_test(c, d):
    if mixin_is_override(c):
        return mixin_call_override(c, d)
    print(mixin_call_super(c, d + " c"))
    return f'c {c["a"]} {c["b"]} {c["c"]} {d}'

some_c = c_new(0)
print(a_test(some_c, "lol"))
