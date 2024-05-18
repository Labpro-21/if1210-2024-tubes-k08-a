from utils.primordials import *
from utils.coroutines import *
from game.state import *
from game.battle import *
from game.monster import *
from game.inventory import *
from .ui_battle import _menu_show_battle

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
        input("Battle Test", selectable=True)
        selection = meta(action="select")
        return 2, gameState, console, selection
    if state == 2:
        gameState, console, selection = args
        if selection is None:
            return SuspendableReturn, None
        if selection == "Battle Test":
            return SuspendableReturn, None, promise_from_suspendable(_menu_show_debug_battle, gameState)
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
            verdict=-1
        ))
        battleView = promise_from_suspendable(_menu_show_battle, gameState, background, battle, battle_ui_handler_wild_monster)
        return SuspendableReturn, battleView
    return SuspendableExhausted
