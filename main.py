from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.database import *
from game.menu import *
from game.battle import *
from os import path
import traceback

def main(state, args):
    if state is SuspendableInitial:
        currentDirectory = path.dirname(__file__)
        savesDirectory = path.join(currentDirectory, "./data/saves/test-save/")
        assetsDirectory = path.join(currentDirectory, "./data/assets/")
        gameState = gamestate_new(savesDirectory)
        visual = gamestate_get_visual(gameState)
        visual_set_directory(visual, assetsDirectory)
        def tick():
            visual_tick(visual)
            visual_draw(visual)
        set_interval(tick, 15)
        gamestate_set_user_id(gameState, 1)
        return "initializing", gameState
    if state == "initializing":
        gameState, *_ = args
        promise = promise_from_suspendable(menu_show_loading_initial, gameState)
        return "menuInit", gameState, promise
    if state == "loading":
        gameState, *_ = args
        promise = promise_from_suspendable(menu_show_loading_splash, gameState, [("menu splash", "menu_background.gif.txt")])
        return "menuInit", gameState, promise
    if state == "menuInit":
        gameState, *_ = args
        visual = gamestate_get_visual(gameState)
        menuBackground = None
        # menuBackground = visual_show_splash(visual, "menu_background.gif.txt")
        # menuBackground["play"](60, True)
        menuView = visual_show_simple_dialog(visual, parent=menuBackground)
        console = visual_with_mock(visual, menuView, keySpeed=120, hasTitle=True)
        # return "menu", gameState, console
        return "menuOption", gameState, console, "admin:debug_test"
    if state == "menu":
        gameState, console, *_ = args
        print, input, meta = console
        meta(action="setAsCurrentView")
        menu = promise_from_suspendable(menu_show_main_menu, gameState, console)
        return "menuOption", gameState, console, menu
    if state == "menuOption":
        gameState, console, menu = args
        if menu == "guest:login":
            return "menu", gameState, console, promise_from_suspendable(menu_show_login, gameState, console)
        if menu == "guest:register":
            return "menu", gameState, console, promise_from_suspendable(menu_show_register, gameState, console)
        if menu == "agent:play":
            return -1
        if menu == "admin:shop_management":
            return -1
        if menu == "admin:debug_test":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_test, gameState, console)
        if menu == "agent:logout" or menu == "admin:logout":
            return "menu", gameState, console, promise_from_suspendable(menu_show_logout, gameState, console)
        if menu == "guest:exit" or menu == "agent:exit" or menu == "admin:exit":
            return "checkExit", gameState, console, promise_from_suspendable(menu_show_exit, gameState, console)
    if state == "checkExit":
        gameState, console, confirmExit = args
        if confirmExit:
            return -1
        return "menu", gameState, console
    if state == -1:
        return SuspendableReturn, None
    return SuspendableExhausted

if __name__ == "__main__":
    looper = looper_new("Main")
    with looper_closure(looper):
        promise = promise_from_suspendable(main)
        promise = promise_catch(promise, lambda e: traceback.print_exception(e))
        promise = promise_finally(promise, lambda: exit())
    try:
        while looper_needs_tick(looper):
            looper_tick(looper)
    except KeyboardInterrupt:
        exit()
