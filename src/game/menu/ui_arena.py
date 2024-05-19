from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.arena import *
from game.battle import *
from .ui_battle import _menu_show_battle
from typing import NamedTuple, TypedDict, Callable, Any

__MenuArenaHandlerCache = TypedDict("MenuArenaHandlerCache",
    phase=str,
    args=tuple,
    promise=Promise
)
__MenuArenaCache = NamedTuple("MenuArena", [
    ("gameState", GameState), # expect not changed
    ("parent", View), # expect not changed
    ("abortSignal", AbortSignal), # expect not changed
    ("arena", ArenaSchemaType),
    ("arenaHandler", Callable), # expect not changed
    ("arenaHandlerCache", __MenuArenaHandlerCache), # expect not changed
    ("lastArenaBattleId", int),
    ("battleRef", TypedDict("BattleRef", abortController=AbortController, promise=Promise[Any])),
    ("mainView", View), # expect not changed
    ("mainConsole", ConsoleMock), # expect not changed
])

def _menu_show_arena(state, args):
    cache: __MenuArenaCache = None
    arena: ArenaSchemaType = None
    if state is SuspendableInitial:
        gameState, parent, arena, abortSignal = args
        arenaHandler = arena_ui_decode_handler(arena.handler)
        cache = __MenuArenaCache(
            gameState=gameState,
            parent=parent,
            abortSignal=abortSignal,
            arena=arena,
            arenaHandler=arenaHandler,
            arenaHandlerCache=dict(
                phase="arena:start",
                args=(),
                promise=None
            ),
            lastArenaBattleId=None,
            battleRef=dict(
                abortController=None, 
                promise=None
            ),
            mainView=None,
            mainConsole=None,
        )
        return "initInterface", cache
    if state == "initInterface":
        cache, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
    
        mainView = visual_show_simple_dialog(visual, "ARENA", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            parent=cache.parent)
        mainConsole = visual_with_mock(visual, mainView)

        cache = namedtuple_with(cache,
            mainView=mainView,
            mainConsole=mainConsole,
        )

        return "checkCache", cache
    if state == "checkCache":
        cache, *_ = args
        gameState = cache.gameState
        arena = arena_get(gameState, cache.arena.id)
        lastArenaBattleId = arena.battleIds[len(arena.battleIds) - 1]
        if lastArenaBattleId == cache.lastArenaBattleId:
            return "loop", cache
        cache = namedtuple_with(cache,
            arena=arena,
            lastArenaBattleId=lastArenaBattleId,
        )
        return "updateBattle", cache
    if state == "endBattle":
        cache, intent, *_ = args
        battleRef = cache.battleRef
        battleAbortController = battleRef["abortController"]
        battlePromise = battleRef["promise"]
        if battlePromise is None:
            return intent, cache
        battleRef["abortController"] = None
        battleRef["promise"] = None
        abortcontroller_abort(battleAbortController, "Aborted")
        return intent, cache, battlePromise
    if state == "updateBattle":
        cache, *_ = args
        gameState = cache.gameState
        arena = cache.arena
        battleRef = cache.battleRef
        if battleRef["promise"] is not None:
            return "endBattle", cache, "updateBattle"
        battleId = arena.battleIds[len(arena.battleIds) - 1]
        if battleId is None:
            if cache.parent is not None:
                view_add_child(cache.parent, cache.mainView)
            else:
                visual = gamestate_get_visual(gameState)
                visual_set_view(visual, cache.mainView)
            return "loop", cache
        if cache.parent is not None:
            view_remove_child(cache.parent, cache.mainView)
        else:
            visual = gamestate_get_visual(gameState)
            visual_set_view(visual, None)
        battle = battle_get(gameState, battleId)
        battleTurn = 1 if arena.playerId == battle.player1Id else 2
        battleAbortController = abortcontroller_new()
        battleAbortSignal = abortcontroller_get_signal(battleAbortController)
        battlePromise = promise_from_suspendable(_menu_show_battle, gameState, cache.parent, battle, battleTurn, battleAbortSignal)
        def onFinally():
            if battleRef["promise"] is not battlePromise:
                return
            battleRef["abortController"] = None
            battleRef["promise"] = None
        battlePromise = promise_finally(battlePromise, onFinally)
        battleRef["abortController"] = battleAbortController
        battleRef["promise"] = battlePromise
        return "loop", cache
    if state == "loop":
        cache, *_ = args
        gameState = cache.gameState
        arena = arena_get(gameState, cache.arena.id)
        lastArenaBattleId = arena.battleIds[len(arena.battleIds) - 1]
        if lastArenaBattleId != cache.lastArenaBattleId:
            return "checkCache", cache
        
        arenaHandler = cache.arenaHandler
        arenaHandlerCache = cache.arenaHandlerCache
        if arenaHandlerCache["phase"] == "arena:end":
            if cache.battleRef["promise"] is None:
                return "end", cache
            return "endBattle", cache, "end"
        arenaHandlerPromise = arenaHandlerCache["promise"]
        if arenaHandlerPromise is None:
            arenaHandlerPromise = promise_from_suspendable(
                arenaHandler, 
                arenaHandlerCache["phase"], 
                cache, *arenaHandlerCache["args"])
            def onResolved(result):
                # this arenaHandlerPromise actually captures the last assignment
                if arenaHandlerCache["promise"] is not arenaHandlerPromise:
                    return "loop"
                arenaHandlerCache["promise"] = None
                if type(result) is tuple:
                    arenaHandlerCache["phase"] = result[0]
                    arenaHandlerCache["args"] = (*array_slice(result, 1),)
                else:
                    arenaHandlerCache["phase"] = result
                    arenaHandlerCache["args"] = ()
                return "loop"
            arenaHandlerPromise = promise_then(arenaHandlerPromise, onResolved)
            arenaHandlerCache["promise"] = arenaHandlerPromise
        # We can't just return from here if abortSignal is aborted. We rely on the handler
        # to do so instead. Because it may handling saving to the database.
        return promise_race([promise_from_wait(30, "loop"), arenaHandlerPromise]), cache
    if state == "end":
        cache, *_ = args
        gameState = cache.gameState
        if cache.parent is not None:
            view_remove_child(cache.parent, cache.mainView)
        else:
            visual = gamestate_get_visual(gameState)
            visual_set_view(visual, None)
        return SuspendableReturn, None
    return SuspendableExhausted
