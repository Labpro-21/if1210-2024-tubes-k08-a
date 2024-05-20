from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.laboratory import *
from game.monster import *
from game.user import *
from game.inventory import *
from .menu import _menu_show_loading_splash
from typing import NamedTuple

__MenuLaboratoryCache = NamedTuple("MenuLaboratoryCache", [
    ("gameState", GameState), # expect not changed
    ("parent", View), # expect not changed
    ("abortSignal", AbortSignal), # expect not changed
    ("upgradeOptions", list[LaboratorySchemaType]),
    ("mainView", View), # expect not changed
    ("upgradeView", View), # expect not changed
    ("beforePreviewFrame", View), # expect not changed
    ("beforePreviewAnimation", View),
    ("beforeDescriptionView", View), # expect not changed
    ("afterPreviewFrame", View), # expect not changed
    ("afterPreviewAnimation", View),
    ("afterDescriptionView", View), # expect not changed
    ("tableView", View), # expect not changed
    ("upgradeDialogView", View), # expect not changed
    ("upgradeDialogConsole", ConsoleMock), # expect not changed
    ("lastInputPosition", int),
    ("inputPosition", int),
    ("lastTableOffset", int),
    ("tableOffset", int),
    ("tableLoadIndex", int),
])

def _menu_show_laboratory(state, args):
    cache: __MenuLaboratoryCache = None
    tableMaxShown = 3
    if state is SuspendableInitial:
        gameState, parent, abortSignal = args
        userId = gamestate_get_user_id(gameState)
        userMonsters = inventory_monster_get_user_monsters(gameState, userId)
        userMonsters = array_map(userMonsters, lambda m, *_: m.referenceId)
        upgradeOptions = laboratory_get_all_upgrades(gameState)
        upgradeOptions = array_filter(upgradeOptions, lambda u, *_: array_includes(userMonsters, u.fromMonsterId))
        cache = __MenuLaboratoryCache(
            gameState=gameState,
            parent=parent,
            abortSignal=abortSignal,
            upgradeOptions=upgradeOptions,
            mainView=None,
            upgradeView=None,
            beforePreviewFrame=None,
            beforePreviewAnimation=None,
            beforeDescriptionView=None,
            afterPreviewFrame=None,
            afterPreviewAnimation=None,
            afterDescriptionView=None,
            tableView=None,
            upgradeDialogView=None,
            upgradeDialogConsole=None,
            lastInputPosition=None,
            inputPosition=-1,
            lastTableOffset=None,
            tableOffset=0,
            tableLoadIndex=None,
        )
        return "initInterface", cache, "checkTableLoad"
    if state == "initInterface":
        cache, intent, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
        driver = visual_get_driver(visual)
        dumpView = view_new(driver)

        mainView = visual_show_simple_dialog(visual, "LABORATORY", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.8), #height=dim_from_absolute(3 + 2 * (2 + tableMaxShown) + 2 + 24),
            height=dim_from_factor(0.8),
            parent=cache.parent)
        mainView["setContent"]("  OWCA: 0")

        tableView = visual_show_table(visual, 
            [
                ("No.", dim_from_absolute(5), "Center"), 
                ("Nama", dim_from_factor(0.3), "Right", (1, 0, 1, 0)), 
                ("HP", dim_sub(dim_from_factor(0.167), dim_from_absolute(2)), "Center"), 
                ("ATK", dim_sub(dim_from_factor(0.167), dim_from_absolute(2)), "Center"), 
                ("DEF", dim_sub(dim_from_factor(0.167), dim_from_absolute(2)), "Center"), 
                ("Harga", dim_from_fill(0), "Center")],
            [],
            x=pos_from_absolute(0), y=pos_from_end(None),
            width=dim_from_fill(0), height=dim_from_absolute(3 + 2 * (2 + tableMaxShown)),
            parent=mainView["contentView"])
        tableView["selectable"](True)
        
        upgradeView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_absolute(2),
            width=dim_from_fill(0), height=dim_sub(dim_from_fill(0), dim_from_view_height(tableView)),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=mainView["contentView"])
        
        beforePreviewFrame = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_absolute(0),
            width=dim_from_factor(0.5), height=dim_from_factor(0.7),
            border=(1, 1, 1, 1), padding=(0, 0, 0, 0),
            parent=upgradeView)
        
        beforePreviewAnimation = None

        beforeDescriptionView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_view_bottom(beforePreviewFrame),
            width=dim_from_factor(0.5), height=dim_from_fill(0),
            parent=upgradeView)
        
        afterPreviewFrame = visual_show_simple_dialog(visual, None, "",
            x=pos_from_view_right(beforePreviewFrame), y=pos_from_absolute(0),
            width=dim_from_fill(0), height=dim_from_factor(0.7),
            border=(1, 1, 1, 1), padding=(0, 0, 0, 0),
            parent=upgradeView)
        
        afterPreviewAnimation = None

        afterDescriptionView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_view_right(beforePreviewFrame), y=pos_from_view_bottom(afterPreviewFrame),
            width=dim_from_fill(0), height=dim_from_fill(0),
            parent=upgradeView)
        
        upgradeDialogView = visual_show_simple_dialog(visual, "UPGRADE", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            parent=dumpView)
        upgradeDialogConsole = visual_with_mock(visual, upgradeDialogView, 
            hasTitle=True)
    
        cache = namedtuple_with(cache,
            mainView=mainView,
            upgradeView=upgradeView,
            beforePreviewFrame=beforePreviewFrame,
            beforePreviewAnimation=beforePreviewAnimation,
            beforeDescriptionView=beforeDescriptionView,
            afterPreviewFrame=afterPreviewFrame,
            afterPreviewAnimation=afterPreviewAnimation,
            afterDescriptionView=afterDescriptionView,
            tableView=tableView,
            upgradeDialogView=upgradeDialogView,
            upgradeDialogConsole=upgradeDialogConsole,
        )
        return intent, cache
    if state == "checkTableLoad":
        cache, *_ = args
        gameState = cache.gameState
        tableLoadIndex = (cache.tableOffset + tableMaxShown - 1) // tableMaxShown
        if cache.tableLoadIndex is not None and tableLoadIndex <= cache.tableLoadIndex:
            visual = gamestate_get_visual(gameState)
            if cache.parent is not None:
                visual_set_view(visual, visual_get_root_view(visual, cache.parent))
            else:
                visual_set_view(visual, cache.mainView)
            return "updateTableEntries", cache
        startIndex = tableLoadIndex * tableMaxShown
        endIndex = startIndex + tableMaxShown
        def getSpriteFor(upgradeOption: LaboratorySchemaType):
            beforeMonster, afterMonster = __resolve_laboratory_upgrade(gameState, upgradeOption)
            return [beforeMonster.spriteFront, afterMonster.spriteFront]
        loadUpgrades = array_slice(cache.upgradeOptions, startIndex, endIndex)
        loadUpgradeSprites = array_map(loadUpgrades, lambda i, *_: getSpriteFor(i))
        loadUpgradeSprites = array_flat(loadUpgradeSprites)
        loadUpgradeSprites = array_map(loadUpgradeSprites, lambda s, *_: (f"sprite {s}", s))
        loadUpgradeSprites = dict_set(dict(), loadUpgradeSprites)
        promise = promise_from_suspendable(_menu_show_loading_splash, gameState, loadUpgradeSprites)
        cache = namedtuple_with(cache,
            tableLoadIndex=tableLoadIndex
        )
        return "checkTableLoad", cache, promise
    if state == "updateTableEntries":
        cache, *_ = args
        if cache.tableOffset == cache.lastTableOffset:
            return "updateUpgradeView", cache
        gameState = cache.gameState
        tableView = cache.tableView
        startIndex = cache.tableOffset
        endIndex = startIndex + tableMaxShown
        upgradeRows = array_slice(cache.upgradeOptions, startIndex, endIndex)
        def getRowFor(i: int, upgradeOption: LaboratorySchemaType):
            beforeMonster, afterMonster = __resolve_laboratory_upgrade(gameState, upgradeOption)
            hpRatio = (afterMonster.healthPoints - beforeMonster.healthPoints) / beforeMonster.healthPoints
            atkRatio = (afterMonster.attackPower - beforeMonster.attackPower) / beforeMonster.attackPower
            defRatio = (afterMonster.defensePower - beforeMonster.defensePower) / beforeMonster.defensePower
            rowName = f"{beforeMonster.name} ({beforeMonster.level}) --> ({afterMonster.level}) {afterMonster.name}"
            rowHp = f"{beforeMonster.healthPoints} {'+' if hpRatio >= 0 else '-'}{hpRatio * 100:.2f}%"
            rowAtk = f"{beforeMonster.attackPower} {'+' if atkRatio >= 0 else '-'}{atkRatio * 100:.2f}%"
            rowDef = f"{beforeMonster.defensePower} {'+' if defRatio >= 0 else '-'}{defRatio * 100:.2f}%"
            return [f"{startIndex + i + 1}", rowName, rowHp, rowAtk, rowDef, f"{upgradeOption.cost}"]
        upgradeRows = array_map(upgradeRows, lambda u, i, *_: getRowFor(i, u))
        tableView["updateRows"]([
            ["▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲"],
            *upgradeRows,
            ["▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼"],
        ])
        cache = namedtuple_with(cache,
            lastTableOffset=cache.tableOffset
        )
        return "updateUpgradeView", cache
    if state == "updateUpgradeView":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        userMoney = user_get_current(gameState).money
        mainView["setContent"](f"  OWCA: {userMoney}")
        if cache.inputPosition == cache.lastInputPosition:
            return "waitInput", cache
        visual = gamestate_get_visual(gameState)
        inputPosition = cache.inputPosition
        beforePreviewFrame = cache.beforePreviewFrame
        beforePreviewAnimation = cache.beforePreviewAnimation
        beforeDescriptionView = cache.beforeDescriptionView
        afterPreviewFrame = cache.afterPreviewFrame
        afterPreviewAnimation = cache.afterPreviewAnimation
        afterDescriptionView = cache.afterDescriptionView
        if beforePreviewAnimation is not None:
            beforePreviewAnimation["stop"]()
            view_remove_child(beforePreviewFrame, beforePreviewAnimation)
            beforePreviewAnimation = None
        if afterPreviewAnimation is not None:
            afterPreviewAnimation["stop"]()
            view_remove_child(afterPreviewFrame, afterPreviewAnimation)
            afterPreviewAnimation = None
        if inputPosition < -1:
            inputPosition = -1
        if inputPosition >= len(cache.upgradeOptions):
            inputPosition = len(cache.upgradeOptions) - 1
        if inputPosition != -1:
            upgradeOption = cache.upgradeOptions[inputPosition]
            beforeMonster, afterMonster = __resolve_laboratory_upgrade(gameState, upgradeOption)
            beforePreviewAnimation = visual_show_splash(visual, beforeMonster.spriteFront, parent=beforePreviewFrame)
            beforePreviewAnimation["play"](60, True)
            beforeDescriptionView["setContent"](f"Nama: {beforeMonster.name} ({beforeMonster.level})\nHP: {beforeMonster.healthPoints}\nATK: {beforeMonster.attackPower}\nDEF: {beforeMonster.defensePower}")
            afterPreviewAnimation = visual_show_splash(visual, afterMonster.spriteFront, parent=afterPreviewFrame)
            afterPreviewAnimation["play"](60, True)
            afterDescriptionView["setContent"](f"Nama: {afterMonster.name} ({afterMonster.level})\nHP: {afterMonster.healthPoints}\nATK: {afterMonster.attackPower}\nDEF: {afterMonster.defensePower}")
        cache = namedtuple_with(cache,
            lastInputPosition=inputPosition,
            beforePreviewAnimation=beforePreviewAnimation,
            afterPreviewAnimation=afterPreviewAnimation,
        )
        return "waitInput", cache
    if state == "waitInput":
        cache, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
        tableView = cache.tableView
        def executor(resolve, _):
            def cleanup():
                tableView["onHover"](None)
                tableView["onEnter"](None)
                visual_remove_key_listener(visual, tableView, onKey)
            def onHover(index):
                cleanup()
                resolve((index, "hover"))
            def onEnter(index):
                cleanup()
                resolve((index, "enter"))
            def onKey(event: KeyEvent):
                if event.key == "ControlESC":
                    cleanup()
                    resolve((None, "escape"))
            tableView["onHover"](onHover)
            tableView["onEnter"](onEnter)
            visual_add_key_listener(visual, tableView, onKey)
        promise = promise_new(executor)
        return "processInput", cache, promise
    if state == "processInput":
        cache, inputAction, *_ = args
        tableView = cache.tableView
        position, action = inputAction
        if action == "escape":
            return SuspendableReturn, None
        tableOffset = cache.tableOffset
        inputPosition = tableOffset + (position - 1)
        if position == 0:
            tableView["setSelection"](1)
            tableOffset = max(0, tableOffset - 1)
            inputPosition = tableOffset + position
            cache = namedtuple_with(cache,
                tableOffset=tableOffset,
                inputPosition=inputPosition,
            )
            return "checkTableLoad", cache
        if position == min(len(cache.upgradeOptions) + 1, tableMaxShown + 1):
            tableView["setSelection"](min(len(cache.upgradeOptions), tableMaxShown))
            tableOffset = min(max(0, len(cache.upgradeOptions) - tableMaxShown), tableOffset + 1)
            inputPosition = tableOffset + (min(len(cache.upgradeOptions), tableMaxShown) - 1)
            cache = namedtuple_with(cache,
                tableOffset=tableOffset,
                inputPosition=inputPosition,
            )
            return "checkTableLoad", cache
        cache = namedtuple_with(cache,
            inputPosition=inputPosition
        )
        if action == "enter":
            return "upgradeDialog", cache
        return "updateUpgradeView", cache
    if state == "upgradeDialog":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        upgradeDialogView = cache.upgradeDialogView
        tableView["selectable"](False)
        view_add_child(mainView["contentView"], upgradeDialogView)
        userMoney = user_get_current(gameState).money
        upgradeOption = cache.upgradeOptions[cache.inputPosition]
        beforeMonster, afterMonster = __resolve_laboratory_upgrade(gameState, upgradeOption)
        print, input, meta = cache.upgradeDialogConsole
        meta(action="clear")
        print(f"==== Upgrade {beforeMonster.name} ({beforeMonster.level}) --> ({afterMonster.level}) {afterMonster.name} ====")
        if userMoney < upgradeOption.cost:
            print("Uangmu tidak cukup untuk melakukan upgrade ini.")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "upgradeDialogConfirmChoose", cache, None, "Batal", selection
        print("Pilih monster yang ingin di upgrade.")
        userId = gamestate_get_user_id(gameState)
        userMonsters = inventory_monster_get_user_monsters(gameState, userId)
        userMonsters = array_filter(userMonsters, lambda m, *_: m.referenceId == upgradeOption.fromMonsterId)
        for userMonster in userMonsters:
            targetHp = max(userMonster.healthPoints, afterMonster.healthPoints)
            targetAtk = max(userMonster.attackPower, afterMonster.attackPower)
            targetDef = max(userMonster.defensePower, afterMonster.defensePower)
            hpRatio = (targetHp - userMonster.healthPoints) / userMonster.healthPoints
            atkRatio = (targetAtk - userMonster.attackPower) / userMonster.attackPower
            defRatio = (targetDef - userMonster.defensePower) / userMonster.defensePower
            rowHp = f"{userMonster.healthPoints} {'+' if hpRatio >= 0 else '-'}{hpRatio * 100:.2f}%"
            rowAtk = f"{userMonster.attackPower} {'+' if atkRatio >= 0 else '-'}{atkRatio * 100:.2f}%"
            rowDef = f"{userMonster.defensePower} {'+' if defRatio >= 0 else '-'}{defRatio * 100:.2f}%"
            description = f"HP: {rowHp} ATK: {rowAtk} DEF: {rowDef}"
            input(f"{userMonster.name}", description, id=userMonster.id, selectable=True)
        selection = meta(action="select")
        return "upgradeDialogConfirm", cache, selection
    if state == "upgradeDialogConfirm":
        cache, monsterId, *_ = args
        if monsterId is None:
            return "upgradeDialogConfirmChoose", cache, None, "Batal"
        gameState = cache.gameState
        userMoney = user_get_current(gameState).money
        userMonster = inventory_monster_get(gameState, monsterId)
        upgradeOption = cache.upgradeOptions[cache.inputPosition]
        beforeMonster, afterMonster = __resolve_laboratory_upgrade(gameState, upgradeOption)
        print, input, meta = cache.upgradeDialogConsole
        meta(action="clear")
        if userMoney < upgradeOption.cost:
            print(f"Uangmu tidak cukup. ", end="")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "upgradeDialogConfirmChoose", cache, None, "Batal", selection
        targetHp = max(userMonster.healthPoints, afterMonster.healthPoints)
        targetAtk = max(userMonster.attackPower, afterMonster.attackPower)
        targetDef = max(userMonster.defensePower, afterMonster.defensePower)
        meta("keySpeed", 120)
        print(f"OWCA mu saat ini terdapat {userMoney}. ", end="")
        print(f"Kamu akan mengupgrade '{userMonster.name}' dari level {beforeMonster.level} ke level {afterMonster.level} dengan harga {upgradeOption.cost}. ", end="")
        print(f"Di akhir transaksi OWCA mu akan tersisa {userMoney - upgradeOption.cost}. Dan '{userMonster.name}' akan memiliki HP: {targetHp} ATK: {targetAtk} DEF: {targetDef}")
        input("Konfirmasi", selectable=True)
        input("Batal", selectable=True)
        selection = meta(action="select")
        return "upgradeDialogConfirmChoose", cache, monsterId, selection
    if state == "upgradeDialogConfirmChoose":
        cache, monsterId, selection, *_ = args
        print, input, meta = cache.upgradeDialogConsole
        meta("keySpeed", -1)
        if selection is None:
            return "upgradeDialog", cache
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        upgradeDialogView = cache.upgradeDialogView
        view_remove_child(mainView["contentView"], upgradeDialogView)
        tableView["selectable"](True)
        if selection == "Batal":
            return "updateUpgradeView", cache
        userMonster = inventory_monster_get(gameState, monsterId)
        upgradeOption = cache.upgradeOptions[cache.inputPosition]
        _, afterMonster = __resolve_laboratory_upgrade(gameState, upgradeOption)
        currentUser = user_get_current(gameState)
        userMoney = currentUser.money - upgradeOption.cost
        currentUser = user_set(gameState, currentUser.id, namedtuple_with(currentUser, money=userMoney))
        targetHp = max(userMonster.healthPoints, afterMonster.healthPoints)
        targetAtk = max(userMonster.attackPower, afterMonster.attackPower)
        targetDef = max(userMonster.defensePower, afterMonster.defensePower)
        userMonster = inventory_monster_set(gameState, userMonster.id, namedtuple_with(userMonster,
            referenceId=afterMonster.id,
            healthPoints=targetHp,
            attackPower=targetAtk,
            defensePower=targetDef,
        ))
        return "reloadAll", cache
    if state == "reloadAll": # I am too lazy, sorry.
        cache, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
        if cache.parent is not None:
            view_remove_child(cache.parent, cache.mainView)
        else:
            visual_set_view(visual, None)
        return SuspendableInitial, cache.gameState, cache.parent, cache.abortSignal
    return SuspendableExhausted

def __resolve_laboratory_upgrade(gameState: GameState, upgradeOption: LaboratorySchemaType):
    beforeMonster = monster_get(gameState, upgradeOption.fromMonsterId)
    afterMonster = monster_get(gameState, upgradeOption.toMonsterId)
    return (beforeMonster, afterMonster)