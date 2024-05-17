from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.database import *
from game.menu import *
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
        return "menu", gameState, visual
    if state == "initializing":
        gameState, visual, *_ = args
        promise = promise_from_suspendable(menu_show_loading_initial, gameState, visual)
        return "loading", gameState, visual, promise
    if state == "loading":
        gameState, visual, *_ = args
        promise = promise_from_suspendable(menu_show_loading_splash, gameState, visual, [("menu splash", "menu_background.gif.txt")])
        return "menu", gameState, visual, promise
    if state == "menu":
        gameState, visual, *_ = args
        menuBackground = None
        # menuBackground = visual_show_splash(visual, "menu_background.gif.txt")
        # menuBackground["play"](60)
        dialogView = visual_show_simple_dialog(visual, parent=menuBackground)
        console = visual_with_mock(visual, dialogView, keySpeed=120, hasTitle=True)
        menu = promise_from_suspendable(menu_show_menu, gameState, console)
        return 4, gameState, visual, menu
    if state == 4:
        gameState, visual, *_ = args
        return -2
    if state == -2:
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
