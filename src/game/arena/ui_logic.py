from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from utils.math import *
from game.state import *
from game.user import *
from game.inventory import *
from game.monster import *
from game.arena import *
from game.battle import *
from typing import NamedTuple, TypedDict, Callable, Any

def _arena_ui_decode_handler(handler: str) -> Suspendable:
    if string_starts_with(handler, "default$"):
        return _arena_ui_handler_default
    return None

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

def _arena_ui_handler_default(state, args):
    cache: __MenuArenaCache = None
    arena: ArenaSchemaType = None
    if state is SuspendableInitial:
        phase, cache, *rest = args
        # If we have abortSignal directly in args, it means some user input has been cancelled.
        # Note that we use flags "doNotRaiseSignal" in console meta.
        if cache.abortSignal is not None and array_some(rest, lambda r, *_: r is cache.abortSignal):
            return "arena:forcefully_aborted", cache
        return phase, cache, *rest
    if state == "arena:start":
        cache, *_ = args
        print, input, meta = cache.mainConsole
        meta("keySpeed", 120)
        meta("selectableAllowEscape", False)
        meta("doNotRaiseSignal", True)
        lastBattleId = cache.arena.battleIds[len(cache.arena.battleIds) - 1]
        if lastBattleId is not None:
            return "arena:start_already_in_battle", cache
        return "arena:start_menu", cache
    if state == "arena:start_already_in_battle":
        cache, *_ = args
        return "arena:wait_battle", cache
    if state == "arena:start_menu":
        cache, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.mainConsole
        meta(action="clear")
        trainers = user_get_all_npcs(gameState)
        trainersMonsters = array_map(trainers, lambda t, *_: (t, array_filter(inventory_monster_get_user_monsters(gameState, t.id), lambda m, *_: m.healthPoints > 0)))
        trainersMonsters = array_filter(trainersMonsters, lambda m, *_: len(m[1]) > 0)
        if len(trainersMonsters) == 0:
            print("Yahhh kayaknya gaada trainer lagi buat kamu:( tunggu kapan-kapan yak!")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "arena:end", selection
        trainersMonsters = array_map(rand_uniq_int_array(0, len(trainersMonsters), min(5, len(trainersMonsters))), lambda i, *_: trainersMonsters[i])
        for trainersMonster in trainersMonsters:
            trainer, monsters = trainersMonster
            description = ""
            for monster in monsters:
                monsterType = monster_get(gameState, monster.referenceId)
                description += f"F: {monsterType.family}, "
                description += f"L: {monsterType.level}, "
                description += f"HP: {monster.healthPoints:.1f}, " # TODO: These properties do not include potion effects
                description += f"ATK: {monster.attackPower:.1f}, "
                description += f"DEF: {monster.defensePower:.1f} | "
            description = string_slice(description, 0, -len(" | "))
            input(f"{trainer.username}", description, id=trainer.id, selectable=True)
        print("Selamat datang di arena! Pilih trainer di bawah untuk mulai bertarung!")
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "arena:start_menu_choose", selection
    if state == "arena:start_menu_choose":
        cache, selection, *_ = args
        gameState = cache.gameState
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "arena:forcefully_aborted", cache
        trainerId = selection
        trainerMonsters = array_filter(inventory_monster_get_user_monsters(gameState, trainerId), lambda m, *_: m.healthPoints > 0)
        initialTrainerMonster = trainerMonsters[int(gamestate_rand(gameState) * len(trainerMonsters))]
        return "arena:next_stage_new_battle", cache, trainerId, initialTrainerMonster
    if state == "arena:wait_battle":
        cache, *_ = args
        return SuspendableReturn, "arena:battle_finished", cache.battleRef["promise"]
    if state == "arena:battle_finished":
        cache, *_ = args
        gameState = cache.gameState
        arena = cache.arena
        arena = arena_set(gameState, arena.id, namedtuple_with(arena, battleIds=[*arena.battleIds, None]))
        battle = battle_get(gameState, arena.battleIds[len(arena.battleIds) - 2])
        playerTurn = 1 if battle.player1Id == arena.playerId else 2
        trainerTurn = 2 if battle.player1Id == arena.playerId else 1
        # Bailout to update arena
        if battle_verdict_is_player_escaped(battle.verdict) == playerTurn:
            return SuspendableReturn, "arena:player_escaped"
        if battle_verdict_is_player_escaped(battle.verdict) == trainerTurn:
            return SuspendableReturn, "arena:trainer_escaped"
        if battle_verdict_is_player_won(battle.verdict) == trainerTurn:
            return SuspendableReturn, "arena:end_lost"
        if len(arena.battleIds) < 6: # This includes the None mark
            return SuspendableReturn, "arena:next_stage"
        else:
            return SuspendableReturn, "arena:end_won"
    def printStats(cache):
        print("Ini stats")
    if state == "arena:end_won":
        cache, *_ = args
        print, input, meta = cache.mainConsole
        meta(action="clear")
        print("Yey kamu menang!")
        printStats(cache)
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "arena:end", selection
    if state == "arena:next_stage":
        cache, *_ = args
        print, input, meta = cache.mainConsole
        meta(action="clear")
        print("Yey kamu menang!")
        printStats(cache)
        input("Next stage", selectable=True)
        input("Selesai", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "arena:next_stage_choose", cache, selection, oldArenaId
    if state == "arena:next_stage_choose":
        cache, selection, *_ = args
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "arena:forcefully_aborted", cache
        if selection == "Next stage":
            return "arena:next_stage_check_trainer", cache, oldArenaId
        if selection == "Selesai":
            return SuspendableReturn, "arena:end"
    if state == "arena:next_stage_check_trainer":
        cache, *_ = args
        print, input, meta = cache.mainConsole
        meta(action="clear")
        gameState = cache.gameState
        arena = cache.arena
        lastBattleId = arena.battleIds[len(arena.battleIds) - 2] # Index before the None mark
        lastBattle = battle_get(gameState, lastBattleId)
        lastTrainerId = lastBattle.player2Id if arena.playerId == lastBattle.player1Id else lastBattle.player1Id
        lastTrainerMonsters = inventory_monster_get_user_monsters(gameState, lastTrainerId)
        lastTrainerMonsters = array_filter(lastTrainerMonsters, lambda m, *_: m.healthPoints > 0)
        if len(lastTrainerMonsters) > 0:
            nextTrainerMonster = lastTrainerMonsters[int(gamestate_rand(gameState) * len(lastTrainerMonsters))]
            return "arena:next_stage_new_battle", cache, lastTrainerId, nextTrainerMonster.id
        trainers = user_get_all_npcs(gameState)
        trainersMonsters = array_map(trainers, lambda t, *_: (t, array_filter(inventory_monster_get_user_monsters(gameState, t.id), lambda m, *_: m.healthPoints > 0)))
        trainersMonsters = array_filter(trainersMonsters, lambda m, *_: len(m[1]) > 0)
        if len(trainersMonsters) == 0:
            print("Yahhh kayaknya gaada trainer lagi buat kamu:( tunggu kapan-kapan yak!")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "arena:end", selection
        trainersMonsters = array_map(rand_uniq_int_array(0, len(trainersMonsters), min(5, len(trainersMonsters))), lambda i, *_: trainersMonsters[i])
        for trainersMonster in trainersMonsters:
            trainer, monsters = trainersMonster
            description = ""
            for monster in monsters:
                monsterType = monster_get(gameState, monster.referenceId)
                description += f"F: {monsterType.family}, "
                description += f"L: {monsterType.level}, "
                description += f"HP: {monster.healthPoints:.1f}, " # TODO: These properties do not include potion effects
                description += f"ATK: {monster.attackPower:.1f}, "
                description += f"DEF: {monster.defensePower:.1f} | "
            description = string_slice(description, 0, -len(" | "))
            input(f"{trainer.username}", description, id=trainer.id, selectable=True)
        meta("selectableAllowEscape", True)
        print("Waduh! trainer yang tadi baru aja kamu kalahin! dia ga ada monster lagi buat bertarung. Pilih trainer lainnya yok!")
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "arena:next_stage_new_trainer", selection
    if state == "arena:next_stage_new_trainer":
        gameState = cache.gameState
        cache, selection, *_ = args
        print, input, meta = cache.mainConsole
        meta("selectableAllowEscape", False)
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "arena:forcefully_aborted", cache
        if selection is None:
            return "arena:next_stage", cache
        trainerId = selection
        trainerMonsters = array_filter(inventory_monster_get_user_monsters(gameState, trainerId), lambda m, *_: m.healthPoints > 0)
        nextTrainerMonster = trainerMonsters[int(gamestate_rand(gameState) * len(trainerMonsters))]
        return "arena:next_stage_new_battle", cache, trainerId, nextTrainerMonster.id
    if state == "arena:next_stage_new_battle":
        cache, trainerId, monsterId, *_ = args
        gameState = cache.gameState
        arena = cache.arena
        battle = battle_new(gameState)
        battle = battle_set(gameState, battle.id, namedtuple_with(battle,
            turn=1,
            player1Id=arena.playerId,
            player2Id=trainerId,
            monster1Id=None,
            monster2Id=monsterId.id,
            verdict=-1,
            handler="default_arena_trainer$"
        ))
        newBattleIds = array_slice(arena.battleIds, 0, -1)
        array_push(newBattleIds, battle.id)
        arena = arena_set(gameState, arena.id, namedtuple_with(arena, battleIds=newBattleIds))
        # Bailout to update arena
        return SuspendableReturn, "arena:wait_battle"
    if state == "arena:end_lost":
        cache, *_ = args
        print, input, meta = cache.mainConsole
        meta(action="clear")
        print("Looserrr!")
        printStats(cache)
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "arena:end", selection
    if state == "arena:player_escaped":
        cache, *_ = args
        print, input, meta = cache.mainConsole
        meta(action="clear")
        print("Kamunya kok lari!")
        printStats(cache)
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "arena:end", selection
    if state == "arena:trainer_escaped":
        cache, *_ = args
        arena = cache.arena
        print, input, meta = cache.mainConsole
        meta(action="clear")
        print("WKKWKWK trainernya lari anyinggg!")
        printStats(cache)
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        if len(arena.battleIds) < 6: # This includes the None mark
            return SuspendableReturn, "arena:next_stage", selection
        else:
            return SuspendableReturn, "arena:end_won", selection
    if state == "arena:forcefully_aborted":
        # Huh, maybe do some cleanup here. Perhaps checking current state and make
        # it recoverable/resumable in the future. Though, this is probably safe
        # because we save the state just before the selection/promise.
        return SuspendableReturn, "arena:end"
    return SuspendableExhausted
