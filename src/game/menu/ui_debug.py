from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.battle import *
from game.monster import *
from game.inventory import *
from game.arena import *
from .ui_battle import _menu_show_battle
from .ui_arena import _menu_show_arena
from .ui_shop import _menu_show_shop
from .ui_laboratory import _menu_show_laboratory
import time

def _menu_show_debug_test(state, args):
    if state is SuspendableInitial:
        gameState, console = args
        print, input, meta = console
        meta(action="clear")
        print("=========== DEBUG TEST ===========")
        return 1, gameState, console
    if state == 1:
        gameState, console = args
        print, input, meta = console
        print("Pilih kumpulan debug test untuk mengetes fitur program")
        input("Coroutines Stats", selectable=True)
        input("Battle Test", selectable=True)
        input("Arena Test", selectable=True)
        input("Shop Test", selectable=True)
        input("Laboratory Test", selectable=True)
        selection = meta(action="select")
        return 2, gameState, console, selection
    if state == 2:
        gameState, console, selection = args
        if selection is None:
            return SuspendableReturn, None
        if selection == "Coroutines Stats":
            return SuspendableReturn, None, promise_from_suspendable(_menu_toggle_coroutines_stats, gameState)
        if selection == "Battle Test":
            return SuspendableReturn, None, promise_from_suspendable(_menu_show_debug_battle, gameState)
        if selection == "Arena Test":
            return SuspendableReturn, None, promise_from_suspendable(_menu_show_debug_arena, gameState)
        if selection == "Shop Test":
            return SuspendableReturn, None, promise_from_suspendable(_menu_show_debug_shop, gameState)
        if selection == "Laboratory Test":
            return SuspendableReturn, None, promise_from_suspendable(_menu_show_debug_laboratory, gameState)
    return SuspendableExhausted

def _menu_toggle_coroutines_stats(state, args):
    if state is SuspendableInitial:
        gameState, = args
        visual = gamestate_get_visual(gameState)
        if "__debug_coroutines_stats" in visual and visual["__debug_coroutines_stats"] is not None:
            return 2, gameState
        return 1, gameState
    if state == 1:
        gameState, = args
        visual = gamestate_get_visual(gameState)
        driver = visual_get_driver(visual)
        toplevel = visual_get_toplevel(visual)
        tempView = view_new(driver)
        statsView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_absolute(0),
            width=dim_from_absolute(25), height=dim_from_absolute(8),
            padding=(0, 0, 0, 0), parent=tempView)
        refController = dict(
            statsView=statsView,
            cancelled=False
        )
        visual["__debug_coroutines_stats"] = refController
        frame = 0
        lastTick = __now()
        lastFps = 0
        def update():
            nonlocal frame, lastTick, lastFps
            if refController["cancelled"]:
                return
            now = __now()
            deltaTime = now - lastTick
            lastTick = now
            if frame % 7 != 0: # prevent updated by next_tick
                lastFps = 1000 / deltaTime
            frame += 1
            if frame % 5 == 0:
                # Force on top
                view_remove_child(toplevel, statsView)
                view_add_child(toplevel, statsView)
            looper = looper_get_current()
            statsView["setContent"](array_join(array_map(string_split(string_trim(f"""
                FPS: {lastFps:.2f}
                Timers length: {len(looper["timers"])}
                Pollables length: {len(looper["pollables"])}
                Immediates length: {len(looper["immediates"])}
                Microtasks length: {len(looper["microtasks"])}
                Timer ID Counter: {looper["timerIdCounter"]}
            """), "\n"), lambda l, *_: string_trim(l)), "\n"))
            if frame % 7 == 0:
                next_tick(update)
                return
            set_timeout(update, 1)
        view_add_child(toplevel, statsView)
        next_tick(update)
        return SuspendableReturn, None
    if state == 2:
        gameState, = args
        visual = gamestate_get_visual(gameState)
        toplevel = visual_get_toplevel(visual)
        refController = visual["__debug_coroutines_stats"]
        visual["__debug_coroutines_stats"] = None
        refController["cancelled"] = True
        view_remove_child(toplevel, refController["statsView"])
        return SuspendableReturn, None
    return SuspendableExhausted

def _menu_show_debug_battle(state, args):
    if state is SuspendableInitial:
        gameState, = args
        # visual = gamestate_get_visual(gameState)
        # background = visual_show_splash(visual, "menu_background.gif.txt")
        # background["play"](60, True)
        background = None
        selfId = gamestate_get_user_id(gameState)
        opponentId = 0
        selfMonster = inventory_monster_new(gameState)
        selfMonster = inventory_monster_set(gameState, selfMonster.id, namedtuple_with(selfMonster, 
            ownerId=selfId, 
            referenceId=305, 
            name="Monster 1", 
            experiencePoints=0,
            healthPoints=230, 
            attackPower=70, 
            defensePower=110,
            activePotions=[]
        ))
        opponentMonster = inventory_monster_new(gameState)
        opponentMonster = inventory_monster_set(gameState, opponentMonster.id, namedtuple_with(opponentMonster, 
            ownerId=opponentId, 
            referenceId=181, 
            name="Monster 2", 
            experiencePoints=0,
            healthPoints=490, 
            attackPower=75, 
            defensePower=80,
            activePotions=[]
        ))
        battle = battle_new(gameState)
        battle = battle_set(gameState, battle.id, namedtuple_with(battle,
            turn=1,
            player1Id=selfId,
            player2Id=opponentId,
            monster1Id=selfMonster.id,
            monster2Id=opponentMonster.id,
            verdict=-1,
            handler="default_wild_monster$"
        ))
        battleView = promise_from_suspendable(_menu_show_battle, gameState, background, battle, 1, None)
        return SuspendableReturn, battleView
    return SuspendableExhausted

def _menu_show_debug_arena(state, args):
    if state is SuspendableInitial:
        gameState, = args
        # visual = gamestate_get_visual(gameState)
        # background = visual_show_splash(visual, "menu_background.gif.txt")
        # background["play"](60, True)
        background = None
        selfId = gamestate_get_user_id(gameState)
        arena = arena_new(gameState)
        arena = arena_set(gameState, arena.id, namedtuple_with(arena,
            playerId=selfId,
            battleIds=[None],
            handler="default$"
        ))
        arenaView = promise_from_suspendable(_menu_show_arena, gameState, background, arena, None)
        return SuspendableReturn, arenaView
    return SuspendableExhausted

def _menu_show_debug_shop(state, args):
    if state is SuspendableInitial:
        gameState, = args
        background = None
        shopView = promise_from_suspendable(_menu_show_shop, gameState, background, None)
        return SuspendableReturn, shopView
    return SuspendableExhausted

def _menu_show_debug_laboratory(state, args):
    if state is SuspendableInitial:
        gameState, = args
        background = None
        laboratoryView = promise_from_suspendable(_menu_show_laboratory, gameState, background, None)
        return SuspendableReturn, laboratoryView
    return SuspendableExhausted

def __now() -> float:
    return time.monotonic() * 1000
