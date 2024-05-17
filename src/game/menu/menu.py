from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.user import *

def _menu_show_loading_initial(state, args):
    if state is SuspendableInitial:
        gameState, visual = args
        loadingInfo = visual_show_simple_dialog(visual, "LOADING", "Please wait a moment",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.3), height=dim_from_absolute(5), padding=(0, 0, 0, 0),
            horizontalAlignment="Center")
        def progress(value):
            loadingInfo["setContent"](f"Initializing: {value * 100:.2f}%")
        promise = visual_load_splash(visual, "loading1.gif.txt", progress)
        return SuspendableReturn, promise
    return SuspendableExhausted

def _menu_show_loading_splash(state, args):
    if state is SuspendableInitial:
        gameState, visual, splashes = args
        loadingScreen = visual_show_splash(visual, "loading1.gif.txt")
        loadingScreen["play"](60)
        loadingInfo = visual_show_simple_dialog(visual, "LOADING", "Please wait a moment",
            x=pos_from_center(), y=pos_from_factor(0.8),
            width=dim_from_factor(0.3), height=dim_from_absolute(5), padding=(0, 0, 0, 0), 
            horizontalAlignment="Center", parent=loadingScreen)
        progressValues = [0 for _ in range(len(splashes))]
        def progress(index, value):
            progressValues[index] = value
            loadingText = array_map(progressValues, lambda v, i, *_: f"Loading {splashes[i][0]}: {v * 100:.2f}%")
            loadingText = array_join(loadingText, "\n")
            loadingInfo["setContent"](loadingText)
        promises = array_map(splashes, lambda s, i, *_: visual_load_splash(visual, s[1], lambda v: progress(i, v)))
        return SuspendableReturn, promise_all(promises)
    return SuspendableExhausted

def _menu_show_menu(state, args):
    if state is SuspendableInitial:
        gameState, console, *_ = args
        print, input, meta = console
        meta(action="clear")
        print("=========== MENU ===========")
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        user = user_get_current(gameState)
        if user is None:
            return 2, gameState, console
        if user.role == "agent":
            return 4, gameState, console, user
        if user.role == "admin":
            return 6, gameState, console, user
    if state == 2:
        gameState, console = args
        print, input, meta = console
        print("Kamu belum login sebagai role apapun. Silahkan login terlebih dahulu.")
        input("Login", "Masuk ke dalam akun yang sudah terdaftar", selectable=True)
        input("Register", "Membuat akun baru", selectable=True)
        input("Exit", selectable=True)
        selection = meta(action="select")
        return 3, gameState, console, selection
    if state == 3:
        gameState, console, selection = args
        if selection is None:
            return SuspendableReturn, None
        if selection == "Login":
            return SuspendableInitial, gameState, console, promise_from_suspendable(_menu_show_login, gameState, console)
        if selection == "Register":
            return SuspendableInitial, gameState, console, promise_from_suspendable(_menu_show_register, gameState, console)
        if selection == "Exit":
            return "checkExit", gameState, console, promise_from_suspendable(_menu_show_exit, gameState, console)
    if state == 4:
        gameState, console, user = args
        print, input, meta = console
        print(f"Halo Agent {user.username}. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian. Berikut adalah hal-hal yang dapat kamu lakukan sekarang:")
        input("Monster", "Melihat owca-dex yang dimiliki oleh Agent", selectable=True)
        input("Logout", "Keluar dari akun yang sedang digunakan", selectable=True)
        input("Exit", selectable=True)
        selection = meta(action="select")
        return 5, gameState, console, selection
    if state == 5:
        gameState, console, selection = args
        if selection is None:
            return SuspendableReturn, None
        if selection == "Monster":
            return SuspendableInitial, gameState, console, promise_from_suspendable(_menu_show_monster, gameState, console)
        if selection == "Logout":
            return SuspendableInitial, gameState, console, promise_from_suspendable(_menu_show_logout, gameState, console)
        if selection == "Exit":
            return "checkExit", gameState, console, promise_from_suspendable(_menu_show_exit, gameState, console)
    if state == 6:
        gameState, console, user = args
        print, input, meta = console
        print("Selamat datang, Admin. Berikut adalah hal-hal yang dapat kamu lakukan:")
        input("Shop", "Melakukan manajemen pada SHOP sebagai tempat jual beli peralatan Agent", selectable=True)
        input("Logout", "Keluar dari akun yang sedang digunakan", selectable=True)
        input("Exit", selectable=True)
        selection = meta(action="select")
        return 7, gameState, console, selection
    if state == 7:
        gameState, console, selection = args
        if selection is None:
            return SuspendableReturn, None
        if selection == "Shop":
            return SuspendableInitial, gameState, console, promise_from_suspendable(_menu_show_shop, gameState, console)
        if selection == "Logout":
            return SuspendableInitial, gameState, console, promise_from_suspendable(_menu_show_logout, gameState, console)
        if selection == "Exit":
            return "checkExit", gameState, console, promise_from_suspendable(_menu_show_exit, gameState, console)
    if state == "checkExit":
        gameState, console, exit = args
        if not exit:
            return SuspendableInitial, gameState, console
        return SuspendableReturn, None
    return SuspendableExhausted

def _menu_show_login(state, args):
    if state is SuspendableInitial:
        gameState, console = args
        print, input, meta = console
        meta(action="clear")
        print("=========== LOGIN ===========")
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        print, input, meta = console
        print("Silahkan masukkan username dan paswordmu yang telah terdaftar.")
        username = input(f"{fbg()}Username: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Username hanya boleh berisi alfabet, angka, underscore, dan strip!")
        password = input(f"{fbg()}Password: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Tekan {fg('e63131')}CTRL+A{fg()} untuk melihat password", renderer=lambda v, *_: array_map(v, lambda r, *_: Rune("•", r.attribute)))
        return 2, gameState, console, username, password
    if state == 2:
        gameState, console, username, password = args
        print, input, meta = console
        if password is None:
            return SuspendableReturn, None
        with meta(action="foreign"):
            user_login(gameState, username, password)
        if user_is_logged_in(gameState):
            return SuspendableReturn, None
        return promise_from_wait(4000, 3), gameState, console
    if state == 3:
        gameState, console = args
        return SuspendableInitial, gameState, console
    return SuspendableExhausted

def _menu_show_register(state, args):
    if state is SuspendableInitial:
        gameState, console = args
        print, input, meta = console
        meta(action="clear")
        print("=========== REGISTER ===========")
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        print, input, meta = console
        print("Silahkan masukkan username dan password untuk register akun.")
        username = input(f"{fbg()}Username: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Username hanya boleh berisi alfabet, angka, underscore, dan strip!")
        password = input(f"{fbg()}Password: {fg('e6dee6')}{bg('734118')}", f"{fbg()}Tekan {fg('e63131')}CTRL+A{fg()} untuk melihat password", renderer=lambda v, *_: array_map(v, lambda r, *_: Rune("•", r.attribute)))
        return 2, gameState, console, username, password
    if state == 2:
        gameState, console, username, password = args
        print, input, meta = console
        if password is None:
            return SuspendableReturn, None
        with meta(action="foreign"):
            user_register(gameState, username, password)
        if user_is_logged_in(gameState):
            return SuspendableReturn, None
        return promise_from_wait(4000, 3), gameState, console
    if state == 3:
        gameState, console = args
        return SuspendableInitial, gameState, console
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
        gameState, console = args
        print, input, meta = console
        meta(action="popFlags")
        with meta(action="foreign"):
            user_logout(gameState)
        return SuspendableReturn, None
    return SuspendableExhausted

def _menu_show_exit(state, args):
    if state is SuspendableInitial:
        gameState, console = args
        print, input, meta = console
        meta(action="clear")
        print("=========== EXIT ===========")
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        print, input, meta = console
        print("Yakin mau keluar?")
        input("Kembali", selectable=True)
        input(f"{fg('e63131')}Keluar{fg()}", selectable=True)
        selection = meta(action="select")
        return 2, gameState, console, selection
    if state == 2:
        gameState, console, selection = args
        if selection is None or selection == "Kembali":
            return SuspendableReturn, False
        return SuspendableReturn, True
    return SuspendableExhausted
