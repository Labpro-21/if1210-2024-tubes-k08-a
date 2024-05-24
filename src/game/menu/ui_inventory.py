from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.monster import *
from game.potion import *
from game.user import *
from game.inventory import *
from .menu import _menu_show_loading_splash
from typing import NamedTuple, Union

__InventoryEntry = Union[InventoryMonsterSchemaType, InventoryItemSchemaType]
__MenuShopCache = NamedTuple("MenuShopCache", [
    ("gameState", GameState), # expect not changed
    ("parent", View), # expect not changed
    ("abortSignal", AbortSignal), # expect not changed
    ("inventoryEntries", list[__InventoryEntry]),
    ("mainView", View), # expect not changed
    ("tableView", View), # expect not changed
    ("entryView", View), # expect not changed
    ("entryPreviewFrame", View), # expect not changed
    ("entryPreviewAnimation", View),
    ("entryDescriptionView", View), # expect not changed
    ("actionDialogView", View), # expect not changed
    ("actionDialogConsole", ConsoleMock), # expect not changed
    ("lastInputPosition", int),
    ("inputPosition", int),
    ("lastTableOffset", int),
    ("tableOffset", int),
    ("tableLoadIndices", list[int]),
])

def _menu_show_inventory(state, args):
    cache: __MenuShopCache = None
    tableMaxShown = 10
    if state is SuspendableInitial:
        gameState, parent, abortSignal = args
        userId = gamestate_get_user_id(gameState)
        monsterEntries = inventory_monster_get_user_monsters(gameState, userId)
        itemEntries = inventory_item_get_user_items(gameState, userId)
        cache = __MenuShopCache(
            gameState=gameState,
            parent=parent,
            abortSignal=abortSignal,
            inventoryEntries=[*monsterEntries, *itemEntries],
            mainView=None,
            tableView=None,
            entryView=None,
            entryPreviewFrame=None,
            entryPreviewAnimation=None,
            entryDescriptionView=None,
            actionDialogView=None,
            actionDialogConsole=None,
            lastInputPosition=None,
            inputPosition=-1,
            lastTableOffset=None,
            tableOffset=0,
            tableLoadIndices=[-1],
        )
        return "initInterface", cache, "checkTableLoad"
    if state == "initInterface":
        cache, intent, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
        driver = visual_get_driver(visual)
        dumpView = view_new(driver)

        mainView = visual_show_simple_dialog(visual, "INVENTORY", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.8), height=dim_from_absolute(3 + 2 * (2 + tableMaxShown) + 2 + 2 + 2 + 2),
            horizontalAlignment="Right",
            parent=cache.parent)
        mainView["setContent"]("OWCA: 0  ")

        entryView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_absolute(0),
            width=dim_from_factor(0.4), height=dim_from_fill(0),
            parent=mainView["contentView"])
        
        entryPreviewFrame = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_absolute(0),
            width=dim_from_fill(0), height=dim_from_factor(0.7),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=entryView)
        
        entryPreviewAnimation = None

        entryDescriptionView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_view_bottom(entryPreviewFrame),
            width=dim_from_fill(0), height=dim_from_fill(0),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=entryView)
        
        tableView = visual_show_table(visual, 
            [
                ("No.", dim_from_absolute(5), "Center"), 
                ("Tipe", dim_sub(dim_from_factor(0.2), dim_from_absolute(2)), "Right", (1, 0, 1, 0)), 
                ("Nama", dim_sub(dim_from_factor(0.6), dim_from_absolute(4)), "Left", (1, 0, 1, 0)), 
                ("Jumlah", dim_sub(dim_from_factor(0.2), dim_from_absolute(1)), "Center")],
            [],
            x=pos_from_view_right(entryView), y=pos_from_absolute(2),
            width=dim_from_fill(0), height=dim_from_fill(0),
            parent=mainView["contentView"])
        tableView["selectable"](True)
        
        actionDialogView = visual_show_simple_dialog(visual, "BELI", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            parent=dumpView)
        actionDialogConsole = visual_with_mock(visual, actionDialogView, 
            hasTitle=True, selectableAlignment="Bottom", inputBoxOffset=2)
    
        cache = namedtuple_with(cache,
            mainView=mainView,
            tableView=tableView,
            entryView=entryView,
            entryPreviewFrame=entryPreviewFrame,
            entryPreviewAnimation=entryPreviewAnimation,
            entryDescriptionView=entryDescriptionView,
            actionDialogView=actionDialogView,
            actionDialogConsole=actionDialogConsole,
        )
        return intent, cache
    if state == "checkTableLoad":
        cache, *_ = args
        gameState = cache.gameState
        tableLoadIndex = (cache.tableOffset + tableMaxShown - 1) // tableMaxShown
        tableBeforeLoadIndex = cache.tableOffset // tableMaxShown
        if array_includes(cache.tableLoadIndices, tableLoadIndex) and array_includes(cache.tableLoadIndices, tableBeforeLoadIndex):
            visual = gamestate_get_visual(gameState)
            if cache.parent is not None:
                visual_set_view(visual, visual_get_root_view(visual, cache.parent))
            elif cache.mainView is not None:
                visual_set_view(visual, cache.mainView)
            return "updateTableEntries", cache
        loadItemSprites = dict()
        if not array_includes(cache.tableLoadIndices, tableLoadIndex):
            startIndex = tableLoadIndex * tableMaxShown
            endIndex = startIndex + tableMaxShown
            loadItems = array_slice(cache.inventoryEntries, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: __resolve_inventory_entry(gameState, i)[3])
            loadItemSprites2 = array_map(loadItemSprites2, lambda s, *_: (f"sprite {s}", s))
            loadItemSprites = dict_set(loadItemSprites, loadItemSprites2)
            cache = namedtuple_with(cache,
                tableLoadIndices=[*cache.tableLoadIndices, tableLoadIndex]
            )
        if not array_includes(cache.tableLoadIndices, tableBeforeLoadIndex):
            startIndex = tableBeforeLoadIndex * tableMaxShown
            endIndex = startIndex + tableMaxShown
            loadItems = array_slice(cache.inventoryEntries, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: __resolve_inventory_entry(gameState, i)[3])
            loadItemSprites2 = array_map(loadItemSprites2, lambda s, *_: (f"sprite {s}", s))
            loadItemSprites = dict_set(loadItemSprites, loadItemSprites2)
            cache = namedtuple_with(cache,
                tableLoadIndices=[*cache.tableLoadIndices, tableBeforeLoadIndex]
            )
        promise = promise_from_suspendable(_menu_show_loading_splash, gameState, loadItemSprites)
        return "checkTableLoad", cache, promise
    if state == "updateTableEntries":
        cache, *_ = args
        if cache.tableOffset == cache.lastTableOffset:
            return "updateItemView", cache
        gameState = cache.gameState
        tableView = cache.tableView
        startIndex = cache.tableOffset
        endIndex = startIndex + tableMaxShown
        itemRows = array_slice(cache.inventoryEntries, startIndex, endIndex)
        def getRowFor(i: int, inventoryEntry: __InventoryEntry):
            resolvedEntry = __resolve_inventory_entry(gameState, inventoryEntry)
            entryType = "monster" if __is_inventory_entries_monster(inventoryEntry) else "item"
            return [f"{startIndex + i + 1}", entryType, resolvedEntry[0], resolvedEntry[2]]
        itemRows = array_map(itemRows, lambda it, i, *_: getRowFor(i, it))
        tableView["updateRows"]([
            ["▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲"],
            *itemRows,
            ["▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼"],
        ])
        cache = namedtuple_with(cache,
            lastTableOffset=cache.tableOffset
        )
        return "updateItemView", cache
    if state == "updateItemView":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        userMoney = user_get_current(gameState).money
        mainView["setContent"](f"OWCA: {userMoney}  ")
        if cache.inputPosition == cache.lastInputPosition:
            return "waitInput", cache
        visual = gamestate_get_visual(gameState)
        inputPosition = cache.inputPosition
        entryPreviewFrame = cache.entryPreviewFrame
        entryPreviewAnimation = cache.entryPreviewAnimation
        entryDescriptionView = cache.entryDescriptionView
        if entryPreviewAnimation is not None:
            entryPreviewAnimation["stop"]()
            view_remove_child(entryPreviewFrame, entryPreviewAnimation)
            entryPreviewAnimation = None
            entryDescriptionView["setContent"]("")
        if inputPosition < -1:
            inputPosition = -1
        if inputPosition >= len(cache.inventoryEntries):
            inputPosition = len(cache.inventoryEntries) - 1
        if inputPosition != -1:
            inventoryEntry = cache.inventoryEntries[inputPosition]
            entryName, entryDescription, entryQuantity, entrySprite = __resolve_inventory_entry(gameState, inventoryEntry)
            entryPreviewAnimation = visual_show_splash(visual, entrySprite, parent=entryPreviewFrame)
            entryPreviewAnimation["play"](60, True)
            description = f"ID: {inputPosition}\n"
            description += f"Nama: {entryName}\n"
            if entryQuantity != "-":
                description += f"Jumlah: {entryQuantity}\n"
            description += entryDescription
            entryDescriptionView["setContent"](description)
        cache = namedtuple_with(cache,
            lastInputPosition=inputPosition,
            entryPreviewAnimation=entryPreviewAnimation,
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
                if event.key == "Home" or event.key == "PageUp":
                    resolve((None, "home"))
                    return
                if event.key == "End" or event.key == "PageDown":
                    resolve((None, "end"))
                    return
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
        if action == "home":
            tableView["setSelection"](1)
            cache = namedtuple_with(cache,
                tableOffset=0,
                inputPosition=0,
            )
            return "checkTableLoad", cache
        if action == "end":
            tableView["setSelection"](min(len(cache.inventoryEntries), tableMaxShown))
            cache = namedtuple_with(cache,
                tableOffset=max(0, len(cache.inventoryEntries) - tableMaxShown),
                inputPosition=len(cache.inventoryEntries) - 1,
            )
            return "checkTableLoad", cache
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
        if position == min(len(cache.inventoryEntries) + 1, tableMaxShown + 1):
            tableView["setSelection"](min(len(cache.inventoryEntries), tableMaxShown))
            tableOffset = min(max(0, len(cache.inventoryEntries) - tableMaxShown), tableOffset + 1)
            inputPosition = tableOffset + (min(len(cache.inventoryEntries), tableMaxShown) - 1)
            cache = namedtuple_with(cache,
                tableOffset=tableOffset,
                inputPosition=inputPosition,
            )
            return "checkTableLoad", cache
        cache = namedtuple_with(cache,
            inputPosition=inputPosition
        )
        # if action == "enter":
        #     return "actionDialog", cache
        return "updateItemView", cache
    # if state == "actionDialog":
    #     cache, *_ = args
    #     gameState = cache.gameState
    #     mainView = cache.mainView
    #     tableView = cache.tableView
    #     actionDialogView = cache.actionDialogView
    #     tableView["selectable"](False)
    #     view_add_child(mainView["contentView"], actionDialogView)
    #     userMoney = user_get_current(gameState).money
    #     print, input, meta = cache.actionDialogConsole
    #     inventoryEntry = cache.inventoryEntries[cache.inputPosition]
    #     itemName = __resolve_inventory_entry(gameState, inventoryEntry)[0]
    #     meta(action="clear")
    #     print(f"==== Beli '{itemName}' @ {inventoryEntry.cost} ====")
    #     print("Masukkan jumlah yang ingin dibeli.")
    #     def onChange(v):
    #         meta(action="clearPrint")
    #         if v == "":
    #             print("Masukkan jumlah yang ingin dibeli.")
    #             return
    #         quantity = parse_int(v)
    #         if quantity is None or quantity <= 0:
    #             print("Jumlah yang dimasukkan tidak valid.")
    #             return
    #         subtotal = quantity * inventoryEntry.cost
    #         print(f"Total harga: {quantity} * {inventoryEntry.cost} = {subtotal}")
    #         if userMoney < subtotal:
    #             print(f"Uangmu tidak cukup.")
    #     quantity = input("Jumlah: ", f"Uangmu: {userMoney}", onChange=onChange)
    #     return "actionDialogConfirm", cache, quantity
    # if state == "actionDialogConfirm":
    #     cache, quantity, *_ = args
    #     if quantity is None:
    #         return "actionDialogConfirmChoose", cache, None, "Batal"
    #     quantity = parse_int(quantity)
    #     if quantity is None or quantity <= 0:
    #         return "actionDialog", cache
    #     gameState = cache.gameState
    #     inventoryEntry = cache.inventoryEntries[cache.inputPosition]
    #     itemName = __resolve_inventory_entry(gameState, inventoryEntry)[0]
    #     print, input, meta = cache.actionDialogConsole
    #     meta(action="clear")
    #     userMoney = user_get_current(gameState).money
    #     subtotal = quantity * inventoryEntry.cost
    #     if userMoney < subtotal:
    #         print(f"Uangmu tidak cukup. ", end="")
    #         input("Lanjut", selectable=True)
    #         selection = meta(action="select")
    #         return "actionDialogConfirmChoose", cache, None, "Batal", selection
    #     meta("keySpeed", 120)
    #     print(f"OWCA mu saat ini terdapat {userMoney}. ", end="")
    #     print(f"Kamu akan membeli '{itemName}' dengan harga satuan {inventoryEntry.cost} sebanyak {quantity} dengan subtotal {subtotal}. ", end="")
    #     print(f"Di akhir transaksi OWCA mu akan tersisa {userMoney - subtotal}.")
    #     input("Konfirmasi", selectable=True)
    #     input("Batal", selectable=True)
    #     selection = meta(action="select")
    #     return "actionDialogConfirmChoose", cache, quantity, selection
    # if state == "actionDialogConfirmChoose":
    #     cache, quantity, selection, *_ = args
    #     print, input, meta = cache.actionDialogConsole
    #     meta("keySpeed", -1)
    #     if selection is None:
    #         return "actionDialog", cache
    #     gameState = cache.gameState
    #     mainView = cache.mainView
    #     tableView = cache.tableView
    #     actionDialogView = cache.actionDialogView
    #     view_remove_child(mainView["contentView"], actionDialogView)
    #     tableView["selectable"](True)
    #     if selection == "Batal":
    #         return "updateItemView", cache
    #     inventoryEntry = cache.inventoryEntries[cache.inputPosition]
    #     currentUser = user_get_current(gameState)
    #     userMoney = currentUser.money - quantity * inventoryEntry.cost
    #     currentUser = user_set(gameState, currentUser.id, namedtuple_with(currentUser, money=userMoney))
    #     if inventoryEntry.referenceType == "monster":
    #         monsterType = monster_get(gameState, inventoryEntry.referenceId)
    #         for _ in range(quantity):
    #             newMonster = inventory_monster_new(gameState)
    #             newMonster = inventory_monster_set(gameState, newMonster.id, namedtuple_with(newMonster,
    #                 ownerId=currentUser.id,
    #                 referenceId=monsterType.id,
    #                 name=monsterType.name,
    #                 experiencePoints=0,
    #                 healthPoints=monsterType.healthPoints,
    #                 attackPower=monsterType.attackPower,
    #                 defensePower=monsterType.defensePower,
    #                 activePotions=[]
    #             ))
    #     if inventoryEntry.referenceType == "item":
    #         itemType = potion_get(gameState, inventoryEntry.referenceId)
    #         userItems = inventory_item_get_user_items(gameState, currentUser.id)
    #         userItem = array_find(userItems, lambda i, *_: i.referenceId == itemType.id)
    #         if userItem is None:
    #             userItem = inventory_item_new(gameState)
    #             userItem = inventory_item_set(gameState, userItem.id, namedtuple_with(userItem,
    #                 ownerId=currentUser.id,
    #                 referenceId=itemType.id,
    #                 quantity=quantity
    #             ))
    #         else:
    #             userItem = inventory_item_set(gameState, userItem.id, namedtuple_with(userItem,
    #                 quantity=userItem.quantity + quantity
    #             ))
    #     return "updateItemView", cache
    return SuspendableExhausted

def __is_inventory_entries_monster(inventoryEntry: __InventoryEntry) -> bool:
    return hasattr(inventoryEntry, "healthPoints")
def __is_inventory_entries_item(inventoryEntry: __InventoryEntry) -> bool:
    return not hasattr(inventoryEntry, "healthPoints")
def __resolve_inventory_entry(gameState: GameState, inventoryEntry: ShopSchemaType):
    if __is_inventory_entries_monster(inventoryEntry):
        monster: InventoryMonsterSchemaType = inventoryEntry
        monsterType = monster_get(gameState, monster.referenceId)
        description = f"Family: {monsterType.family} Level: {monsterType.level}\nATK: {monster.attackPower}     DEF: {monster.defensePower}\nDeskripsi: {monsterType.description}"
        return (monster.name, description, "-", monsterType.spriteFront)
    if __is_inventory_entries_item(inventoryEntry):
        potion: InventoryItemSchemaType = inventoryEntry
        potionType = potion_get(gameState, potion.referenceId)
        description = f"Deskripsi: {potionType.description}"
        return (potionType.name, description, f"{potion.quantity}", potionType.sprite)
