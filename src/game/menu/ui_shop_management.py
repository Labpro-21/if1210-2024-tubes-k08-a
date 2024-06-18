from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.shop import *
from game.monster import *
from game.potion import *
from game.inventory import *
from game.database import *
from .menu import _menu_show_loading_splash
from typing import NamedTuple

__MenuShopManagementCache = NamedTuple("MenuShopManagementCache", [
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
    ("actionDialogView", View), # expect not changed
    ("actionDialogConsole", ConsoleMock), # expect not changed
    ("lastInputPosition", int),
    ("inputPosition", int),
    ("lastTableOffset", int),
    ("tableOffset", int),
    ("tableLoadIndices", list[int]),
])

def _menu_show_shop_management(state, args):
    cache: __MenuShopManagementCache = None
    tableMaxShown = 10
    if state is SuspendableInitial:
        gameState, parent, abortSignal = args
        shopItems = shop_get_all_items(gameState)
        cache = __MenuShopManagementCache(
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

        mainView = visual_show_simple_dialog(visual, "SHOP MANAGEMENT", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.8), height=dim_from_absolute(3 + 2 * (2 + tableMaxShown) + 2 + 2 + 2),
            parent=cache.parent)
        
        tableView = visual_show_table(visual, 
            [
                ("No.", dim_from_absolute(5), "Center"), 
                ("Tipe", dim_sub(dim_from_factor(0.15), dim_from_absolute(2)), "Right", (1, 0, 1, 0)), 
                ("Nama", dim_sub(dim_from_factor(0.6), dim_from_absolute(4)), "Left", (1, 0, 1, 0)), 
                ("Stok", dim_sub(dim_from_factor(0.1), dim_from_absolute(1)), "Center"),
                ("Harga", dim_sub(dim_from_factor(0.15), dim_from_absolute(1)), "Center")],
            [],
            x=pos_from_absolute(0), y=pos_from_absolute(0),
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
        
        actionDialogView = visual_show_simple_dialog(visual, "BELI", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.5), height=dim_from_factor(0.5),
            parent=dumpView)
        actionDialogConsole = visual_with_mock(visual, actionDialogView, 
            hasTitle=True, inputBoxOffset=3)
    
        cache = namedtuple_with(cache,
            mainView=mainView,
            tableView=tableView,
            itemView=itemView,
            itemPreviewFrame=itemPreviewFrame,
            itemPreviewAnimation=itemPreviewAnimation,
            itemDescriptionView=itemDescriptionView,
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
            loadItems = array_slice(cache.shopItems, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: __resolve_shop_management_item(gameState, i)[2])
            loadItemSprites2 = array_map(loadItemSprites2, lambda s, *_: (f"sprite {s}", s))
            loadItemSprites = dict_set(loadItemSprites, loadItemSprites2)
            cache = namedtuple_with(cache,
                tableLoadIndices=[*cache.tableLoadIndices, tableLoadIndex]
            )
        if not array_includes(cache.tableLoadIndices, tableBeforeLoadIndex):
            startIndex = tableBeforeLoadIndex * tableMaxShown
            endIndex = startIndex + tableMaxShown
            loadItems = array_slice(cache.shopItems, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: __resolve_shop_management_item(gameState, i)[2])
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
            resolvedItem = __resolve_shop_management_item(gameState, shopItem)
            return [f"{startIndex + i + 1}", shopItem.referenceType, resolvedItem[0], txtqty(shopItem.stock), txtcrcy(shopItem.cost)]
        itemRows = array_map(itemRows, lambda it, i, *_: getRowFor(i, it))
        if len(itemRows) < tableMaxShown:
            array_push(itemRows, scrlad(5))
        tableView["updateRows"]([scrlup(5), *itemRows, scrldw(5)])
        cache = namedtuple_with(cache,
            lastTableOffset=cache.tableOffset
        )
        return "updateItemView", cache
    if state == "updateItemView":
        cache, *_ = args
        gameState = cache.gameState
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
        if inputPosition >= len(cache.shopItems) + 1:
            inputPosition = len(cache.shopItems)
        if inputPosition != -1 and inputPosition != len(cache.shopItems):
            shopItem = cache.shopItems[inputPosition]
            itemName, itemDescription, itemSprite = __resolve_shop_management_item(gameState, shopItem)
            itemPreviewAnimation = visual_show_splash(visual, itemSprite, parent=itemPreviewFrame)
            itemPreviewAnimation["play"](60, True)
            description = txtkv("ID: ", inputPosition) + "\n"
            description += txtkv("Nama: ", itemName) + "\n"
            description += txtkv("Harga: ", txtcrcy(shopItem.cost)) + " "
            description += txtkv("Stok: ", txtqty(shopItem.stock)) + "\n"
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
                if event.code == "KeyA" and event.ctrlKey:
                    cleanup()
                    resolve((None, "addNew"))
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
            tableView["setSelection"](min(len(cache.shopItems) + 1, tableMaxShown))
            cache = namedtuple_with(cache,
                tableOffset=max(0, len(cache.shopItems) - tableMaxShown + 1),
                inputPosition=len(cache.shopItems),
            )
            return "checkTableLoad", cache
        if action == "addNew":
            return "actionAddDialog", cache
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
        if position == min(len(cache.shopItems) + 2, tableMaxShown + 1):
            tableView["setSelection"](min(len(cache.shopItems) + 1, tableMaxShown))
            tableOffset = min(max(0, len(cache.shopItems) - tableMaxShown + 1), tableOffset + 1)
            inputPosition = tableOffset + (min(len(cache.shopItems) + 1, tableMaxShown) - 1)
            cache = namedtuple_with(cache,
                tableOffset=tableOffset,
                inputPosition=inputPosition,
            )
            return "checkTableLoad", cache
        cache = namedtuple_with(cache,
            inputPosition=inputPosition
        )
        if action == "enter":
            if inputPosition == len(cache.shopItems):
                return "actionAddDialog", cache
            return "actionDialog", cache
        return "updateItemView", cache
    if state == "actionAddDialog":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        actionDialogView = cache.actionDialogView
        tableView["selectable"](False)
        view_add_child(mainView["contentView"], actionDialogView)
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        print(f"==== Tambah Baru ====")
        input("Monster", selectable=True)
        input("Item", selectable=True)
        selection = meta(action="select")
        return "actionAddDialogChoose", cache, selection
    if state == "actionAddDialogChoose":
        cache, selection, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        if selection is None:
            return "closeActionDialog", cache
        if selection == "Monster":
            meta(action="clear")
            print("Masukkan ID monster, stok, dan harga.")
            lastId = None
            lastStock = None
            lastCost = None
            def onChange(id = None, stock = None, cost = None):
                nonlocal lastId, lastStock, lastCost
                meta(action="clearPrint")
                if id is not None:
                    lastId = id
                if stock is not None:
                    lastStock = stock
                if cost is not None:
                    lastCost = cost
                emptyFields = []
                descriptions = []
                if lastId is None or lastId == "":
                    array_push(emptyFields, "ID monster")
                else:
                    parsedId = parse_int(lastId)
                    monsters = monster_get_all_monsters(gameState)
                    if parsedId is None or parsedId < 0 or parsedId >= len(monsters):
                        array_push(descriptions, "ID monster tidak valid.")
                    else:
                        monster = monsters[parsedId]
                        description = txtkv("Monster: ", monster.name) + " "
                        description = txtkv("F: ", monster.family) + " "
                        description += txtkv("L: ", monster.level) + " "
                        description += txtkv("HP: ", monster.healthPoints) + " "
                        description += txtkv("ATK: ", monster.attackPower) + " "
                        description += txtkv("DEF: ", monster.defensePower) + " "
                        array_push(descriptions, description)
                        existingShopItem = array_find(cache.shopItems, lambda i, *_: i.referenceType == "monster" and i.referenceId == parsedId)
                        if existingShopItem is not None:
                            array_push(descriptions, "Sudah terdapat item dengan id yang sama.")
                if lastStock is None or lastStock == "":
                    array_push(emptyFields, "stok")
                else:
                    parsedStock = parse_int(lastStock)
                    if parsedStock is None or parsedStock < 0:
                        array_push(descriptions, "Stok tidak valid.")
                    else:
                        array_push(descriptions, txtkv("Stok: ", parsedStock) + "")
                if lastCost is None or lastCost == "":
                    array_push(emptyFields, "harga")
                else:
                    parsedCost = parse_int(lastCost)
                    if parsedCost is None or parsedCost < 0:
                        array_push(descriptions, "Harga tidak valid.")
                    else:
                        array_push(descriptions, txtkv("Harga: ", parsedCost) + "")
                emptyFieldsStr = None
                if len(emptyFields) == 3:
                    emptyFieldsStr = f"{emptyFields[0]}, {emptyFields[1]}, dan {emptyFields[2]}."
                if len(emptyFields) == 2:
                    emptyFieldsStr = f"{emptyFields[0]} dan {emptyFields[1]}."
                if len(emptyFields) == 1:
                    emptyFieldsStr = f"{emptyFields[0]}."
                if emptyFieldsStr is not None:
                    print(f"Masukkan {emptyFieldsStr}")
                for description in descriptions:
                    print(description)
            monsterId = input("ID: ", onChange=lambda v: onChange(id=v))
            monsterStock = input("Stok: ", onChange=lambda v: onChange(stock=v))
            monsterCost = input("Harga: ", onChange=lambda v: onChange(cost=v))
            return "actionAddDialogChooseInput", cache, "monster", monsterId, monsterStock, monsterCost
        if selection == "Item":
            meta(action="clear")
            print("Masukkan ID item, stok, dan harga.")
            lastId = None
            lastStock = None
            lastCost = None
            def onChange(id = None, stock = None, cost = None):
                nonlocal lastId, lastStock, lastCost
                meta(action="clearPrint")
                if id is not None:
                    lastId = id
                if stock is not None:
                    lastStock = stock
                if cost is not None:
                    lastCost = cost
                emptyFields = []
                descriptions = []
                if lastId is None or lastId == "":
                    array_push(emptyFields, "ID item")
                else:
                    parsedId = parse_int(lastId)
                    potions = potion_get_all_potions(gameState)
                    if parsedId is None or parsedId < 0 or parsedId >= len(potions):
                        array_push(descriptions, "ID item tidak valid.")
                    else:
                        potion = potions[parsedId]
                        array_push(descriptions, txtkv("Item: ", potion.name) + "")
                        existingShopItem = array_find(cache.shopItems, lambda i, *_: i.referenceType == "item" and i.referenceId == parsedId)
                        if existingShopItem is not None:
                            array_push(descriptions, "Sudah terdapat item dengan id yang sama.")
                if lastStock is None or lastStock == "":
                    array_push(emptyFields, "stok")
                else:
                    parsedStock = parse_int(lastStock)
                    if parsedStock is None or parsedStock < 0:
                        array_push(descriptions, "Stok tidak valid.")
                    else:
                        array_push(descriptions, txtkv("Stok: ", parsedStock) + "")
                if lastCost is None or lastCost == "":
                    array_push(emptyFields, "harga")
                else:
                    parsedCost = parse_int(lastCost)
                    if parsedCost is None or parsedCost < 0:
                        array_push(descriptions, "Harga tidak valid.")
                    else:
                        array_push(descriptions, txtkv("Harga: ", parsedCost) + "")
                emptyFieldsStr = None
                if len(emptyFields) == 3:
                    emptyFieldsStr = f"{emptyFields[0]}, {emptyFields[1]}, dan {emptyFields[2]}."
                if len(emptyFields) == 2:
                    emptyFieldsStr = f"{emptyFields[0]} dan {emptyFields[1]}."
                if len(emptyFields) == 1:
                    emptyFieldsStr = f"{emptyFields[0]}."
                if emptyFieldsStr is not None:
                    print(f"Masukkan {emptyFieldsStr}")
                for description in descriptions:
                    print(description)
            itemId = input("ID: ", onChange=lambda v: onChange(id=v))
            itemStock = input("Stok: ", onChange=lambda v: onChange(stock=v))
            itemCost = input("Harga: ", onChange=lambda v: onChange(cost=v))
            return "actionAddDialogChooseInput", cache, "item", itemId, itemStock, itemCost
    if state == "actionAddDialogChooseInput":
        cache, itemReferenceType, itemReferencedId, itemStock, itemCost, *_ = args
        if itemReferencedId is None or itemStock is None or itemCost is None:
            return "closeActionDialog", cache
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        itemReferencedId = parse_int(itemReferencedId)
        itemStock = parse_int(itemStock)
        itemCost = parse_int(itemCost)
        errors = []
        itemName = None
        existingShopItem = None
        if itemReferenceType == "monster":
            monsters = monster_get_all_monsters(gameState)
            if itemReferencedId is None or itemReferencedId < 0 or itemReferencedId >= len(monsters):
                array_push(errors, "ID monster tidak valid.")
            else:
                itemName = monsters[itemReferencedId].name
                existingShopItem = array_find(cache.shopItems, lambda i, *_: i.referenceType == "monster" and i.referenceId == itemReferencedId)
        if itemReferenceType == "item":
            potions = potion_get_all_potions(gameState)
            if itemReferencedId is None or itemReferencedId < 0 or itemReferencedId >= len(potions):
                array_push(errors, "ID item tidak valid.")
            else:
                itemName = potions[itemReferencedId].name
                existingShopItem = array_find(cache.shopItems, lambda i, *_: i.referenceType == "item" and i.referenceId == itemReferencedId)
        if itemStock is None or itemStock < 0:
            array_push(errors, "Stok tidak valid.")
        if itemCost is None or itemCost < 0:
            array_push(errors, "Harga tidak valid.")
        if existingShopItem is not None:
            array_push(errors, "Sudah terdapat item dengan id yang sama.")
        meta(action="clear")
        if len(errors) > 0:
            for error in errors:
                print(error)
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionAddDialogChoose", cache, "Monster" if itemReferenceType == "monster" else "Item", selection
        shopItem = shop_new(gameState)
        shopItem = shop_set(gameState, shopItem.id, namedtuple_with(shopItem,
            referenceType=itemReferenceType,
            referenceId=itemReferencedId,
            stock=itemStock,
            cost=itemCost,
        ))
        return "reloadAll", cache
    if state == "actionDialog":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        actionDialogView = cache.actionDialogView
        tableView["selectable"](False)
        view_add_child(mainView["contentView"], actionDialogView)
        print, input, meta = cache.actionDialogConsole
        shopItem = cache.shopItems[cache.inputPosition]
        itemName = __resolve_shop_management_item(gameState, shopItem)[0]
        meta(action="clear")
        print(f"==== Edit {itemName} ====")
        input("Ganti Stok", selectable=True)
        input("Ganti Harga", selectable=True)
        input(txtdngr("Hapus"), selectable=True)
        selection = meta(action="select")
        return "actionDialogChoose", cache, selection
    if state == "actionDialogChoose":
        cache, selection, *_ = args
        if selection is None:
            return "closeActionDialog", cache
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        if selection == "Ganti Stok":
            meta(action="clear")
            print("Masukkan jumlah stok yang ingin diganti.")
            def onChange(v):
                meta(action="clearPrint")
                if v == "":
                    print("Masukkan jumlah stok yang ingin diganti.")
                    return
                quantity = parse_int(v)
                if quantity is None or quantity < 0:
                    print("Jumlah yang dimasukkan tidak valid.")
                    return
                print(f"Stok akan diganti menjadi {txtqty(quantity)}")
            quantity = input("Jumlah: ", onChange=onChange)
            return "actionDialogChangeStock", cache, quantity
        if selection == "Ganti Harga":
            meta(action="clear")
            print("Masukkan harga yang ingin diganti.")
            def onChange(v):
                meta(action="clearPrint")
                if v == "":
                    print("Masukkan harga yang ingin diganti.")
                    return
                cost = parse_int(v)
                if cost is None or cost < 0:
                    print("Harga yang dimasukkan tidak valid.")
                    return
                print(f"Harga akan diganti menjadi {txtcrcy(cost)}")
            cost = input("Harga: ", onChange=onChange)
            return "actionDialogChangeCost", cache, cost
        if selection == "Hapus":
            meta(action="clear")
            shopItem = cache.shopItems[cache.inputPosition]
            itemName = __resolve_shop_management_item(gameState, shopItem)[0]
            print(f"Yakin mau ngehapus item {itemName}?")
            input(txtdngr("Hapus"), selectable=True)
            input(txtcncl("Batal"), selectable=True)
            selection = meta(action="select")
            return "actionDialogRemove", cache, selection
    if state == "actionDialogChangeStock":
        cache, stock, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        if stock is None:
            return "actionDialog", cache
        stock = parse_int(stock)
        if stock is None or stock < 0:
            print("Jumlah stok yang dimasukkan tidak valid.")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionDialogChoose", cache, "Ganti Stok", selection
        shopItem = cache.shopItems[cache.inputPosition]
        shopItem = shop_set(gameState, shopItem.id, namedtuple_with(shopItem,
            stock=stock
        ))
        return "closeActionDialog", cache
    if state == "actionDialogChangeCost":
        cache, cost, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        if cost is None:
            return "actionDialog", cache
        cost = parse_int(cost)
        if cost is None or cost < 0:
            print("Harga yang dimasukkan tidak valid.")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionDialogChoose", cache, "Ganti Harga", selection
        shopItem = cache.shopItems[cache.inputPosition]
        shopItem = shop_set(gameState, shopItem.id, namedtuple_with(shopItem,
            cost=cost
        ))
        return "closeActionDialog", cache
    if state == "actionDialogRemove":
        cache, selection, *_ = args
        if selection is None:
            return "actionDialog", cache
        if selection == "Batal":
            return "closeActionDialog", cache
        # THIS IS A HACK TO CONFORM THE RULES. This is messy and illegal.
        gameState = cache.gameState
        shopItems = cache.shopItems
        for i in range(cache.inputPosition, len(shopItems) - 1):
            shop_set(gameState, i, namedtuple_with(shopItems[i + 1], id=i))
        shopDatabase = gamestate_get_shop_database(gameState)
        database_delete_entry_at(shopDatabase, len(shopItems) - 1)
        return "reloadAll", cache
    if state == "closeActionDialog":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        actionDialogView = cache.actionDialogView
        view_remove_child(mainView["contentView"], actionDialogView)
        tableView["selectable"](True)
        newShopItems = shop_get_all_items(gameState)
        cache = namedtuple_with(cache,
            shopItems=newShopItems,
            lastTableOffset=-1,
            lastInputPosition=-1,
        )
        return "checkTableLoad", cache
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

def __resolve_shop_management_item(gameState: GameState, shopItem: ShopSchemaType):
    if shopItem.referenceType == "item":
        potion = potion_get(gameState, shopItem.referenceId)
        name = ptncl(potion.name)
        description = txtkv("Deskripsi: ", potion.description) + ""
        return (name, description, potion.sprite)
    if shopItem.referenceType == "monster":
        monster = monster_get(gameState, shopItem.referenceId)
        name = smnstr(monster.name)
        description = txtkv("Family: ", monster.family) + " "
        description += txtkv("Level: ", monster.level) + "\n"
        description += txtkv("HP: ", monster.healthPoints) + "     "
        description += txtkv("ATK: ", monster.attackPower) + "     "
        description += txtkv("DEF: ", monster.defensePower) + "\n"
        description += txtkv("Deskripsi: ", monster.description) + ""
        return (name, description, monster.spriteFront)
