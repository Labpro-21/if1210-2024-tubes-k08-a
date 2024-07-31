from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.database import *
from game.menu import *
from game.battle import *
from os import path
from sys import argv
import traceback

def main(state, args):
    if state is SuspendableInitial:
        currentDirectory = path.dirname(__file__)
        saveName = string_trim(array_join(array_slice(argv, 1), " "))
        if string_starts_with(saveName, "\"") and string_ends_with(saveName, "\""):
            saveName = string_slice(saveName, 1, -1)
        saveName = string_trim(saveName)
        if saveName == "":
            saveName = "default-save"
        savesDirectory = path.join(currentDirectory, "./data/saves/", saveName)
        assetsDirectory = path.join(currentDirectory, "./data/assets/")
        gameState = gamestate_new(savesDirectory)
        visual = gamestate_get_visual(gameState)
        visual_set_directory(visual, assetsDirectory)
        def tick():
            gamestate_tick(gameState)
            visual_tick(visual)
            visual_draw(visual)
        set_interval(tick, 15)
        return "initializing", gameState
    if state == "initializing":
        gameState, *_ = args
        savesDirectory = gamestate_get_directory(gameState)
        if not path.exists(savesDirectory) or not path.isdir(savesDirectory):
            visual = gamestate_get_visual(gameState)
            dialogView = visual_show_simple_dialog(visual, "ERROR LOADING SAVE", "")
            print, input, meta = visual_with_mock(visual, dialogView, keySpeed=120)
            print(f"Tidak dapat loading file \"{savesDirectory}\" karena folder tidak ada.")
            input("Keluar", selectable=True)
            selection = meta(action="select")
            return -1, selection
        gamestate_load(gameState)
        # gamestate_set_user_id(gameState, 1)
        promise = promise_from_suspendable(menu_show_loading_initial, gameState)
        return "loading", gameState, promise
    if state == "loading":
        gameState, *_ = args
        promise = promise_from_suspendable(menu_show_loading_splash, gameState, [("menu splash", "menu_background.gif.txt")])
        return "menuInit", gameState, promise
    if state == "menuInit":
        gameState, *_ = args
        visual = gamestate_get_visual(gameState)
        # menuBackground = None
        menuBackground = visual_show_splash(visual, "menu_background.gif.txt")
        menuBackground["play"](60, True)
        menuView = visual_show_simple_dialog(visual, parent=menuBackground)
        console = visual_with_mock(visual, menuView, keySpeed=120, hasTitle=True)
        return "menu", gameState, console
        # return "menuOption", gameState, console, "admin:debug_test"
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
        if menu == "agent:battle_wild_monster":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_battle, gameState)
        if menu == "agent:battle_arena":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_arena, gameState)
        if menu == "agent:shop":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_shop, gameState)
        if menu == "agent:laboratory":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_laboratory, gameState)
        if menu == "agent:inventory":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_inventory, gameState)
        if menu == "admin:shop_management":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_shop_management, gameState)
        if menu == "admin:monster_management":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_monster_management, gameState)
        if menu == "admin:debug_test":
            return "menu", gameState, console, promise_from_suspendable(menu_show_debug_test, gameState, console)
        if menu == "agent:save" or menu == "admin:save":
            savesDirectory = path.join(path.dirname(__file__), "./data/saves/")
            return "menu", gameState, console, promise_from_suspendable(menu_show_save, gameState, console, savesDirectory)
        if menu == "agent:logout" or menu == "admin:logout":
            return "menu", gameState, console, promise_from_suspendable(menu_show_logout, gameState, console)
        if menu == "guest:exit" or menu == "agent:exit" or menu == "admin:exit":
            return "checkExit", gameState, console, promise_from_suspendable(menu_show_exit, gameState, console)
    if state == "checkExit":
        gameState, console, confirmExit = args
        if type(confirmExit) is bool and confirmExit == False:
            return "menu", gameState, console
        if confirmExit == 0:
            savesDirectory = path.join(path.dirname(__file__), "./data/saves/")
            promise = promise_from_suspendable(menu_show_save, gameState, console, savesDirectory)
            return "checkExitSave", gameState, console, promise
        return -1
    if state == "checkExitSave":
        gameState, console, result = args
        if result:
            return -1
        return "menuOption", gameState, console, "guest:exit"
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
    finally:
        driverstd_reset_console()
