from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.user import *

def _menu_show_login(state, args):
    if state is SuspendableInitial:
        gameState, console = args
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        print, input, meta = console
        meta(action="clear")
        print("=========== LOGIN ===========")
        print("Silahkan masukkan username dan paswordmu yang telah terdaftar.")
        username = input(f"{fbg()}Username: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Username hanya boleh berisi alfabet, angka, underscore, dan strip!")
        password = input(f"{fbg()}Password: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Tekan {fg('e63131')}CTRL+A{fg()} untuk melihat password", renderer=lambda v, *_: array_map(v, lambda r, *_: Rune("•", r.attribute)))
        return 2, gameState, console, username, password
    if state == 2:
        gameState, console, username, password = args
        print, input, meta = console
        if username is None or password is None:
            return SuspendableReturn, None
        meta(action="clear")
        with meta(action="foreign"):
            user_login(gameState, username, password)
        if user_is_logged_in(gameState):
            print("Berhasil login!")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return SuspendableReturn, None, selection
        return promise_from_wait(4000, 3), gameState, console
    if state == 3:
        gameState, console = args
        return SuspendableInitial, gameState, console
    return SuspendableExhausted

def _menu_show_register(state, args):
    if state is SuspendableInitial:
        gameState, console = args
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        print, input, meta = console
        meta(action="clear")
        print("=========== REGISTER ===========")
        print("Silahkan masukkan username dan password untuk register akun.")
        username = input(f"{fbg()}Username: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Username hanya boleh berisi alfabet, angka, underscore, dan strip!")
        password = input(f"{fbg()}Password: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Tekan {fg('e63131')}CTRL+A{fg()} untuk melihat password", renderer=lambda v, *_: array_map(v, lambda r, *_: Rune("•", r.attribute)))
        return 2, gameState, console, username, password
    if state == 2:
        gameState, console, username, password = args
        print, input, meta = console
        if username is None or password is None:
            return SuspendableReturn, None
        meta(action="clear")
        promise = promise_from_suspendable(user_register, gameState, console, username, password)
        return 3, gameState, console, promise
    if state == 3:
        gameState, console, *_ = args
        if user_is_logged_in(gameState):
            return SuspendableReturn, None
        return promise_from_wait(4000, 1), gameState, console
    return SuspendableExhausted

def _menu_show_logout(state, args):
    if state is SuspendableInitial:
        gameState, console = args
        print, input, meta = console
        meta(action="clear")
        print("=========== LOGOUT ===========")
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        print, input, meta = console
        meta(action="pushFlags")
        meta("keySpeed", 30)
        print("..............................")
        return 2, gameState, console, meta(action="waitContent")
    if state == 2:
        gameState, console, *_ = args
        print, input, meta = console
        meta(action="popFlags")
        meta(action="clear")
        with meta(action="foreign"):
            user_logout(gameState)
        print("Berhasil logout!")
        input("Lanjut", selectable=True)
        selection = meta(action="select")
        return SuspendableReturn, None, selection
    return SuspendableExhausted
