from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.user import *

def _menu_show_loading_initial(state, args):
    if state is SuspendableInitial:
        gameState, = args
        visual = gamestate_get_visual(gameState)
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
        gameState, splashes = args
        visual = gamestate_get_visual(gameState)
        loadingScreen = visual_show_splash(visual, "loading1.gif.txt")
        loadingScreen["play"](60, True)
        loadingInfo = visual_show_simple_dialog(visual, "LOADING", "Please wait a moment",
            x=pos_from_center(), y=pos_sub(pos_from_factor(0.8), pos_from_absolute(len(splashes) // 2)),
            width=dim_from_factor(0.4), height=dim_from_absolute(4 + len(splashes)), padding=(0, 0, 0, 0), 
            horizontalAlignment="Center", parent=loadingScreen)
        text_formatter_set_wordwrap(view_get_text_formatter(loadingInfo["contentView"]), False)
        progressValues = [0 for _ in range(len(splashes))]
        def progress(index, value):
            progressValues[index] = value
            loadingText = array_map(progressValues, lambda v, i, *_: f"Loading {splashes[i][0]}: {v * 100:.2f}%" if v < 1 else f"Loaded {splashes[i][0]}")
            loadingText = array_join(loadingText, "\n")
            loadingInfo["setContent"](loadingText)
        promises = array_map(splashes, lambda s, i, *_: visual_load_splash(visual, s[1], lambda v: progress(i, v)))
        return SuspendableReturn, promise_all(promises)
    return SuspendableExhausted

def _menu_show_main_menu(state, args):
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
            return SuspendableInitial, gameState, console
        if selection == "Login":
            return SuspendableReturn, "guest:login"
        if selection == "Register":
            return SuspendableReturn, "guest:register"
        if selection == "Exit":
            return SuspendableReturn, "guest:exit"
    if state == 4:
        gameState, console, user = args
        print, input, meta = console
        print(f"Halo Agent {user.username}. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian. Berikut adalah hal-hal yang dapat kamu lakukan sekarang:")
        input("Play", "Memulai permainan", selectable=True)
        input("Logout", "Keluar dari akun yang sedang digunakan", selectable=True)
        input("Exit", selectable=True)
        selection = meta(action="select")
        return 5, gameState, console, selection
    if state == 5:
        gameState, console, selection = args
        if selection is None:
            return SuspendableInitial, gameState, console
        if selection == "Play":
            return SuspendableReturn, "agent:play"
        if selection == "Logout":
            return SuspendableReturn, "agent:logout"
        if selection == "Exit":
            return SuspendableReturn, "agent:exit"
    if state == 6:
        gameState, console, user = args
        print, input, meta = console
        print("Selamat datang, Admin. Berikut adalah hal-hal yang dapat kamu lakukan:")
        input("Shop Management", "Melakukan manajemen pada SHOP sebagai tempat jual beli peralatan Agent", selectable=True)
        input("Debug Test", "Kumpulan debug untuk testing program", selectable=True)
        input("Logout", "Keluar dari akun yang sedang digunakan", selectable=True)
        input("Exit", selectable=True)
        selection = meta(action="select")
        return 7, gameState, console, selection
    if state == 7:
        gameState, console, selection = args
        if selection is None:
            return SuspendableInitial, gameState, console
        if selection == "Shop Management":
            return SuspendableReturn, "admin:shop_management"
        if selection == "Debug Test":
            return SuspendableReturn, "admin:debug_test"
        if selection == "Logout":
            return SuspendableReturn, "admin:logout"
        if selection == "Exit":
            return SuspendableReturn, "admin:exit"
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
