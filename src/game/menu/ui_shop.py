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
    ("tableLoadIndices", int),
])

def _menu_show_shop(state, args):
    cache: __MenuShopCache = None
    tableMaxShown = 10
    if state is SuspendableInitial:
        gameState, parent, abortSignal = args
        shopItems = shop_get_all_items(gameState)
        # THIS IS A HACK TO CONFORM THE RULES. Empty stock are still displayed.
        # shopItems = array_filter(shopItems, lambda s, *_: s.stock > 0)
        cache = __MenuShopCache(
            gameState=gameState,
            parent=parent,
            abortSignal=abortSignal,
            shopItems=shopItems,
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
            tableLoadIndices=[-1],
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
                ("Tipe", dim_sub(dim_from_factor(0.15), dim_from_absolute(2)), "Right", (1, 0, 1, 0)), 
                ("Nama", dim_sub(dim_from_factor(0.6), dim_from_absolute(4)), "Left", (1, 0, 1, 0)), 
                ("Stok", dim_sub(dim_from_factor(0.1), dim_from_absolute(1)), "Center"),
                ("Harga", dim_sub(dim_from_factor(0.15), dim_from_absolute(1)), "Center")],
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
            loadItems = array_slice(cache.shopItems, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: __resolve_shop_item(gameState, i)[2])
            loadItemSprites2 = array_map(loadItemSprites2, lambda s, *_: (f"sprite {s}", s))
            loadItemSprites = dict_set(loadItemSprites, loadItemSprites2)
            cache = namedtuple_with(cache,
                tableLoadIndices=[*cache.tableLoadIndices, tableLoadIndex]
            )
        if not array_includes(cache.tableLoadIndices, tableBeforeLoadIndex):
            startIndex = tableBeforeLoadIndex * tableMaxShown
            endIndex = startIndex + tableMaxShown
            loadItems = array_slice(cache.shopItems, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: __resolve_shop_item(gameState, i)[2])
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
        itemRows = array_slice(cache.shopItems, startIndex, endIndex)
        def getRowFor(i: int, shopItem: ShopSchemaType):
            resolvedItem = __resolve_shop_item(gameState, shopItem)
            return [f"{startIndex + i + 1}", shopItem.referenceType, resolvedItem[0], f"{shopItem.stock}", f"{shopItem.cost}"]
        itemRows = array_map(itemRows, lambda it, i, *_: getRowFor(i, it))
        tableView["updateRows"]([
            ["▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲"],
            *itemRows,
            ["▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼"],
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
            itemDescriptionView["setContent"]("")
        if inputPosition < -1:
            inputPosition = -1
        if inputPosition >= len(cache.shopItems):
            inputPosition = len(cache.shopItems) - 1
        if inputPosition != -1:
            shopItem = cache.shopItems[inputPosition]
            itemName, itemDescription, itemSprite = __resolve_shop_item(gameState, shopItem)
            itemPreviewAnimation = visual_show_splash(visual, itemSprite, parent=itemPreviewFrame)
            itemPreviewAnimation["play"](60, True)
            description = f"ID: {inputPosition}\n"
            description += f"Nama: {itemName}\n"
            description += f"Harga: {shopItem.cost} "
            description += f"Stok: {shopItem.stock}\n"
            description += itemDescription
            itemDescriptionView["setContent"](description)
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
            tableView["setSelection"](min(len(cache.shopItems), tableMaxShown))
            cache = namedtuple_with(cache,
                tableOffset=max(0, len(cache.shopItems) - tableMaxShown),
                inputPosition=len(cache.shopItems) - 1,
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
        currentUser = user_get_current(gameState)
        userMoney = currentUser.money
        print, input, meta = cache.buyDialogConsole
        shopItem = cache.shopItems[cache.inputPosition]
        itemName = __resolve_shop_item(gameState, shopItem)[0]
        meta(action="clear")
        print(f"==== Beli '{itemName}' @ {shopItem.cost} ====")
        if shopItem.stock <= 0:
            print("Waduh! Kayaknya stoknya lagi kosong. Mampir kapan-kapan lagi ya.")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "buyDialogConfirmChoose", cache, None, "Batal", selection
        # THIS IS A HACK TO CONFORM THE RULES. Apparently you cannot have two monsters with the same type? WHYY??
        if shopItem.referenceType == "monster":
            userMonsters = inventory_monster_get_user_monsters(gameState, currentUser.id)
            if array_some(userMonsters, lambda m, *_: m.referenceId == shopItem.referenceId):
                print("Kamu telah memiliki monster ini!")
                input("Lanjut", selectable=True)
                selection = meta(action="select")
                return "buyDialogConfirmChoose", cache, None, "Batal", selection
            # THIS IS A HACK TO CONFORM THE RULES. You can only have one for each monster types. Don't bother to show quantity dialog.
            return "buyDialogConfirm", cache, "1"
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
                print(f"Uangmu tidak cukup.", end=" ")
            if quantity > shopItem.stock:
                print(f"Stok di shop tidak cukup.", end=" ")
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
        if userMoney < subtotal or quantity > shopItem.stock:
            if userMoney < subtotal:
                print(f"Uangmu tidak cukup.", end=" ")
            if quantity > shopItem.stock:
                print(f"Stok di shop tidak cukup.", end=" ")
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
        shopItem = shop_set(gameState, shopItem.id, namedtuple_with(shopItem,
            stock=shopItem.stock - quantity
        ))
        currentUser = user_get_current(gameState)
        userMoney = currentUser.money - quantity * shopItem.cost
        currentUser = user_set(gameState, currentUser.id, namedtuple_with(currentUser, money=userMoney))
        if shopItem.referenceType == "monster":
            monsterType = monster_get(gameState, shopItem.referenceId)
            for _ in range(quantity):
                newMonster = inventory_monster_new(gameState)
                newMonster = inventory_monster_set(gameState, newMonster.id, namedtuple_with(newMonster,
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
        newShopItems = shop_get_all_items(gameState)
        # THIS IS A HACK TO CONFORM THE RULES. Empty stock are still displayed.
        # newShopItems = array_filter(newShopItems, lambda s, *_: s.stock > 0)
        if len(newShopItems) != len(cache.shopItems):
            return "reloadAll", cache
        cache = namedtuple_with(cache, 
            shopItems=newShopItems,
            lastTableOffset=-1,
            lastInputPosition=-1,
        )
        return "updateTableEntries", cache
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

def __resolve_shop_item(gameState: GameState, shopItem: ShopSchemaType):
    if shopItem.referenceType == "item":
        potion = potion_get(gameState, shopItem.referenceId)
        description = f"Deskripsi: {potion.description}"
        return (potion.name, description, potion.sprite)
    if shopItem.referenceType == "monster":
        monster = monster_get(gameState, shopItem.referenceId)
        description = f"Family: {monster.family} Level: {monster.level}\nATK: {monster.attackPower}     DEF: {monster.defensePower}\nDeskripsi: {monster.description}"
        return (monster.name, description, monster.spriteFront)
