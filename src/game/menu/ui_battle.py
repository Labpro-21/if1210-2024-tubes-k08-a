from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.battle import *
from game.monster import *
from game.inventory import *
from .menu import _menu_show_loading_splash
from typing import NamedTuple, Optional, TypedDict, Callable

__MenuBattleHandlerCache = TypedDict("MenuBattleHandlerCache",
    phase=str,
    args=tuple,
    promise=Promise
)
__MenuBattleCache = NamedTuple("MenuBattle", [
    ("gameState", GameState), # expect not changed
    ("parent", View), # expect not changed
    ("turn", int), # expect not changed
    ("abortSignal", AbortSignal), # expect not changed
    ("battle", BattleSchemaType),
    ("battleHandler", Callable), # expect not changed
    ("battleHandlerCache", __MenuBattleHandlerCache), # expect not changed
    ("selfMonster", Optional[InventoryMonsterSchemaType]),
    ("opponentMonster", Optional[InventoryMonsterSchemaType]),
    ("selfMonsterSprite", Optional[str]),
    ("opponentMonsterSprite", Optional[str]),
    ("mainView", View), # expect not changed
    ("opponentStatView", View), # expect not changed
    ("selfStatView", View), # expect not changed
    ("battleView", View), # expect not changed
    ("opponentMonsterFrame", View), # expect not changed
    ("selfMonsterFrame", View), # expect not changed
    ("opponentMonsterAnimation", View),
    ("selfMonsterAnimation", View),
    ("dialogView", View), # expect not changed
    ("dialogConsole", ConsoleMock), # expect not changed
])

def _menu_show_battle(state, args):
    cache: __MenuBattleCache = None
    battle: BattleSchemaType = None
    if state is SuspendableInitial:
        gameState, parent, battle, turn, abortSignal = args
        battleHandler = battle_ui_decode_handler(battle.handler)
        cache = __MenuBattleCache(
            gameState=gameState,
            parent=parent,
            turn=turn,
            abortSignal=abortSignal,
            battle=battle,
            battleHandler=battleHandler,
            battleHandlerCache=dict(
                phase="battle:start",
                args=(),
                promise=None
            ),
            selfMonster=None,
            opponentMonster=None,
            selfMonsterSprite=None,
            opponentMonsterSprite=None,
            mainView=None,
            opponentStatView=None,
            selfStatView=None,
            battleView=None,
            opponentMonsterFrame=None,
            selfMonsterFrame=None,
            opponentMonsterAnimation=None,
            selfMonsterAnimation=None,
            dialogView=None,
            dialogConsole=None,
        )
        return "loadMonsterSprite", cache, "initInterface"
    if state == "loadMonsterSprite":
        cache, intent, *_ = args
        gameState = cache.gameState
        battle = battle_get(gameState, cache.battle.id)
        selfMonsterId = battle.monster1Id if cache.turn == 1 else battle.monster2Id if cache.turn == 2 else None
        opponentMonsterId = battle.monster2Id if cache.turn == 1 else battle.monster1Id if cache.turn == 2 else None
        selfMonster = inventory_monster_get(gameState, selfMonsterId) if selfMonsterId is not None else None
        opponentMonster = inventory_monster_get(gameState, opponentMonsterId) if opponentMonsterId is not None else None
        selfMonsterType = monster_get(gameState, selfMonster.referenceId) if selfMonster is not None else None
        opponentMonsterType = monster_get(gameState, opponentMonster.referenceId) if opponentMonster is not None else None
        selfMonsterSprite = selfMonsterType.spriteBack if selfMonsterType is not None else None
        opponentMonsterSprite = opponentMonsterType.spriteFront if opponentMonsterType is not None else None
        if selfMonsterSprite == cache.selfMonsterSprite and opponentMonsterSprite == cache.opponentMonsterSprite:
            visual = gamestate_get_visual(gameState)
            if cache.parent is not None:
                visual_set_view(visual, visual_get_root_view(visual, cache.parent))
            elif cache.mainView is not None:
                visual_set_view(visual, cache.mainView)
            return "reloadSprite", cache, intent
        promise = promise_from_suspendable(_menu_show_loading_splash, gameState, array_filter([
            (f"sprite {selfMonsterSprite}", selfMonsterSprite) if selfMonsterSprite is not None else None,
            (f"sprite {opponentMonsterSprite}", opponentMonsterSprite) if opponentMonsterSprite is not None else None,
        ], lambda s, *_: s is not None))
        selfMonsterAnimation = cache.selfMonsterAnimation
        if selfMonsterAnimation is not None and selfMonsterSprite != cache.selfMonsterSprite:
            selfMonsterAnimation["stop"]()
            view_remove_child(cache.selfMonsterFrame, selfMonsterAnimation)
            selfMonsterAnimation = None
        opponentMonsterAnimation = cache.opponentMonsterAnimation
        if opponentMonsterAnimation is not None and opponentMonsterSprite != cache.opponentMonsterSprite:
            opponentMonsterAnimation["stop"]()
            view_remove_child(cache.opponentMonsterFrame, opponentMonsterAnimation)
            opponentMonsterAnimation = None
        cache = namedtuple_with(cache,
            battle=battle,
            selfMonster=selfMonster,
            opponentMonster=opponentMonster,
            selfMonsterSprite=selfMonsterSprite,
            opponentMonsterSprite=opponentMonsterSprite,
            selfMonsterAnimation=selfMonsterAnimation,
            opponentMonsterAnimation=opponentMonsterAnimation,
        )
        return "loadMonsterSprite", cache, intent, promise
    if state == "reloadSprite":
        cache, intent, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
        selfMonsterSprite = cache.selfMonsterSprite
        opponentMonsterSprite = cache.opponentMonsterSprite
        selfMonsterAnimation = cache.selfMonsterAnimation
        opponentMonsterAnimation = cache.opponentMonsterAnimation
        if cache.selfMonsterFrame is not None and selfMonsterSprite is not None:
            if selfMonsterAnimation is None:
                selfMonsterAnimation = visual_show_splash(visual, selfMonsterSprite,
                    parent=cache.selfMonsterFrame)
                cache = namedtuple_with(cache, selfMonsterAnimation=selfMonsterAnimation)
            selfMonsterAnimation["play"](20, True)
        if cache.opponentMonsterFrame is not None and opponentMonsterSprite is not None:
            if opponentMonsterAnimation is None:
                opponentMonsterAnimation = visual_show_splash(visual, opponentMonsterSprite,
                    parent=cache.opponentMonsterFrame)
                cache = namedtuple_with(cache, opponentMonsterAnimation=opponentMonsterAnimation)
            opponentMonsterAnimation["play"](20, True)
        return intent, cache
    if state == "initInterface":
        cache, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
        
        mainView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_center(), y=pos_from_center(), 
            width=dim_from_factor(0.85), height=dim_from_factor(0.85),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=cache.parent)
        
        opponentStatView = visual_show_simple_dialog(visual, "STAT MUSUH", "",
            x=pos_from_absolute(0), y=pos_from_absolute(0),
            width=dim_from_factor(0.2), height=dim_from_factor(0.35),
            parent=mainView)

        selfStatView = visual_show_simple_dialog(visual, "STAT KAMU", "",
            x=pos_from_absolute(0), y=pos_from_factor(0.35),
            width=dim_from_factor(0.2), height=dim_sub(dim_from_factor(0.7), dim_from_factor(0.35)),
            parent=mainView)
        
        battleView = visual_show_simple_dialog(visual, "", "",
            x=pos_from_factor(0.2), y=pos_from_absolute(0),
            width=dim_from_fill(0), height=dim_from_factor(0.7),
            padding=(0, 0, 0, 0),
            parent=mainView)
        
        opponentMonsterFrame = visual_show_simple_dialog(visual, None, "",
            x=pos_from_end(None), y=pos_from_absolute(2),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=battleView)

        def opponentMonsterFrameMove():
            handle = None
            frame = 0
            totalFrame = 30
            def loop():
                nonlocal handle, frame
                frame += 1
                if frame < totalFrame:
                    middleFrame = frame if frame <= totalFrame / 2 else totalFrame - frame
                    view_set_x(opponentMonsterFrame, pos_sub(pos_from_end(None), pos_from_factor(middleFrame / totalFrame * 0.5)))
                    view_set_y(opponentMonsterFrame, pos_add(pos_from_factor(middleFrame / totalFrame * 0.5), pos_from_absolute(2)))
                    return
                view_set_x(opponentMonsterFrame, pos_from_end(None))
                view_set_y(opponentMonsterFrame, pos_from_absolute(2))
                clear_interval(handle)
                handle = None
            handle = set_interval(loop, 15)
        opponentMonsterFrame["move"] = opponentMonsterFrameMove

        selfMonsterFrame = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_sub(pos_from_end(None), pos_from_absolute(2)),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=battleView)
        
        def selfMonsterFrameMove():
            handle = None
            frame = 0
            totalFrame = 30
            def loop():
                nonlocal handle, frame
                frame += 1
                if frame < totalFrame:
                    middleFrame = frame if frame <= totalFrame / 2 else totalFrame - frame
                    view_set_x(selfMonsterFrame, pos_from_factor(middleFrame / totalFrame * 0.5))
                    view_set_y(selfMonsterFrame, pos_sub(pos_from_end(None), pos_from_factor(middleFrame / totalFrame * 0.5)))
                    return
                view_set_x(selfMonsterFrame, pos_from_absolute(0))
                view_set_y(selfMonsterFrame, pos_sub(pos_from_end(None), pos_from_absolute(2)))
                clear_interval(handle)
                handle = None
            handle = set_interval(loop, 15)
        selfMonsterFrame["move"] = selfMonsterFrameMove

        opponentMonsterAnimation = None
        if cache.opponentMonsterSprite is not None:
            opponentMonsterAnimation = visual_show_splash(visual, cache.opponentMonsterSprite,
                parent=opponentMonsterFrame)
            opponentMonsterAnimation["play"](20, True)

        selfMonsterAnimation = None
        if cache.selfMonsterSprite is not None:
            selfMonsterAnimation = visual_show_splash(visual, cache.selfMonsterSprite,
                parent=selfMonsterFrame)
            selfMonsterAnimation["play"](20, True)

        dialogView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_factor(0.7),
            width=dim_from_fill(0), height=dim_from_fill(0),
            parent=mainView)
        dialogConsole = visual_with_mock(visual, dialogView)

        cache = namedtuple_with(cache,
            mainView=mainView,
            opponentStatView=opponentStatView,
            selfStatView=selfStatView,
            battleView=battleView,
            opponentMonsterFrame=opponentMonsterFrame,
            selfMonsterFrame=selfMonsterFrame,
            opponentMonsterAnimation=opponentMonsterAnimation,
            selfMonsterAnimation=selfMonsterAnimation,
            dialogView=dialogView,
            dialogConsole=dialogConsole,
        )

        return "loop", cache
    if state == "loop":
        cache, *_ = args
        gameState = cache.gameState
        battle = battle_get(gameState, cache.battle.id)
        selfMonsterId = battle.monster1Id if cache.turn == 1 else battle.monster2Id if cache.turn == 2 else None
        opponentMonsterId = battle.monster2Id if cache.turn == 1 else battle.monster1Id if cache.turn == 2 else None
        lastSelfMonsterId = cache.selfMonster.id if cache.selfMonster is not None else None
        lastOpponentMonsterId = cache.opponentMonster.id if cache.opponentMonster is not None else None
        if selfMonsterId != lastSelfMonsterId or opponentMonsterId != lastOpponentMonsterId:
            return "loadMonsterSprite", cache, "loop"
        selfMonster = inventory_monster_get(gameState, selfMonsterId) if selfMonsterId is not None else None
        opponentMonster = inventory_monster_get(gameState, opponentMonsterId) if opponentMonsterId is not None else None
        def formatString(string):
            string = string_trim(string)
            string = array_join(array_map(string_split(string, "\n"), lambda l, *_: string_trim(l)), "\n")
            return string
        if selfMonster is not None:
            selfStatView = cache.selfStatView
            selfStatView["setContent"](formatString(f"""
                Nama: {selfMonster.name}
                HP: {selfMonster.healthPoints:.1f}
                Attack: {selfMonster.attackPower}
                Defense: {selfMonster.defensePower}
                Potions: {0}
            """))
        if opponentMonster is not None:
            opponentStatView = cache.opponentStatView
            opponentStatView["setContent"](formatString(f"""
                Nama: {opponentMonster.name}
                HP: {opponentMonster.healthPoints:.1f}
                Attack: {opponentMonster.attackPower}
                Defense: {opponentMonster.defensePower}
                Potions: {0}
            """))
        cache = namedtuple_with(cache,
            battle=battle,
            selfMonster=selfMonster,
            opponentMonster=opponentMonster
        )

        battleHandler = cache.battleHandler
        battleHandlerCache = cache.battleHandlerCache
        if battleHandlerCache["phase"] == "battle:end":
            if cache.parent is not None:
                view_remove_child(cache.parent, cache.mainView)
            else:
                visual = gamestate_get_visual(gameState)
                visual_set_view(visual, None)
            return SuspendableReturn, None
        battleHandlerPromise = battleHandlerCache["promise"]
        if battleHandlerPromise is None:
            battleHandlerPromise = promise_from_suspendable(
                battleHandler, 
                battleHandlerCache["phase"], 
                cache, *battleHandlerCache["args"])
            def onResolved(result):
                # this battleHandlerPromise actually captures the last assignment
                if battleHandlerCache["promise"] is not battleHandlerPromise:
                    return "loop"
                battleHandlerCache["promise"] = None
                if type(result) is tuple:
                    battleHandlerCache["phase"] = result[0]
                    battleHandlerCache["args"] = (*array_slice(result, 1),)
                else:
                    battleHandlerCache["phase"] = result
                    battleHandlerCache["args"] = ()
                return "loop"
            battleHandlerPromise = promise_then(battleHandlerPromise, onResolved)
            battleHandlerCache["promise"] = battleHandlerPromise
        # We can't just return from here if abortSignal is aborted. We rely on the handler
        # to do so instead. Because it may handling saving to the database.
        return promise_race([promise_from_wait(30, "loop"), battleHandlerPromise]), cache
    return SuspendableExhausted
