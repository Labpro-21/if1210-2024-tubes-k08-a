from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.battle import *
from game.inventory import *
from game.potion import *
from game.monster import *
from game.arena import *
from game.user import *
from .battle import _battle_end_player_escaped, _battle_end_player_draw, _battle_end_player_won, _battle_action_attack, _battle_set
from typing import NamedTuple, Optional, TypedDict, Callable

def _battle_ui_decode_handler(handler: str) -> Suspendable:
    if string_starts_with(handler, "default_wild_monster$"):
        return _battle_ui_handler_wild_monster
    if string_starts_with(handler, "default_arena_trainer$"):
        return _battle_ui_handler_wild_monster
    return None

__MenuBattleHandlerCache = TypedDict("MenuBattleHandlerCache",
    phase=str,
    args=tuple,
    promise=Promise
)
__MenuBattleCache = NamedTuple("MenuBattleCache", [
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

def _battle_ui_handler_wild_monster(state, args):
    cache: __MenuBattleCache = None
    battle: BattleSchemaType = None
    # THIS IS A HACK TO CONFORM THE RULES. Get arena instance if the battle is part of arena.
    def getArenaFromBattle(cache: __MenuBattleCache) -> ArenaSchemaType:
        gameState = cache.gameState
        battleId = cache.battle.id
        __battleArenaId = f"__battle-{battleId}-arena-id"
        if __battleArenaId not in gameState:
            return None
        return gameState[__battleArenaId]
    if state == SuspendableInitial:
        phase, cache, *rest = args
        # If we have abortSignal directly in args, it means some user input has been cancelled.
        # Note that we use flags "doNotRaiseSignal" in console meta.
        if cache.abortSignal is not None and array_some(rest, lambda r, *_: r is cache.abortSignal):
            return "battle:forcefully_aborted", cache
        return phase, cache, *rest
    if state == "battle:start":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        meta("keySpeed", 120)
        meta("selectableAllowEscape", False)
        meta("doNotRaiseSignal", True)
        battle = cache.battle
        if battle_verdict_is_finished(battle.verdict):
            return "battle:verdict_finished", cache
        if battle.turn == 0:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, turn=cache.turn)) # switch turn
            # Bailout to update battle
            return SuspendableReturn, "battle:start_menu"
        return "battle:start_menu", cache
    if state == "battle:verdict_finished":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        print("Kayaknya battle ini sudah selesai deh?")
        input("Lanjut", selectable=True)
        return SuspendableReturn, "battle:end", selection
    if state == "battle:start_menu":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        # THIS IS A HACK TO CONFORM THE RULES. Custom dialog for arena.
        arena = getArenaFromBattle(cache)
        if arena is not None:
            print("Lawanmu telah mengeluarkan monsternya! Apa yang akan kamu lakukan?")
        else:
            print("Boom! Kamu bertemu dengan monster liar! Apa yang akan kamu lakukan?")
        input("Attack", selectable=True)
        if arena is None:
            input("Capture", selectable=True)
        input("Kabur", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:start_menu#respond", selection
    if state == "battle:start_menu#respond":
        cache, selection, *_ = args
        battle = cache.battle
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "battle:forcefully_aborted"
        if selection == "Attack" and ((cache.turn == 1 and battle.monster1Id is None) or (cache.turn == 2 and battle.monster2Id is None)):
            return "battle:main#choose_monster", cache, "battle:start_menu#choose_monster_selection"
        if selection == "Kabur" and ((cache.turn == 1 and battle.monster1Id is None) or (cache.turn == 2 and battle.monster2Id is None)):
            return "battle:action#escape", cache, True
        return "battle:main#respond", cache, selection
    if state == "battle:start_menu#choose_monster_selection":
        cache, choose, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.dialogConsole
        if choose == "Cancelled":
            return "battle:start_menu", cache
        if choose == "Nothing":
            battle = cache.battle
            battle = _battle_end_player_escaped(gameState, battle, cache.turn)
            meta(action="clear")
            print("Kayaknya kamu ga ada monster buat dibuat battle deh.")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            # Bailout to update battle
            return SuspendableReturn, "battle:end", selection
        battle = cache.battle
        if cache.turn == 1:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster1Id=choose))
        if cache.turn == 2:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster2Id=choose))
        # Bailout to update battle
        return SuspendableReturn, "battle:start_menu#choose_monster_selection?callout"
    if state == "battle:start_menu#choose_monster_selection?callout":
        # Need intermediate state to show loading
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        print("Aku memanggil monster baru!")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:action#attack", selection
    if state == "battle:main":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        battle = cache.battle
        selfMonster = cache.selfMonster
        opponentMonster = cache.opponentMonster
        if selfMonster is None: # Can the user's monster be None other than initial battle?
            # If the user's monster is dead, then we open the monster selection overlay, but all in all it never make it here.
            return "battle:start_menu", cache
        if selfMonster.healthPoints <= 0 or opponentMonster.healthPoints <= 0:
            return "battle:main#monster_defeated", cache
        if battle.turn != cache.turn:
            return "battle:main#opponent_turn", cache
        meta(action="clear")
        print("Ambil tindakan selanjutnya...")
        input("Attack", selectable=True)
        if getArenaFromBattle(cache) is None:
            input("Capture", selectable=True)
        input("Tindakan lainnya...", id="page2", selectable=True)
        input("Kabur", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:main#respond", selection
    if state == "battle:main#page2":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        print("Ambil tindakan selanjutnya...")
        input("Gunakan Potion", selectable=True)
        input("Ganti Monster", selectable=True)
        input("Tindakan lainnya...", id="page1", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:main#respond", selection
    if state == "battle:main#respond":
        cache, selection, *_ = args
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "battle:forcefully_aborted"
        if selection == "page1":
            return "battle:main", cache
        if selection == "page2":
            return "battle:main#page2", cache
        if selection == "Attack":
            return "battle:action#attack", cache
        if selection == "Capture":
            return "battle:action#capture", cache
        if selection == "Gunakan Potion":
            return "battle:action#use_potion", cache
        if selection == "Ganti Monster":
            return "battle:action#change_monster", cache
        if selection == "Kabur":
            return "battle:action#escape", cache, False
    if state == "battle:main#monster_defeated":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        gameState = cache.gameState
        battle = cache.battle
        selfMonster = cache.selfMonster
        opponentMonster = cache.opponentMonster
        meta(action="clear")
        if selfMonster.healthPoints <= 0 and opponentMonster.healthPoints <= 0:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster1Id=None, monster2Id=None))
            battle = _battle_end_player_draw(gameState, battle)
            print("Yah monstermu dan monster opponent mati...")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            # Bailout to update battle
            return SuspendableReturn, "battle:end", selection
        if opponentMonster.healthPoints <= 0:
            if cache.turn == 1:
                battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster2Id=None))
            if cache.turn == 2:
                battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster1Id=None))
            battle = _battle_end_player_won(gameState, battle, cache.turn)
            print("YEYYY kamu menang! Monster opponent telah mati.")
            # THIS IS A HACK TO CONFORM THE RULES. User received some amount of money after wild monster battle.
            if getArenaFromBattle(cache) is None:
                userId = battle.player1Id if cache.turn == 1 else battle.player2Id if cache.turn == 2 else None
                opponentMonsterLevel = monster_get(gameState, opponentMonster.referenceId)
                receivedMoney = 100 * opponentMonsterLevel.level + int(gamestate_rand(gameState) * 70 * opponentMonsterLevel.level)
                user = user_get(gameState, userId)
                user = user_set(gameState, user.id, namedtuple_with(user, money=user.money + receivedMoney))
                print(f"Kamu mendapatkan uang sebanyak {receivedMoney} dari battle ini!")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            # Bailout to update battle
            return SuspendableReturn, "battle:end", selection
        if selfMonster.healthPoints <= 0:
            if cache.turn == 1:
                battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster1Id=None))
            if cache.turn == 2:
                battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster2Id=None))
            return SuspendableReturn, "battle:main#monster_defeated_choose_monster_dialog"
    if state == "battle:main#monster_defeated_choose_monster_dialog":
        cache, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.dialogConsole
        battle = cache.battle
        selfMonsterId = battle.monster1Id if cache.turn == 1 else battle.monster2Id if cache.turn == 2 else None
        userId = battle.player1Id if cache.turn == 1 else battle.player2Id if cache.turn == 2 else None
        userMonsters = inventory_monster_get_user_monsters(gameState, userId)
        userMonsters = array_filter(userMonsters, lambda m, *_: m.healthPoints > 0 and m.id != selfMonsterId)
        meta(action="clear")
        if len(userMonsters) > 0:
            print("Yah monstermu mati...")
            input("Ganti Monster", selectable=True)
            input("Kabur", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main#monster_defeated_choose_monster_dialog_choose", selection
        battle = _battle_end_player_won(gameState, battle, 2 if cache.turn == 1 else 1)
        print("Lol monstermu udah mati semua wkkwkwkwkw.")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:end", selection
    if state == "battle:main#monster_defeated_choose_monster_dialog_choose":
        cache, selection, *_ = args
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "battle:forcefully_aborted"
        if selection == "Ganti Monster":
            return "battle:main#choose_monster", cache, "battle:main#monster_defeated_choose_monster"
        if selection == "Kabur":
            return "battle:action#escape", cache, True
    if state == "battle:main#monster_defeated_choose_monster":
        cache, choose, *_ = args
        gameState = cache.gameState
        battle = cache.battle
        print, input, meta = cache.dialogConsole
        if choose == "Cancelled":
            return "battle:main#monster_defeated_choose_monster_dialog", cache
        if choose == "Nothing":
            battle = _battle_end_player_won(gameState, battle, 2 if cache.turn == 1 else 1)
            meta(action="clear")
            print("Lol monstermu udah mati semua wkkwkwkwkw.")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:end", selection
        if cache.turn == 1:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster1Id=choose))
        if cache.turn == 2:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster2Id=choose))
        # Bailout to update battle
        return SuspendableReturn, "battle:main#monster_defeated_choose_monster?callout"
    if state == "battle:main#monster_defeated_choose_monster?callout":
        # Need intermediate state to show loading
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        print("Aku memanggil monster baru!")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:main", selection
    if state == "battle:main#opponent_turn":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        gameState = cache.gameState
        battle = cache.battle
        opponentMonsterAttack, *_ = _battle_action_attack(gameState, battle)
        battle = _battle_set(gameState, battle.id, namedtuple_with(battle, turn=cache.turn)) # switch turn
        cache.opponentMonsterFrame["move"]()
        meta(action="clear")
        print(f"Kamu menerima serangan dan musuh mengurangi HP-mu sebesar {opponentMonsterAttack:.2f}")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        # Bailout to update battle
        return SuspendableReturn, "battle:main", selection
    if state == "battle:main#choose_monster":
        cache, intent, *_ = args
        gameState = cache.gameState
        battle = cache.battle
        selfMonsterId = battle.monster1Id if cache.turn == 1 else battle.monster2Id if cache.turn == 2 else None
        userId = battle.player1Id if cache.turn == 1 else battle.player2Id if cache.turn == 2 else None
        userMonsters = inventory_monster_get_user_monsters(gameState, userId)
        userMonsters = array_filter(userMonsters, lambda m, *_: m.healthPoints > 0 and m.id != selfMonsterId)
        if len(userMonsters) == 0:
            return intent, cache, "Nothing"
        visual = gamestate_get_visual(gameState)
        modalView = visual_show_simple_dialog(visual, "Pilih Monster", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            parent=cache.mainView)
        modalConsole = visual_with_mock(visual, modalView)
        print, input, meta = modalConsole
        meta(action="clear")
        print("Pilih monstermu yang ingin digunakan")
        for userMonster in userMonsters:
            monsterType = monster_get(gameState, userMonster.referenceId)
            description = txtkv("F: ", monsterType.family) + " "
            description += txtkv("L: ", monsterType.level) + " "
            description += txtkv("HP: ", f"{userMonster.healthPoints:.1f}") + " " # TODO: These properties do not include potion effects
            description += txtkv("ATK: ", f"{userMonster.attackPower:.1f}") + " "
            description += txtkv("DEF: ", f"{userMonster.defensePower:.1f}") + ""
            input(f"{userMonster.name}", description, id=userMonster.id, selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        # Purposefuly undefined behaviour: We expect the database to not change between selection.
        return "battle:main#choose_monster_selection", cache, intent, selection, modalView
    if state == "battle:main#choose_monster_selection":
        cache, intent, selection, modalView, *_ = args
        view_remove_child(cache.mainView, modalView)
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "battle:forcefully_aborted"
        if selection == None:
            return intent, cache, "Cancelled"
        return intent, cache, selection
    if state == "battle:action#attack":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        gameState = cache.gameState
        battle = cache.battle
        selfMonsterAttack, *_ = _battle_action_attack(gameState, battle)
        battle = _battle_set(gameState, battle.id, namedtuple_with(battle, turn=2 if cache.turn == 1 else 1)) # switch turn
        cache.selfMonsterFrame["move"]()
        meta(action="clear")
        print(f"Kamu melakukan serangan dan mengurangi HP opponent sebesar {selfMonsterAttack:.2f}")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        # Bailout to update battle
        return SuspendableReturn, "battle:main", selection
    if state == "battle:action#capture":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        gameState = cache.gameState
        battle = cache.battle
        meta(action="clear")
        userId = battle.player1Id if cache.turn == 1 else battle.player2Id if cache.turn == 2 else None
        userMonsterBall = inventory_item_get_user_items(gameState, userId)
        userMonsterBall = array_find(userMonsterBall, lambda i, *_: i.referenceId == 3 and i.quantity > 0) # ID 3 is for monster ball
        if userMonsterBall is None:
            print("Kamu ga ada monster ball yang bisa dipake!")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main", selection
        userMonsterBall = inventory_item_set(gameState, userMonsterBall.id, namedtuple_with(userMonsterBall,
            quantity=userMonsterBall.quantity - 1
        ))
        opponentMonster = cache.opponentMonster
        opponentMonsterType = monster_get(gameState, opponentMonster.referenceId)
        randomNumber = gamestate_rand(gameState)
        captureSuccess = False
        if opponentMonsterType.level == 1 and randomNumber < 0.75:
            captureSuccess = True
        if opponentMonsterType.level == 2 and randomNumber < 0.50:
            captureSuccess = True
        if opponentMonsterType.level == 3 and randomNumber < 0.25:
            captureSuccess = True
        if opponentMonsterType.level == 4 and randomNumber < 0.10:
            captureSuccess = True
        if opponentMonsterType.level == 5 and randomNumber < 0.05:
            captureSuccess = True
        if not captureSuccess:
            print("BAM! Kamu mengeluarkan monster ball!")
            print("Tapi kayaknya monsternya ga ketangkep deh:(")
            print(f"Sisa monster ball: {txtqty(userMonsterBall.quantity)}")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main", selection
        if cache.turn == 1:
            battle = battle_set(gameState, battle.id, namedtuple_with(battle, monster2Id=None))
        if cache.turn == 2:
            battle = battle_set(gameState, battle.id, namedtuple_with(battle, monster1Id=None))
        opponentMonster = inventory_monster_set(gameState, opponentMonster.id, namedtuple_with(opponentMonster,
            ownerId=userId
        ))
        # Bailout to update battle, this also hides the opponent's monster.
        return SuspendableReturn, "battle:action#capture_success", userMonsterBall.quantity
    if state == "battle:action#capture_success":
        cache, quantity, *_ = args
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        print("BAM! Kamu mengeluarkan monster ball!")
        print("Yesss. Monsternya berhasil ketangkep!")
        print(f"Sisa monster ball: {txtqty(quantity)}")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:end", selection
    if state == "battle:action#use_potion":
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        gameState = cache.gameState
        battle = cache.battle
        selfMonsterId = battle.monster1Id if cache.turn == 1 else battle.monster2Id if cache.turn == 2 else None
        userId = battle.player1Id if cache.turn == 1 else battle.player2Id if cache.turn == 2 else None
        userMonsterBall = inventory_item_get_user_items(gameState, userId)
        # THIS IS A HACK TO CONFORM THE RULES. Empty stock are still displayed.
        # userItems = array_filter(userItems, lambda i, *_: i.quantity > 0)
        userMonsterBall = array_filter(userMonsterBall, lambda i, *_: i.referenceId != 8) # Potion id 8 is for monster ball
        if len(userMonsterBall) == 0:
            meta(action="clear")
            print("Kamu gaada potion yang bisa dipakai")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main#page2", selection
        visual = gamestate_get_visual(gameState)
        modalView = visual_show_simple_dialog(visual, "Pilih Potion", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            parent=cache.mainView)
        modalConsole = visual_with_mock(visual, modalView)
        print, input, meta = modalConsole
        meta(action="clear")
        print("Pilih potion yang ingin digunakan")
        for userItem in userMonsterBall:
            potion = potion_get(gameState, userItem.referenceId)
            description = txtkv("Stok: ", txtqty(userItem.quantity)) + f" | {potion.description}"
            input(f"{potion.name}", description, id=userItem.id, selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        # Purposefuly undefined behaviour: We expect the database to not change between selection.
        return "battle:main#use_potion_selection", cache, selection, modalView
    if state == "battle:main#use_potion_selection":
        cache, selection, modalView, *_ = args
        gameState = cache.gameState
        view_remove_child(cache.mainView, modalView)
        if cache.abortSignal is not None and selection is cache.abortSignal:
            return "battle:forcefully_aborted"
        if selection is None:
            return SuspendableReturn, "battle:main#page2"
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        userItem = inventory_item_get(gameState, selection)
        if userItem.quantity <= 0:
            print("Waduh, kamu ga punya potion ini.")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main#page2", selection
        userItem = inventory_item_set(gameState, userItem.id, namedtuple_with(userItem,
            quantity=userItem.quantity - 1
        ))
        potion = potion_get(gameState, userItem.referenceId)
        battle = cache.battle
        selfMonsterId = battle.monster1Id if cache.turn == 1 else battle.monster2Id if cache.turn == 2 else None
        selfMonster = inventory_monster_get(gameState, selfMonsterId)
        # THIS IS A HACK TO CONFORM THE RULES. Apparently, potion can only be used once per battle.
        # OMG. I am gonna kill myself. This is the fastest thing to patch something up.
        # My original plan was to change the battle schema type to be append-only history logs.
        # But it will take more time. This is the most economically-advantage time.
        __battleMonsterUsedPotionId = f"__battle-{battle.id}-monster{selfMonster.id}-used-potion-{potion.id}"
        if __battleMonsterUsedPotionId in gameState and gameState[__battleMonsterUsedPotionId] > 0:
            print("Aduh!! Monstermu gamau sama potion ini:(")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main#page2", selection
        if __battleMonsterUsedPotionId in gameState:
            gameState[__battleMonsterUsedPotionId] += 1
        else:
            gameState[__battleMonsterUsedPotionId] = 1
        # THIS IS A HACK TO CONFORM THE RULES. The way the rule's potion is designed conflicts with my potion design.
        if potion.id == 0:
            monsterType = monster_get(gameState, selfMonster.referenceId)
            newHealthPoints = selfMonster.healthPoints + 0.25 * monsterType.healthPoints
            newHealthPoints = min(monsterType.healthPoints, newHealthPoints)
            selfMonster = inventory_monster_set(gameState, selfMonster.id, namedtuple_with(selfMonster,
                healthPoints=newHealthPoints
            ))
        elif potion.id == 1:
            selfMonster = inventory_monster_set(gameState, selfMonster.id, namedtuple_with(selfMonster,
                attackPower=selfMonster.attackPower * 1.05
            ))
        elif potion.id == 2:
            selfMonster = inventory_monster_set(gameState, selfMonster.id, namedtuple_with(selfMonster,
                defensePower=selfMonster.defensePower * 1.05
            ))
        else:
            selfMonster = inventory_monster_use_potion(gameState, selfMonster, potion)
        print(f"Kamu memakai potion {ptncl(potion.name)}")
        # THIS IS A HACK TO CONFORM THE RULES. Print the potion affect message
        if potion.id == 0:
            print("Setelah meminum ramuan ini, luka-luka yang ada di dalam tubuh Pikachow sembuh dengan cepat. Dalam sekejap, Pikachow terlihat kembali prima dan siap melanjutkan pertempuran.")
        elif potion.id == 1:
            print("Setelah meminum ramuan ini, aura kekuatan terlihat mengelilingi Pikachow dan gerakannya menjadi lebih cepat dan mematikan.")
        elif potion.id == 2:
            print("Setelah meminum ramuan ini, muncul sebuah energi pelindung di sekitar Pikachow yang membuatnya terlihat semakin tangguh dan sulit dilukai.")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:main#page2", selection
    if state == "battle:action#change_monster":
        cache, *_ = args
        return "battle:main#choose_monster", cache, "battle:action#change_monster_selection"
    if state == "battle:action#change_monster_selection":
        cache, choose, *_ = args
        gameState = cache.gameState
        battle = cache.battle
        print, input, meta = cache.dialogConsole
        if choose == "Cancelled":
            return "battle:main#page2", cache
        if choose == "Nothing":
            meta(action="clear")
            print("Gada monster lainnya yang bisa dipake ngab.")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main#page2", selection
        battle = _battle_set(gameState, battle.id, namedtuple_with(battle, turn=2 if cache.turn == 1 else 1)) # switch turn
        if cache.turn == 1:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster1Id=choose))
        if cache.turn == 2:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, monster2Id=choose))
        # Bailout to update battle
        return SuspendableReturn, "battle:action#change_monster_selection?callout"
    if state == "battle:action#change_monster_selection?callout":
        # Need intermediate state to show loading
        cache, *_ = args
        print, input, meta = cache.dialogConsole
        meta(action="clear")
        print("Aku memanggil monster baru!")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        # To battle:main so that it is opponent's turn
        return SuspendableReturn, "battle:main", selection
    if state == "battle:action#escape":
        cache, forceAllowEscape, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.dialogConsole
        battle = cache.battle
        meta(action="clear")
        if not forceAllowEscape and gamestate_rand(gameState) < 0.5:
            battle = _battle_set(gameState, battle.id, namedtuple_with(battle, turn=2 if cache.turn == 1 else 1)) # switch turn
            print("Wkwkwkwkkw kamu gagal buat kabur! Monsternya pingin geleud lagi")
            input("Lanjut", selectable=True)
            selection = meta(action="select", signal=cache.abortSignal)
            return SuspendableReturn, "battle:main", selection
        battle = _battle_end_player_escaped(gameState, battle, cache.turn)
        print("Kamu berhasil untuk kabur dari battle!")
        input("Lanjut", selectable=True)
        selection = meta(action="select", signal=cache.abortSignal)
        return SuspendableReturn, "battle:end", selection
    if state == "battle:forcefully_aborted":
        # Huh, maybe do some cleanup here. Perhaps checking current state and make
        # it can be recoverable/resumable in the future. Though, this is probably safe
        # because we save the state just before the selection/promise.
        # We presumably can resume the dialog by embedding serializable value in battle.handler
        return SuspendableReturn, "battle:end"
    return SuspendableExhausted
