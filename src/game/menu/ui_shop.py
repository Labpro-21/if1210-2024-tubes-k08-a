from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.shop import *
from game.monster import *
from game.potion import *
from game.user import *
from game.inventory import *
from .menu import _menu_show_loading_splash
from typing import NamedTuple

__MenuShopCache = NamedTuple("MenuShopCache", [
    ("gameState", GameState), # expect not changed
    ("parent", View), # expect not changed
    ("abortSignal", AbortSignal), # expect not changed
    ("shopItems", list[ShopSchemaType]),
    ("mainView", View), # expect not changed
    ("tableView", View), # expect not changed
    ("itemView", View), # expect not changed
    ("itemPreviewFrame", View), # expect not changed
    ("itemPreviewAnimation", View),
    ("itemDescriptionView", View), # expect not changed
    ("buyDialogView", View), # expect not changed
    ("buyDialogConsole", ConsoleMock), # expect not changed
    ("lastInputPosition", int),
    ("inputPosition", int),
    ("lastTableOffset", int),
    ("tableOffset", int),
    ("tableLoadIndex", int),
])

def _menu_show_shop(state, args):
    cache: __MenuShopCache = None
    tableMaxShown = 10
    if state is SuspendableInitial:
        gameState, parent, abortSignal = args
        cache = __MenuShopCache(
            gameState=gameState,
            parent=parent,
            abortSignal=abortSignal,
            shopItems=shop_get_all_items(gameState),
            mainView=None,
            tableView=None,
            itemView=None,
            itemPreviewFrame=None,
            itemPreviewAnimation=None,
            itemDescriptionView=None,
            buyDialogView=None,
            buyDialogConsole=None,
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

        mainView = visual_show_simple_dialog(visual, "SHOP", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.8), height=dim_from_absolute(3 + 2 * (2 + tableMaxShown) + 2 + 2 + 2 + 2),
            parent=cache.parent)
        mainView["setContent"]("  OWCA: 0")
        
        tableView = visual_show_table(visual, 
            [
                ("No.", dim_from_absolute(5), "Center"), 
                ("Tipe", dim_sub(dim_from_factor(0.2), dim_from_absolute(2)), "Right", (1, 0, 1, 0)), 
                ("Nama", dim_sub(dim_from_factor(0.6), dim_from_absolute(4)), "Left", (1, 0, 1, 0)), 
                ("Harga", dim_sub(dim_from_factor(0.2), dim_from_absolute(1)), "Center")],
            [],
            x=pos_from_absolute(0), y=pos_from_absolute(2),
            width=dim_from_factor(0.6), height=dim_from_fill(0),
            parent=mainView["contentView"])
        tableView["selectable"](True)

        itemView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_view_right(tableView), y=pos_from_absolute(0),
            width=dim_from_fill(0), height=dim_from_fill(0),
            parent=mainView["contentView"])
        
        itemPreviewFrame = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_absolute(0),
            width=dim_from_fill(0), height=dim_from_factor(0.7),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=itemView)
        
        itemPreviewAnimation = None

        itemDescriptionView = visual_show_simple_dialog(visual, None, "",
            x=pos_from_absolute(0), y=pos_from_view_bottom(itemPreviewFrame),
            width=dim_from_fill(0), height=dim_from_fill(0),
            border=(0, 0, 0, 0), padding=(0, 0, 0, 0),
            parent=itemView)
        
        buyDialogView = visual_show_simple_dialog(visual, "BELI", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            parent=dumpView)
        buyDialogConsole = visual_with_mock(visual, buyDialogView, 
            hasTitle=True, selectableAlignment="Bottom", inputBoxOffset=2)
    
        cache = namedtuple_with(cache,
            mainView=mainView,
            tableView=tableView,
            itemView=itemView,
            itemPreviewFrame=itemPreviewFrame,
            itemPreviewAnimation=itemPreviewAnimation,
            itemDescriptionView=itemDescriptionView,
            buyDialogView=buyDialogView,
            buyDialogConsole=buyDialogConsole,
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
            elif cache.mainView is not None:
                visual_set_view(visual, cache.mainView)
            return "updateTableEntries", cache
        startIndex = tableLoadIndex * tableMaxShown
        endIndex = startIndex + tableMaxShown
        loadItems = array_slice(cache.shopItems, startIndex, endIndex)
        loadItemSprites = array_map(loadItems, lambda i, *_: __resolve_shop_item(gameState, i)[2])
        loadItemSprites = array_map(loadItemSprites, lambda s, *_: (f"sprite {s}", s))
        loadItemSprites = dict_set(dict(), loadItemSprites)
        promise = promise_from_suspendable(_menu_show_loading_splash, gameState, loadItemSprites)
        cache = namedtuple_with(cache,
            tableLoadIndex=tableLoadIndex
        )
        return "checkTableLoad", cache, promise
    if state == "updateTableEntries":
        cache, *_ = args
        if cache.tableOffset == cache.lastTableOffset:
            return "updateItemView", cache
        gameState = cache.gameState
        tableView = cache.tableView
        startIndex = cache.tableOffset
        endIndex = startIndex + tableMaxShown
        itemRows = array_slice(cache.shopItems, startIndex, endIndex)
        itemRows = array_map(itemRows, lambda it, i, *_: [f"{startIndex + i + 1}", it.referenceType, __resolve_shop_item(gameState, it)[0], f"{it.cost}"])
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
        mainView["setContent"](f"  OWCA: {userMoney}")
        if cache.inputPosition == cache.lastInputPosition:
            return "waitInput", cache
        visual = gamestate_get_visual(gameState)
        inputPosition = cache.inputPosition
        itemPreviewFrame = cache.itemPreviewFrame
        itemPreviewAnimation = cache.itemPreviewAnimation
        itemDescriptionView = cache.itemDescriptionView
        if itemPreviewAnimation is not None:
            itemPreviewAnimation["stop"]()
            view_remove_child(itemPreviewFrame, itemPreviewAnimation)
            itemPreviewAnimation = None
        if inputPosition < -1:
            inputPosition = -1
        if inputPosition >= len(cache.shopItems):
            inputPosition = len(cache.shopItems) - 1
        if inputPosition != -1:
            shopItem = cache.shopItems[inputPosition]
            itemName, itemDescription, itemSprite = __resolve_shop_item(gameState, shopItem)
            itemPreviewAnimation = visual_show_splash(visual, itemSprite, parent=itemPreviewFrame)
            itemPreviewAnimation["play"](60, True)
            itemDescriptionView["setContent"](f"ID: {inputPosition}\nNama: {itemName}\nHarga: {shopItem.cost}\n{itemDescription}")
        cache = namedtuple_with(cache,
            lastInputPosition=inputPosition,
            itemPreviewAnimation=itemPreviewAnimation,
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
        if position == min(len(cache.shopItems) + 1, tableMaxShown + 1):
            tableView["setSelection"](min(len(cache.shopItems), tableMaxShown))
            tableOffset = min(max(0, len(cache.shopItems) - tableMaxShown), tableOffset + 1)
            inputPosition = tableOffset + (min(len(cache.shopItems), tableMaxShown) - 1)
            cache = namedtuple_with(cache,
                tableOffset=tableOffset,
                inputPosition=inputPosition,
            )
            return "checkTableLoad", cache
        cache = namedtuple_with(cache,
            inputPosition=inputPosition
        )
        if action == "enter":
            return "buyDialog", cache
        return "updateItemView", cache
    if state == "buyDialog":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        buyDialogView = cache.buyDialogView
        tableView["selectable"](False)
        view_add_child(mainView["contentView"], buyDialogView)
        userMoney = user_get_current(gameState).money
        print, input, meta = cache.buyDialogConsole
        shopItem = cache.shopItems[cache.inputPosition]
        itemName = __resolve_shop_item(gameState, shopItem)[0]
        meta(action="clear")
        print(f"==== Beli '{itemName}' @ {shopItem.cost} ====")
        print("Masukkan jumlah yang ingin dibeli.")
        def onChange(v):
            meta(action="clearPrint")
            if v == "":
                print("Masukkan jumlah yang ingin dibeli.")
                return
            quantity = parse_int(v)
            if quantity is None or quantity <= 0:
                print("Jumlah yang dimasukkan tidak valid.")
                return
            subtotal = quantity * shopItem.cost
            print(f"Total harga: {quantity} * {shopItem.cost} = {subtotal}")
            if userMoney < subtotal:
                print(f"Uangmu tidak cukup.")
        quantity = input("Jumlah: ", f"Uangmu: {userMoney}", onChange=onChange)
        return "buyDialogConfirm", cache, quantity
    if state == "buyDialogConfirm":
        cache, quantity, *_ = args
        if quantity is None:
            return "buyDialogConfirmChoose", cache, None, "Batal"
        quantity = parse_int(quantity)
        if quantity is None or quantity <= 0:
            return "buyDialog", cache
        gameState = cache.gameState
        shopItem = cache.shopItems[cache.inputPosition]
        itemName = __resolve_shop_item(gameState, shopItem)[0]
        print, input, meta = cache.buyDialogConsole
        meta(action="clear")
        userMoney = user_get_current(gameState).money
        subtotal = quantity * shopItem.cost
        if userMoney < subtotal:
            print(f"Uangmu tidak cukup. ", end="")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "buyDialogConfirmChoose", cache, None, "Batal", selection
        meta("keySpeed", 120)
        print(f"OWCA mu saat ini terdapat {userMoney}. ", end="")
        print(f"Kamu akan membeli '{itemName}' dengan harga satuan {shopItem.cost} sebanyak {quantity} dengan subtotal {subtotal}. ", end="")
        print(f"Di akhir transaksi OWCA mu akan tersisa {userMoney - subtotal}.")
        input("Konfirmasi", selectable=True)
        input("Batal", selectable=True)
        selection = meta(action="select")
        return "buyDialogConfirmChoose", cache, quantity, selection
    if state == "buyDialogConfirmChoose":
        cache, quantity, selection, *_ = args
        print, input, meta = cache.buyDialogConsole
        meta("keySpeed", -1)
        if selection is None:
            return "buyDialog", cache
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        buyDialogView = cache.buyDialogView
        view_remove_child(mainView["contentView"], buyDialogView)
        tableView["selectable"](True)
        if selection == "Batal":
            return "updateItemView", cache
        shopItem = cache.shopItems[cache.inputPosition]
        currentUser = user_get_current(gameState)
        userMoney = currentUser.money - quantity * shopItem.cost
        currentUser = user_set(gameState, currentUser.id, namedtuple_with(currentUser, money=userMoney))
        if shopItem.referenceType == "monster":
            monsterType = monster_get(gameState, shopItem.referenceId)
            for _ in range(quantity):
                newMonster = inventory_monster_new(gameState)
                newMonster = inventory_monster_new(gameState, newMonster.id, namedtuple_with(newMonster,
                    ownerId=currentUser.id,
                    referenceId=monsterType.id,
                    name=monsterType.name,
                    experiencePoints=0,
                    healthPoints=monsterType.healthPoints,
                    attackPower=monsterType.attackPower,
                    defensePower=monsterType.defensePower,
                    activePotions=[]
                ))
        if shopItem.referenceType == "item":
            itemType = potion_get(gameState, shopItem.referenceId)
            userItems = inventory_item_get_user_items(gameState, currentUser.id)
            userItem = array_find(userItems, lambda i, *_: i.referenceId == itemType.id)
            if userItem is None:
                userItem = inventory_item_new(gameState)
                userItem = inventory_item_set(gameState, userItem.id, namedtuple_with(userItem,
                    ownerId=currentUser.id,
                    referenceId=itemType.id,
                    quantity=quantity
                ))
            else:
                userItem = inventory_item_set(gameState, userItem.id, namedtuple_with(userItem,
                    quantity=userItem.quantity + quantity
                ))
        return "updateItemView", cache
    return SuspendableExhausted

def __resolve_shop_item(gameState: GameState, shopItem: ShopSchemaType):
    if shopItem.referenceType == "item":
        potion = potion_get(gameState, shopItem.referenceId)
        description = f"Deskripsi: {potion.description}"
        return (potion.name, description, potion.sprite)
    if shopItem.referenceType == "monster":
        monster = monster_get(gameState, shopItem.referenceId)
        description = f"Family: {monster.family} Level: {monster.level}\nATK: {monster.attackPower}     DEF: {monster.defensePower}\nDeskripsi: {monster.description}"
        return (monster.name, description, monster.spriteFront)
