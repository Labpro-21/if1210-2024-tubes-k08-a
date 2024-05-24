from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.monster import *
from game.potion import *
from game.user import *
from game.inventory import *
from game.database import *
from .menu import _menu_show_loading_splash
from typing import NamedTuple
from os import path

__MenuShopManagementCache = NamedTuple("MenuShopManagementCache", [
    ("gameState", GameState), # expect not changed
    ("parent", View), # expect not changed
    ("abortSignal", AbortSignal), # expect not changed
    ("monsterTypes", list[MonsterSchemaType]),
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

def _menu_show_monster_management(state, args):
    cache: __MenuShopManagementCache = None
    tableMaxShown = 10
    if state is SuspendableInitial:
        gameState, parent, abortSignal = args
        monsterTypes = monster_get_all_monsters(gameState)
        cache = __MenuShopManagementCache(
            gameState=gameState,
            parent=parent,
            abortSignal=abortSignal,
            monsterTypes=monsterTypes,
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

        mainView = visual_show_simple_dialog(visual, "MONSTER MANAGEMENT", "",
            x=pos_from_center(), y=pos_from_center(),
            width=dim_from_factor(0.8), height=dim_from_absolute(3 + 2 * (2 + tableMaxShown) + 2 + 2 + 2),
            parent=cache.parent)
        
        tableView = visual_show_table(visual, 
            [
                ("No.", dim_from_absolute(5), "Center"), 
                ("Family", dim_sub(dim_from_factor(0.2), dim_from_absolute(2)), "Right", (1, 0, 1, 0)), 
                ("Nama", dim_sub(dim_from_factor(0.3), dim_from_absolute(4)), "Left", (1, 0, 1, 0)), 
                ("Level", dim_from_factor(0.125), "Center"),
                ("HP", dim_from_factor(0.125), "Center"),
                ("ATK", dim_from_factor(0.125), "Center"),
                ("DEF", dim_from_factor(0.125), "Center")],
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
            hasTitle=True, inputBoxOffset=4)
    
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
            loadItems = array_slice(cache.monsterTypes, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: i.spriteFront)
            loadItemSprites2 = array_map(loadItemSprites2, lambda s, *_: (f"sprite {s}", s))
            loadItemSprites = dict_set(loadItemSprites, loadItemSprites2)
            cache = namedtuple_with(cache,
                tableLoadIndices=[*cache.tableLoadIndices, tableLoadIndex]
            )
        if not array_includes(cache.tableLoadIndices, tableBeforeLoadIndex):
            startIndex = tableBeforeLoadIndex * tableMaxShown
            endIndex = startIndex + tableMaxShown
            loadItems = array_slice(cache.monsterTypes, startIndex, endIndex)
            loadItemSprites2 = array_map(loadItems, lambda i, *_: i.spriteFront)
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
        itemRows = array_slice(cache.monsterTypes, startIndex, endIndex)
        def getRowFor(i: int, monsterType: MonsterSchemaType):
            return [f"{startIndex + i + 1}", monsterType.family, monsterType.name, f"{monsterType.level}", f"{monsterType.healthPoints}", f"{monsterType.attackPower}", f"{monsterType.defensePower}"]
        itemRows = array_map(itemRows, lambda it, i, *_: getRowFor(i, it))
        if len(itemRows) < tableMaxShown:
            array_push(itemRows, ["+++", "++++++", "++++++", "++++++", "++++++", "++++++", "++++++"])
        tableView["updateRows"]([
            ["▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲", "▲▲▲▲▲▲"],
            *itemRows,
            ["▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼", "▼▼▼▼▼▼"],
        ])
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
        if inputPosition >= len(cache.monsterTypes) + 1:
            inputPosition = len(cache.monsterTypes)
        if inputPosition != -1 and inputPosition != len(cache.monsterTypes):
            monsterType = cache.monsterTypes[inputPosition]
            itemPreviewAnimation = visual_show_splash(visual, monsterType.spriteFront, parent=itemPreviewFrame)
            itemPreviewAnimation["play"](60, True)
            description = f"ID: {inputPosition}\n"
            description += f"Family: {monsterType.family}\n"
            description += f"Nama: {monsterType.name}\n"
            description += f"Level: {monsterType.level}\n"
            description += f"HP: {monsterType.healthPoints}\n"
            description += f"ATK: {monsterType.attackPower}\n"
            description += f"DEF: {monsterType.defensePower}\n"
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
            tableView["setSelection"](min(len(cache.monsterTypes) + 1, tableMaxShown))
            cache = namedtuple_with(cache,
                tableOffset=max(0, len(cache.monsterTypes) - tableMaxShown + 1),
                inputPosition=len(cache.monsterTypes),
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
        if position == min(len(cache.monsterTypes) + 2, tableMaxShown + 1):
            tableView["setSelection"](min(len(cache.monsterTypes) + 1, tableMaxShown))
            tableOffset = min(max(0, len(cache.monsterTypes) - tableMaxShown + 1), tableOffset + 1)
            inputPosition = tableOffset + (min(len(cache.monsterTypes) + 1, tableMaxShown) - 1)
            cache = namedtuple_with(cache,
                tableOffset=tableOffset,
                inputPosition=inputPosition,
            )
            return "checkTableLoad", cache
        cache = namedtuple_with(cache,
            inputPosition=inputPosition
        )
        if action == "enter":
            if inputPosition == len(cache.monsterTypes):
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
        print("Masukkan family, nama, level, health points, attack power, dan defense power.")
        lastFamily = None
        lastName = None
        lastLevel = None
        lastHealthPoints = None
        lastAttackPower = None
        lastDefensePower = None
        def onChange(family = None, name = None, level = None, healthPoints = None, attackPower = None, defensePower = None):
            nonlocal lastFamily, lastName, lastLevel, lastHealthPoints, lastAttackPower, lastDefensePower
            meta(action="clearPrint")
            if family is not None:
                lastFamily = family
            if name is not None:
                lastName = name
            if level is not None:
                lastLevel = level
            if healthPoints is not None:
                lastHealthPoints = healthPoints
            if attackPower is not None:
                lastAttackPower = attackPower
            if defensePower is not None:
                lastDefensePower = defensePower
            emptyFields = []
            descriptions = []
            if lastFamily is None or lastFamily == "":
                array_push(emptyFields, "family")
            else:
                array_push(descriptions, f"Family: {lastFamily}")
            if lastName is None or lastName == "":
                array_push(emptyFields, "nama")
            else:
                # THIS IS A HACK TO CONFORM THE RULES. Name cannot be duplicate
                if array_some(cache.monsterTypes, lambda m, *_: m.name == lastName):
                    array_push(descriptions, "Nama sudah terdaftar!")
                else:
                    array_push(descriptions, f"Nama: {lastName}")
            parsedLevel = None
            if level is None or level == "":
                array_push(emptyFields, "level")
            else:
                parsedLevel = parse_int(level)
                if parsedLevel is None or parsedLevel < 0:
                    array_push(descriptions, "Level tidak valid.")
                else:
                    array_push(descriptions, f"Level: {parsedLevel}")
            if lastFamily is not None and parsedLevel is not None:
                if array_some(cache.monsterTypes, lambda m, *_: m.family == lastFamily and m.level == parsedLevel):
                    array_push(descriptions, f"Monster dengan family dan level ini telah ada!")
            if healthPoints is None or healthPoints == "":
                array_push(emptyFields, "health points")
            else:
                parsedHealthPoints = parse_int(healthPoints)
                if parsedHealthPoints is None or parsedHealthPoints < 0:
                    array_push(descriptions, "Health points tidak valid.")
                else:
                    array_push(descriptions, f"HP: {parsedHealthPoints}")
            if attackPower is None or attackPower == "":
                array_push(emptyFields, "attack power")
            else:
                parsedAttackPower = parse_int(attackPower)
                if parsedAttackPower is None or parsedAttackPower < 0:
                    array_push(descriptions, "Attack power tidak valid.")
                else:
                    array_push(descriptions, f"ATK: {parsedAttackPower}")
            if defensePower is None or defensePower == "":
                array_push(emptyFields, "defense power")
            else:
                parsedDefensePower = parse_int(defensePower)
                # THIS IS A HACK TO CONFORM THE RULES. Defense power range is from 0 to 50
                if parsedDefensePower is None or parsedDefensePower < 0 or parsedDefensePower > 50:
                    array_push(descriptions, "Defense power tidak valid.")
                else:
                    array_push(descriptions, f"DEF: {parsedDefensePower}")
            emptyFieldsStr = None
            if len(emptyFields) >= 3:
                emptyFieldsStr = f"{array_join(array_slice(emptyFields, 0, len(emptyFields) - 1), ', ')}, dan {emptyFields[len(emptyFields) - 1]}."
            if len(emptyFields) == 2:
                emptyFieldsStr = f"{emptyFields[0]} dan {emptyFields[1]}."
            if len(emptyFields) == 1:
                emptyFieldsStr = f"{emptyFields[0]}."
            if emptyFieldsStr is not None:
                print(f"Masukkan {emptyFieldsStr}")
            for description in descriptions:
                print(description)
        monsterFamily = input("Family: ", onChange=lambda v: onChange(family=v))
        monsterName = input("Nama: ", onChange=lambda v: onChange(name=v))
        monsterLevel = input("Level: ", onChange=lambda v: onChange(level=v))
        monsterHealthPoints = input("HP: ", onChange=lambda v: onChange(healthPoints=v))
        monsterAttackPower = input("ATK: ", onChange=lambda v: onChange(attackPower=v))
        monsterDefensePower = input("DEF: ", onChange=lambda v: onChange(defensePower=v))
        return "actionAddDialogChooseInput", cache, monsterFamily, monsterName, monsterLevel, monsterHealthPoints, monsterAttackPower, monsterDefensePower
    if state == "actionAddDialogChooseInput":
        cache, monsterFamily, monsterName, monsterLevel, monsterHealthPoints, monsterAttackPower, monsterDefensePower, *_ = args
        if monsterFamily is None or monsterName is None or monsterLevel is None or monsterHealthPoints is None or monsterAttackPower is None or monsterDefensePower is None:
            return "closeActionDialog", cache
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        monsterLevel = parse_int(monsterLevel)
        monsterHealthPoints = parse_int(monsterHealthPoints)
        monsterAttackPower = parse_int(monsterAttackPower)
        monsterDefensePower = parse_int(monsterDefensePower)
        errors = []
        if monsterLevel is None or monsterLevel < 0:
            array_push(errors, "Level tidak valid.")
        elif array_some(cache.monsterTypes, lambda m, *_: m.family == monsterFamily and m.level == monsterLevel):
            array_push(errors, f"Monster dengan family dan level ini telah ada!")
        if monsterHealthPoints is None or monsterHealthPoints < 0:
            array_push(errors, "Health points tidak valid.")
        if monsterAttackPower is None or monsterAttackPower < 0:
            array_push(errors, "Attack power tidak valid.")
        # THIS IS A HACK TO CONFORM THE RULES. Defense power range is from 0 to 50
        if monsterDefensePower is None or monsterDefensePower < 0 or monsterDefensePower > 50:
            array_push(errors, "Defense power tidak valid.")
        meta(action="clear")
        if len(errors) > 0:
            for error in errors:
                print(error)
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionAddDialog", cache, selection
        monsterType = monster_new(gameState)
        monsterType = monster_set(gameState, monsterType.id, namedtuple_with(monsterType,
            name=monsterName,
            description="",
            family=monsterFamily,
            level=monsterLevel,
            healthPoints=monsterHealthPoints,
            attackPower=monsterAttackPower,
            defensePower=monsterDefensePower,
            spriteDefault="monsters/bulbasaur.png.txt",
            spriteFront="monsters/bulbasaur_normal.gif.txt",
            spriteBack="monsters/bulbasaur_back.gif.txt",
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
        monsterType = cache.monsterTypes[cache.inputPosition]
        meta(action="clear")
        print(f"==== Edit '{monsterType.name}' ====")
        input("Ganti Nama", selectable=True)
        input("Ganti HP", selectable=True)
        input("Ganti ATK", selectable=True)
        input("Ganti DEF", selectable=True)
        input("Ganti Sprite", selectable=True)
        selection = meta(action="select")
        return "actionDialogChoose", cache, selection
    if state == "actionDialogChoose":
        cache, selection, *_ = args
        if selection is None:
            return "closeActionDialog", cache
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        if selection == "Ganti Nama":
            meta(action="clear")
            print("Masukkan nama yang ingin diganti.")
            def onChange(v):
                meta(action="clearPrint")
                if v == "":
                    print("Masukkan nama yang ingin diganti.")
                    return
                # THIS IS A HACK TO CONFORM THE RULES. Name cannot be duplicate
                if array_some(cache.monsterTypes, lambda m, *_: m.name == v):
                    print("Nama sudah terdaftar!")
                    return
                print(f"Nama akan diganti menjadi {v}")
            monsterName = input("Nama: ", onChange=onChange)
            return "actionDialogChangeName", cache, monsterName
        if selection == "Ganti HP":
            meta(action="clear")
            print("Masukkan health points yang ingin diganti.")
            def onChange(v):
                meta(action="clearPrint")
                if v == "":
                    print("Masukkan health points yang ingin diganti.")
                    return
                healthPoints = parse_int(v)
                if healthPoints is None or healthPoints < 0:
                    print("Health points yang dimasukkan tidak valid.")
                    return
                print(f"Health points akan diganti menjadi {healthPoints}")
            monsterHealthPoints = input("HP: ", onChange=onChange)
            return "actionDialogChangeHealthPoints", cache, monsterHealthPoints
        if selection == "Ganti ATK":
            meta(action="clear")
            print("Masukkan attack power yang ingin diganti.")
            def onChange(v):
                meta(action="clearPrint")
                if v == "":
                    print("Masukkan attack power yang ingin diganti.")
                    return
                attackPower = parse_int(v)
                if attackPower is None or attackPower < 0:
                    print("Attack power yang dimasukkan tidak valid.")
                    return
                print(f"Attack power akan diganti menjadi {attackPower}")
            monsterAttackPower = input("ATK: ", onChange=onChange)
            return "actionDialogChangeAttackPower", cache, monsterAttackPower
        if selection == "Ganti DEF":
            meta(action="clear")
            print("Masukkan defense power yang ingin diganti.")
            def onChange(v):
                meta(action="clearPrint")
                if v == "":
                    print("Masukkan defense power yang ingin diganti.")
                    return
                defensePower = parse_int(v)
                # THIS IS A HACK TO CONFORM THE RULES. Defense power range is from 0 to 50
                if defensePower is None or defensePower < 0 or defensePower > 0:
                    print("Defense power yang dimasukkan tidak valid.")
                    return
                print(f"Defense power akan diganti menjadi {defensePower}")
            monsterAttackPower = input("DEF: ", onChange=onChange)
            return "actionDialogChangeDefensePower", cache, monsterAttackPower
        if selection == "Ganti Sprite":
            visual = gamestate_get_visual(gameState)
            directory = visual_get_directory(visual)
            meta(action="clear")
            print("Masukkan sprite yang ingin diganti.")
            def onChange(v):
                meta(action="clearPrint")
                if v == "":
                    print("Masukkan sprite yang ingin diganti.")
                    return
                defaultSprite = path.join(directory, v + ".png.txt")
                frontSprite = path.join(directory, v + "_normal.gif.txt")
                backSprite = path.join(directory, v + "_back.gif.txt")
                errors = []
                if not path.exists(defaultSprite):
                    array_push(errors, f"File {defaultSprite} tidak ada!")
                if not path.exists(frontSprite):
                    array_push(errors, f"File {frontSprite} tidak ada!")
                if not path.exists(backSprite):
                    array_push(errors, f"File {backSprite} tidak ada!")
                if len(errors) > 0:
                    for error in errors:
                        print(error)
                    return
                print(f"Sprite akan diganti menjadi {v}")
            monsterSprite = input("Sprite: ", onChange=onChange)
            return "actionDialogChangeSprite", cache, monsterSprite
    if state == "actionDialogChangeName":
        cache, monsterName, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        if monsterName is None:
            return "actionDialog", cache
        # THIS IS A HACK TO CONFORM THE RULES. Name cannot be duplicate
        if array_some(cache.monsterTypes, lambda m, *_: m.name == monsterName):
            print("Nama sudah terdaftar!")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionDialogChoose", cache, "Ganti Nama", selection
        monsterType = cache.monsterTypes[cache.inputPosition]
        monsterType = monster_set(gameState, monsterType.id, namedtuple_with(monsterType,
            name=monsterName
        ))
        return "closeActionDialog", cache
    if state == "actionDialogChangeSprite":
        cache, monsterSprite, *_ = args
        gameState = cache.gameState
        visual = gamestate_get_visual(gameState)
        directory = visual_get_directory(visual)
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        if monsterSprite is None:
            return "actionDialog", cache
        defaultSprite = path.join(directory, monsterSprite + ".png.txt")
        frontSprite = path.join(directory, monsterSprite + "_normal.gif.txt")
        backSprite = path.join(directory, monsterSprite + "_back.gif.txt")
        errors = []
        if not path.exists(defaultSprite):
            array_push(errors, f"File {defaultSprite} tidak ada!")
        if not path.exists(frontSprite):
            array_push(errors, f"File {frontSprite} tidak ada!")
        if not path.exists(backSprite):
            array_push(errors, f"File {backSprite} tidak ada!")
        if len(errors) > 0:
            for error in errors:
                print(error)
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionDialogChoose", cache, "Ganti Sprite", selection
        monsterType = cache.monsterTypes[cache.inputPosition]
        monsterType = monster_set(gameState, monsterType.id, namedtuple_with(monsterType,
            spriteDefault=monsterSprite + ".png.txt",
            spriteFront=monsterSprite + "_normal.gif.txt",
            spriteBack=monsterSprite + "_back.gif.txt",
        ))
        cache = namedtuple_with(cache,
            tableLoadIndices=[-1], # Force reload all sprites
        )
        return "closeActionDialog", cache
    if state == "actionDialogChangeHealthPoints":
        cache, monsterHealthPoints, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        if monsterHealthPoints is None:
            return "actionDialog", cache
        monsterHealthPoints = parse_int(monsterHealthPoints)
        if monsterHealthPoints is None or monsterHealthPoints < 0:
            print("Health points yang dimasukkan tidak valid.")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionDialogChoose", cache, "Ganti HP", selection
        monsterType = cache.monsterTypes[cache.inputPosition]
        monsterType = monster_set(gameState, monsterType.id, namedtuple_with(monsterType,
            healthPoints=monsterHealthPoints
        ))
        return "closeActionDialog", cache
    if state == "actionDialogChangeAttackPower":
        cache, monsterAttackPower, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        if monsterAttackPower is None:
            return "actionDialog", cache
        monsterAttackPower = parse_int(monsterAttackPower)
        if monsterAttackPower is None or monsterAttackPower < 0:
            print("Attack power yang dimasukkan tidak valid.")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionDialogChoose", cache, "Ganti ATK", selection
        monsterType = cache.monsterTypes[cache.inputPosition]
        monsterType = monster_set(gameState, monsterType.id, namedtuple_with(monsterType,
            attackPower=monsterAttackPower
        ))
        return "closeActionDialog", cache
    if state == "actionDialogChangeDefensePower":
        cache, monsterDefensePower, *_ = args
        gameState = cache.gameState
        print, input, meta = cache.actionDialogConsole
        meta(action="clear")
        if monsterDefensePower is None:
            return "actionDialog", cache
        monsterDefensePower = parse_int(monsterDefensePower)
        # THIS IS A HACK TO CONFORM THE RULES. Defense power range is from 0 to 50
        if monsterDefensePower is None or monsterDefensePower < 0 or monsterDefensePower > 50:
            print("Defense power yang dimasukkan tidak valid.")
            input("Lanjut", selectable=True)
            selection = meta(action="select")
            return "actionDialogChoose", cache, "Ganti DEF", selection
        monsterType = cache.monsterTypes[cache.inputPosition]
        monsterType = monster_set(gameState, monsterType.id, namedtuple_with(monsterType,
            defensePower=monsterDefensePower
        ))
        return "closeActionDialog", cache
    if state == "closeActionDialog":
        cache, *_ = args
        gameState = cache.gameState
        mainView = cache.mainView
        tableView = cache.tableView
        actionDialogView = cache.actionDialogView
        view_remove_child(mainView["contentView"], actionDialogView)
        tableView["selectable"](True)
        newMonsterTypes = monster_get_all_monsters(gameState)
        cache = namedtuple_with(cache,
            monsterTypes=newMonsterTypes,
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
