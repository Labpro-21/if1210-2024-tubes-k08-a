from utils.primordials import *
from utils.console import *
from utils.coroutines import *
from utils.csv import *
from utils.codec import *
from typing import TypedDict, Optional, Callable, Any, Union
import os
import time

_Visual = TypedDict("Visual",
    driver=Driver,
    toplevel=TopLevel,
    view=Optional[View],
    directory=str,
    splashes=dict[str, list[list[Rune]]]
)

__Text = Union[str, list[Union[str, Rune]]]

def _visual_new() -> _Visual:
    driver = driverstd_new()
    toplevel = toplevel_new(driver)
    visual: _Visual = dict(
        driver=driver,
        toplevel=toplevel,
        view=None,
        directory=None,
        splashes=dict()
    )
    driverstd_add_key_listener(driver, lambda e: __visual_on_key(visual, e))
    return visual
def _visual_get_driver(visual: _Visual) -> Driver:
    return visual["driver"]
def _visual_get_toplevel(visual: _Visual) -> TopLevel:
    return visual["toplevel"]
def _visual_get_view(visual: _Visual) -> View:
    return visual["view"]
def _visual_get_directory(visual: _Visual) -> str:
    return visual["directory"]
def _visual_set_view(visual: _Visual, view: View) -> None:
    toplevel = visual["toplevel"]
    if visual["view"] is not None:
        view_remove_child(toplevel, visual["view"])
    visual["view"] = view
    if view is None:
        return
    __visual_attach_key_handler(visual, view)
    view_add_child(toplevel, view)
def _visual_set_directory(visual: _Visual, directory: str) -> None:
    visual["directory"] = directory

def _visual_add_key_listener(visual: _Visual, view: View, callback: Callable[[KeyEvent], Any]) -> None:
    keyListeners = view["__key_listeners"]
    if array_includes(keyListeners, callback):
        return
    array_push(keyListeners, callback)
def _visual_remove_key_listener(visual: _Visual, view: View, callback: Callable[[KeyEvent], Any]) -> None:
    keyListeners = view["__key_listeners"]
    listenerIndex = array_index_of(keyListeners, callback)
    if listenerIndex == -1:
        return
    array_splice(keyListeners, listenerIndex, 1)

def __visual_attach_key_handler(visual: _Visual, view: View) -> None:
    keyListeners = None
    propagateHandler = None
    if keyListeners is None:
        keyListeners = []
        view["__key_listeners"] = keyListeners
    else:
        keyListeners = view["__key_listeners"]
    if propagateHandler is None:
        def propagateToSubviews(event: KeyEvent) -> None:
            subviews = view["subviews"]
            for subview in subviews:
                if "__key_listeners" not in subview:
                    continue
                subviewKeyListeners = subview["__key_listeners"]
                for subviewKeyListener in subviewKeyListeners:
                    subviewKeyListener(event)
        propagateHandler = propagateToSubviews
        view["__key_propagate_handle"] = propagateHandler
    else:
        propagateHandler = view["__key_propagate_handle"]
    if array_includes(keyListeners, propagateHandler):
        return
    array_push(keyListeners, propagateHandler)
def __visual_on_key(visual: _Visual, event: KeyEvent) -> None:
    view = visual["view"]
    if view is None:
        return
    keyListeners = view["__key_listeners"]
    for keyListener in keyListeners:
        keyListener(event)

def _visual_tick(visual: _Visual) -> None:
    driver = visual["driver"]
    driver_tick(driver)

def _visual_draw(visual: _Visual) -> None:
    driver = visual["driver"]
    toplevel = visual["toplevel"]
    view_mark_recompute_layout(toplevel)
    view_recompute_layout(toplevel)
    view_mark_recompute_display(toplevel)
    view_draw(toplevel)
    driver_draw(driver)

def _visual_load_splash(visual: _Visual, name: str, progress: Callable[[float], None] = None) -> Promise[list[list[Rune]]]:
    currentDirectory = visual["directory"]
    splashes = visual["splashes"]
    if name in splashes:
        if progress is not None:
            progress(1)
        return promise_resolved(splashes[name])
    path = os.path.join(currentDirectory, name)
    promise = promise_from_suspendable(__load_splash_suspendable, path, progress)
    def onResolved(splash: list[list[Rune]]):
        splashes[name] = splash
        return splash
    promise = promise_then(promise, onResolved)
    return promise

def _visual_show_frame_sequence(
        visual: _Visual, 
        frames: list[__Text], 
        parent: Optional[View] = None
    ) -> View:
    driver = visual["driver"]
    mainView = view_new(driver)
    view_set_x(mainView, pos_from_factor(0))
    view_set_y(mainView, pos_from_factor(0))
    view_set_width(mainView, dim_from_factor(1))
    view_set_height(mainView, dim_from_factor(1))
    textFormatter = view_get_text_formatter(mainView)
    text_formatter_set_wordwrap(textFormatter, False)
    text_formatter_set_horizontal_alignment(textFormatter, "Center")
    text_formatter_set_vertical_alignment(textFormatter, "Middle")
    
    currentFrame = -1
    compiledFrames = array_map(frames, lambda f, *_: __parse_colored_text(f)[0])
    def setFrame(index: int) -> bool:
        nonlocal currentFrame
        if index < 0 or index >= len(compiledFrames):
            return False
        currentFrame = index
        text_formatter_set_text(textFormatter, compiledFrames[index])
        return True
    def nextFrame() -> None:
        nonlocal currentFrame
        return setFrame(currentFrame + 1)
    def previousFrame() -> None:
        nonlocal currentFrame
        return setFrame(currentFrame - 1)
    handle = None
    def isAttached():
        currentView = mainView
        while currentView["superview"] is not None and currentView["superview"] is not visual["toplevel"]:
            currentView = currentView["superview"]
        return currentView["superview"] is visual["toplevel"]
    def play(fps: float = 60, loopFrame = False) -> None:
        nonlocal handle
        if handle is not None:
            stop()
        def loop():
            nonlocal handle
            if not isAttached():
                stop()
                return
            if nextFrame():
                return
            if not loopFrame:
                stop()
                return
            setFrame(0)
        handle = set_interval(loop, 1000 / fps)
    def stop() -> None:
        nonlocal handle
        if handle is None:
            return
        clear_interval(handle)
        handle = None
    mainView["setFrame"] = setFrame
    mainView["nextFrame"] = nextFrame
    mainView["previousFrame"] = previousFrame
    mainView["play"] = play
    mainView["stop"] = stop
    __visual_attach_key_handler(visual, mainView)
    if parent is not None:
        view_add_child(parent, mainView)
    else:
        _visual_set_view(visual, mainView)
    return mainView

def _visual_show_splash(
        visual: _Visual, 
        splash: str,
        parent: Optional[View] = None
    ) -> View:
    splashes = visual["splashes"]
    splash = splashes[splash]
    return _visual_show_frame_sequence(visual, splash, parent)

def _visual_show_simple_dialog(
        visual: _Visual,
        title: __Text = "",
        content: __Text = "",
        /,
        x: Pos = pos_from_center(),
        y: Pos = pos_from_center(),
        width: Dim = dim_from_factor(0.5),
        height: Dim = dim_from_factor(0.5),
        horizontalAlignment: TextHorizontalAlignment = "Left",
        verticalAlignment: TextVerticalAlignment = "Top",
        border: tuple = (1, 1, 1, 1),
        padding: tuple = (2, 1, 2, 1),
        parent: Optional[View] = None
    ) -> View:
    driver = visual["driver"]
    mainView = view_new(driver)
    view_set_x(mainView, x)
    view_set_y(mainView, y)
    view_set_width(mainView, width)
    view_set_height(mainView, height)
    adornment_set_thickness(view_get_border(mainView), Thickness(*border))
    adornment_set_thickness(view_get_padding(mainView), Thickness(*padding))

    titleView = None
    if title is not None:
        titleView = view_new(driver)
        view_add_child(mainView, titleView)
        view_set_x(titleView, pos_from_absolute(0))
        view_set_y(titleView, pos_from_absolute(0))
        view_set_width(titleView, dim_from_fill(0))
        view_set_height(titleView, dim_from_absolute(2))
        textFormatter = view_get_text_formatter(titleView)
        text_formatter_set_text(textFormatter, __parse_colored_text(title)[0])
        text_formatter_set_horizontal_alignment(textFormatter, "Center")
        text_formatter_set_vertical_alignment(textFormatter, "Middle")

    contentView = view_new(driver)
    view_add_child(mainView, contentView)
    view_set_x(contentView, pos_from_absolute(0))
    view_set_y(contentView, pos_from_absolute(2 if title is not None else 0))
    view_set_width(contentView, dim_from_fill(0))
    view_set_height(contentView, dim_from_fill(0))
    textFormatter = view_get_text_formatter(contentView)
    text_formatter_set_text(textFormatter, __parse_colored_text(content)[0])
    text_formatter_set_horizontal_alignment(textFormatter, horizontalAlignment)
    text_formatter_set_vertical_alignment(textFormatter, verticalAlignment)

    mainView["titleView"] = titleView
    mainView["contentView"] = contentView
    mainView["setTitle"] = lambda t: text_formatter_set_text(view_get_text_formatter(titleView), __parse_colored_text(t)[0])
    mainView["setContent"] = lambda t: text_formatter_set_text(view_get_text_formatter(contentView), __parse_colored_text(t)[0])
    __visual_attach_key_handler(visual, mainView)
    if parent is not None:
        view_add_child(parent, mainView)
    else:
        _visual_set_view(visual, mainView)
    return mainView

def _visual_with_mock(visual: _Visual, view: View, **kwargs) -> tuple[Callable[[__Text], None], Callable[[__Text], Promise[str]], Callable[[str, Any], None]]:
    driver = visual["driver"]
    setTitle = view["setTitle"]
    setContent = view["setContent"]
    lastDrawing: Optional[float] = None
    drawingOnCompletes: list[Callable[[], None]] = []
    contentLastAttribute = RuneAttribute_clear
    content: list[Rune] = []
    contentDrawnPosition = 0
    flagsStack: list[dict[str, Any]] = []
    flags = dict_with(
        dict(
            keySpeed=-1, # characters per second
            hasTitle=False,
            selectableWaitAfterContent=True,
            selectableClearAfterSelection=True,
            selectableAllowEscape=True,
            inputWaitAfterContent=True,
            inputAllowEscape=True,
        ),
        **kwargs
    )
    def doDraw():
        nonlocal lastDrawing, contentDrawnPosition
        now = __now()
        deltaTime = now - lastDrawing if lastDrawing is not None else 0
        lastDrawing = now
        if int(contentDrawnPosition) == len(content):
            lastDrawing = None
            for drawingOnComplete in array_splice(drawingOnCompletes, 0):
                drawingOnComplete()
            return
        keySpeed = flags["keySpeed"]
        advancePosition = keySpeed * deltaTime / 1000 if keySpeed != -1 else len(content) - contentDrawnPosition
        contentDrawnPosition += advancePosition
        contentDrawnPosition = min(contentDrawnPosition, len(content))
        drawnContent = array_slice(content, 0, int(contentDrawnPosition))
        setContent(drawnContent)
        set_timeout(doDraw, 15)
    def waitDrawComplete():
        if lastDrawing is None:
            return promise_resolved(None)
        def executor(resolve, _):
            array_push(drawingOnCompletes, lambda: resolve(None))
        return promise_new(executor)
    def recognizeTitle(text: list[Rune]) -> Optional[list[Rune]]:
        string = array_join(array_map(text, lambda r, *_: r.character), "")
        indexStart = string_index_of(string, "==== ")
        if indexStart == -1:
            return None
        indexStart += len("==== ")
        indexEnd = string_index_of(string, " ====", indexStart + 1)
        if indexEnd == -1:
            return None
        return array_slice(text, indexStart, indexEnd)
    selectableIndex = -1
    selectables: list[View] = []
    selectableDescription: View = None
    selectableListeners: list[Callable[[str], None]] = []
    lastSelectableIndex = -1
    lastSelectables: list[View] = []
    def newSelectable(message: __Text, description: __Text, /, id: str = None) -> None:
        nonlocal contentLastAttribute
        message, contentLastAttribute = __parse_colored_text(message, contentLastAttribute)
        if description is not None:
            description = __parse_colored_text(description, contentLastAttribute)[0]
        if id is None:
            id = array_join(array_map(message, lambda r, *_: r.character), "")
        selectable = view_new(driver)
        textFormatter = view_get_text_formatter(selectable)
        text_formatter_set_text(textFormatter, message)
        text_formatter_set_horizontal_alignment(textFormatter, "Center")
        text_formatter_set_vertical_alignment(textFormatter, "Middle")
        selectable["selectableId"] = id
        selectable["selectableMessage"] = message
        selectable["selectableDescription"] = description
        array_push(selectables, selectable)
        layoutSelectable()
        selectableChange()
    def clearSelectables():
        array_splice(selectables, 0)
        layoutSelectable()
        selectableChange()
    def layoutSelectable():
        nonlocal selectableIndex, lastSelectableIndex, selectableDescription
        removedSelectables = array_filter(lastSelectables, lambda s, *_: not array_includes(selectables, s))
        addedSelectables = array_filter(selectables, lambda s, *_: not array_includes(lastSelectables, s))
        for removedSelectable in removedSelectables:
            view_remove_child(view, removedSelectable)
            array_splice(lastSelectables, array_index_of(lastSelectables, removedSelectable), 1)
        for addedSelectable in addedSelectables:
            view_add_child(view, addedSelectable)
            array_push(lastSelectables, addedSelectable)
        if len(selectables) == 0:
            if selectableDescription is not None:
                view_remove_child(view, selectableDescription)
                selectableDescription = None
            selectableIndex = -1
            lastSelectableIndex = -1
            array_splice(lastSelectables, 0)
            _visual_remove_key_listener(visual, view, selectableOnKey)
            return
        if selectableDescription is None:
            selectableDescription = view_new(driver)
            view_set_x(selectableDescription, pos_from_absolute(0))
            view_set_y(selectableDescription, pos_from_end(1))
            view_set_width(selectableDescription, dim_from_fill(0))
            view_set_height(selectableDescription, dim_from_absolute(2))
            adornment_set_thickness(view_get_border(selectableDescription), Thickness(0, 1, 0, 0))
            _visual_add_key_listener(visual, view, selectableOnKey)
        for i in range(len(selectables)):
            selectable = selectables[i]
            view_set_x(selectable, pos_from_center())
            view_set_y(selectable, pos_add(pos_from_center(), pos_from_absolute(i - (len(selectables) // 2) + 2)))
            view_set_width(selectable, dim_from_fill(0))
            view_set_height(selectable, dim_from_absolute(1))
    def selectableChange():
        nonlocal selectableIndex, selectableDescription, lastSelectableIndex
        if selectableIndex < -1:
            selectableIndex = -1
        if selectableIndex >= len(selectables):
            selectableIndex = len(selectables) - 1
        if selectableIndex == lastSelectableIndex:
            return
        if lastSelectableIndex != -1:
            selectable = selectables[lastSelectableIndex]
            textFormatter = view_get_text_formatter(selectable)
            message = selectable["selectableMessage"]
            text_formatter_set_text(textFormatter, message)
        if selectableIndex != -1:
            selectable = selectables[selectableIndex]
            textFormatter = view_get_text_formatter(selectable)
            message = selectable["selectableMessage"]
            description = selectable["selectableDescription"]
            text_formatter_set_text(textFormatter, __reverse_background_foreground(message))
            if description is not None:
                descriptionTextFormatter = view_get_text_formatter(selectableDescription)
                text_formatter_set_text(descriptionTextFormatter, description)
                view_add_child(view, selectableDescription)
            else:
                view_remove_child(view, selectableDescription)
        else:
            view_remove_child(view, selectableDescription)
        lastSelectableIndex = selectableIndex
    def selectableOnKey(event: KeyEvent):
        nonlocal selectableIndex
        if len(selectables) == 0:
            return
        if event.key == "ControlESC":
            if not flags["selectableAllowEscape"]:
                return
            for selectableListener in selectableListeners:
                selectableListener(None)
            if flags["selectableClearAfterSelection"]:
                clearSelectables()
            return
        if event.key == "ControlCR" or event.key == "ControlLF":
            if selectableIndex == -1 or len(selectableListeners) == 0:
                return
            selectable = selectables[selectableIndex]
            selectableId = selectable["selectableId"]
            for selectableListener in selectableListeners:
                selectableListener(selectableId)
            if flags["selectableClearAfterSelection"]:
                clearSelectables()
            return
        if event.key == "Up":
            selectableIndex = max(0, selectableIndex - 1) if selectableIndex != -1 else len(selectables) - 1
            selectableChange()
            return
        if event.key == "Down":
            selectableIndex = min(len(selectables) - 1, selectableIndex + 1) if selectableIndex != -1 else 0
            selectableChange()
            return
    def print(message: __Text, *args, end: __Text = "\n", **kwargs) -> Any:
        nonlocal lastDrawing, contentLastAttribute
        additionalContent, contentLastAttribute = __parse_colored_text(message, contentLastAttribute)
        if flags["hasTitle"]:
            titleText = recognizeTitle(additionalContent)
            if titleText is not None:
                additionalContent = []
                setTitle(titleText)
                return
        array_push(content, *additionalContent)
        additionalContent, contentLastAttribute = __parse_colored_text(end, contentLastAttribute)
        array_push(content, *additionalContent)
        if lastDrawing is not None:
            return
        doDraw()
    inputParent: View = None
    inputDescription: View = None
    inputIndex = -1
    inputViews: list[View] = []
    lastInputIndex = -1
    lastInputViews: list[View] = []
    def newInput(message: __Text, description: __Text, /, renderer: Callable[[list[Rune]], list[Rune]] = None):
        nonlocal inputIndex, contentLastAttribute
        message, contentLastAttribute = __parse_colored_text(message, contentLastAttribute)
        if description is not None:
            description = __parse_colored_text(description, contentLastAttribute)[0]
        inputView = view_new(driver)
        textFormatter = view_get_text_formatter(inputView)
        text_formatter_set_text(textFormatter, message)
        inputView["inputDone"] = False
        inputView["inputMessage"] = message
        inputView["inputDescription"] = description
        inputView["inputAttribute"] = contentLastAttribute
        inputView["inputValue"] = ""
        inputView["inputSize"] = 20
        inputView["inputOffset"] = 0
        inputView["inputCursor"] = -1
        inputView["inputValueRenderer"] = renderer
        def update():
            message = array_slice(inputView["inputMessage"])
            done = inputView["inputDone"]
            attribute = inputView["inputAttribute"]
            value = inputView["inputValue"]
            size = inputView["inputSize"]
            offset = inputView["inputOffset"]
            cursor = inputView["inputCursor"]
            setCursorPosition(cursor)
            offset = inputView["inputOffset"]
            cursor = inputView["inputCursor"]
            renderer = inputView["inputValueRenderer"]
            value = __parse_colored_text(value, attribute)[0]
            if renderer is not None:
                value = renderer(value)
            array_push(value, Rune(" ", attribute)) # Space for cursor at the end
            if cursor != -1:
                value[cursor] = __reverse_background_foreground([value[cursor]])[0]
            value = array_slice(value, offset, offset + size)
            if not done:
                value = __reverse_background_foreground(value)
            array_push(message, *value)
            text_formatter_set_text(textFormatter, message)
        def setCursorPosition(cursor):
            size = inputView["inputSize"]
            offset = inputView["inputOffset"]
            cursor = max(-1, min(len(inputView["inputValue"]), cursor))
            if cursor <= offset:
                offset = cursor - 1 if cursor > 1 else 0
            if cursor >= offset + size:
                offset = cursor - size + 1
            inputView["inputOffset"] = offset
            inputView["inputCursor"] = cursor
        inputView["inputUpdate"] = update
        inputView["inputSetCursorPosition"] = setCursorPosition
        def executor(resolve, _):
            inputView["inputResolve"] = resolve
        promise = promise_new(executor)
        array_push(inputViews, inputView)
        if inputIndex == -1:
            inputIndex = len(inputViews) - 1
        layoutInput()
        inputChange()
        return promise
    def clearInputs():
        array_splice(inputViews, 0)
        layoutInput()
        inputChange()
    def layoutInput():
        nonlocal inputIndex, lastInputIndex, inputParent, inputDescription
        if len(inputViews) == 0:
            if inputParent is not None:
                view_remove_child(view, inputParent)
                inputParent = None
            if inputDescription is not None:
                view_remove_child(view, inputDescription)
                inputDescription = None
            lastInputIndex = -1
            inputIndex = -1
            array_splice(lastInputViews, 0)
            _visual_remove_key_listener(visual, view, inputOnKey)
            return
        if inputParent is None:
            inputParent = view_new(driver)
            view_set_x(inputParent, pos_from_center())
            view_set_y(inputParent, pos_add(pos_from_center(), pos_from_absolute(1)))
            view_set_width(inputParent, dim_from_factor(0.8))
            view_set_height(inputParent, dim_from_absolute(0))
            adornment_set_thickness(view_get_border(inputParent), Thickness(1, 1, 1, 1))
            view_add_child(view, inputParent)
            _visual_add_key_listener(visual, view, inputOnKey)
        if inputDescription is None:
            inputDescription = view_new(driver)
            view_set_x(inputDescription, pos_from_absolute(0))
            view_set_y(inputDescription, pos_from_end(1))
            view_set_width(inputDescription, dim_from_fill(0))
            view_set_height(inputDescription, dim_from_absolute(2))
            adornment_set_thickness(view_get_border(inputDescription), Thickness(0, 1, 0, 0))
        if len(lastInputViews) != len(inputViews):
            view_set_height(inputParent, dim_from_absolute(len(inputViews) + 2))
        removedInputViews = array_filter(lastInputViews, lambda s, *_: not array_includes(inputViews, s))
        addedInputViews = array_filter(inputViews, lambda s, *_: not array_includes(lastInputViews, s))
        for removedInputView in removedInputViews:
            view_remove_child(inputParent, removedInputView)
            array_splice(lastInputViews, array_index_of(lastInputViews, removedInputView), 1)
        for addedInputView in addedInputViews:
            view_add_child(inputParent, addedInputView)
            array_push(lastInputViews, addedInputView)
        for i in range(len(inputViews)):
            inputView = inputViews[i]
            view_set_x(inputView, pos_from_absolute(0))
            view_set_y(inputView, pos_from_absolute(i))
            view_set_width(inputView, dim_from_fill(0))
            view_set_height(inputView, dim_from_absolute(1))
    def inputChange():
        nonlocal inputIndex, inputDescription, lastInputIndex
        if inputIndex < -1:
            inputIndex = -1
        if inputIndex >= len(inputViews):
            inputIndex = len(inputViews) - 1
        if inputIndex == lastInputIndex:
            return
        if lastInputIndex != -1:
            inputView = inputViews[lastInputIndex]
            inputView["__inputCursor"] = inputView["inputCursor"]
            inputView["inputCursor"] = -1
            inputView["inputUpdate"]()
        if inputIndex != -1:
            inputView = inputViews[inputIndex]
            if "__inputCursor" in inputView:
                inputView["inputCursor"] = inputView["__inputCursor"]
                inputView["__inputCursor"] = None
            else:
                inputView["inputCursor"] = 0
            inputView["inputUpdate"]()
            description = inputView["inputDescription"]
            if description is not None:
                descriptionTextFormatter = view_get_text_formatter(inputDescription)
                text_formatter_set_text(descriptionTextFormatter, description)
                view_add_child(view, inputDescription)
            else:
                view_remove_child(view, inputDescription)
        else:
            view_remove_child(view, inputDescription)
        lastInputIndex = inputIndex
    def inputOnKey(event: KeyEvent):
        nonlocal inputIndex
        if len(inputViews) == 0:
            return
        def restoreRendererIfAvailable(inputCurrent):
            if "__inputValueRenderer" in inputCurrent and inputCurrent["__inputValueRenderer"] is not None:
                inputCurrent["inputValueRenderer"] = inputCurrent["__inputValueRenderer"]
                inputCurrent["__inputValueRenderer"] = None
                inputCurrent["inputUpdate"]()
        if event.key == "ControlESC":
            if not flags["inputAllowEscape"]:
                return
            if inputIndex == -1:
                return
            for inputView in inputViews:
                inputView["inputDone"] = True
                inputView["inputValue"] = ""
                inputView["inputUpdate"]()
                inputView["inputResolve"](None)
                restoreRendererIfAvailable(inputView)
            array_splice(inputViews, 0)
            layoutInput()
            inputChange()
            return
        if event.key == "ControlCR" or event.key == "ControlLF":
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            inputCurrent["inputDone"] = True
            inputCurrent["inputResolve"](inputCurrent["inputValue"])
            restoreRendererIfAvailable(inputCurrent)
            inputIndex = array_find_index(inputViews, lambda v, i, *_: not v["inputDone"] and i > inputIndex)
            if inputIndex == -1:
                inputIndex = array_find_index(inputViews, lambda v, i, *_: not v["inputDone"])
            inputChange()
            return
        if event.key == "Up":
            newInputIndex = -1
            if inputIndex == -1:
                newInputIndex = array_find_last_index(inputViews, lambda v, *_: not v["inputDone"])
            else:
                newInputIndex = array_find_index(inputViews, lambda v, i, *_: not v["inputDone"] and i < inputIndex)
            if newInputIndex == -1:
                return
            if inputIndex != -1:
                inputCurrent = inputViews[inputIndex]
                restoreRendererIfAvailable(inputCurrent)
            inputIndex = newInputIndex
            inputChange()
            return
        if event.key == "Down":
            newInputIndex = -1
            if inputIndex == -1:
                newInputIndex = array_find_index(inputViews, lambda v, *_: not v["inputDone"])
            else:
                newInputIndex = array_find_index(inputViews, lambda v, i, *_: not v["inputDone"] and i > inputIndex)
            if newInputIndex == -1:
                return
            if inputIndex != -1:
                inputCurrent = inputViews[inputIndex]
                restoreRendererIfAvailable(inputCurrent)
            inputIndex = newInputIndex
            inputChange()
            return
        if event.key == "Left":
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            inputCurrent["inputCursor"] = max(0, inputCurrent["inputCursor"] - 1)
            inputCurrent["inputUpdate"]()
            return
        if event.key == "Right":
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            inputCurrent["inputCursor"] = min(len(inputCurrent["inputValue"]), inputCurrent["inputCursor"] + 1)
            inputCurrent["inputUpdate"]()
            return
        if event.key == "Home" or event.key == "PageUp":
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            inputCurrent["inputCursor"] = 0
            inputCurrent["inputUpdate"]()
            return
        if event.key == "End" or event.key == "PageDown":
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            inputCurrent["inputCursor"] = len(inputCurrent["inputValue"])
            inputCurrent["inputUpdate"]()
            return
        if event.key == "ControlBS":
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            value = inputCurrent["inputValue"]
            cursor = inputCurrent["inputCursor"]
            valueBefore = array_slice(value, 0, cursor - 1)
            valueAfter = array_slice(value, cursor)
            inputCurrent["inputValue"] = valueBefore + valueAfter
            if inputCurrent["inputCursor"] > 0:
                inputCurrent["inputCursor"] -= 1
            inputCurrent["inputUpdate"]()
            return
        if event.code == "KeyA" and event.ctrlKey:
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            renderer = inputCurrent["inputValueRenderer"]
            if renderer is not None:
                inputCurrent["__inputValueRenderer"] = renderer
                inputCurrent["inputValueRenderer"] = None
                inputCurrent["inputUpdate"]()
            elif "__inputValueRenderer" in inputCurrent and inputCurrent["__inputValueRenderer"] is not None:
                inputCurrent["inputValueRenderer"] = inputCurrent["__inputValueRenderer"]
                inputCurrent["__inputValueRenderer"] = None
                inputCurrent["inputUpdate"]()
            return
        if len(event.key) == 1:
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            value = inputCurrent["inputValue"]
            cursor = inputCurrent["inputCursor"]
            valueBefore = array_slice(value, 0, cursor)
            valueAfter = array_slice(value, cursor)
            inputCurrent["inputValue"] = valueBefore + event.key + valueAfter
            inputCurrent["inputCursor"] += 1
            inputCurrent["inputUpdate"]()
            return
    def input(message: __Text, *args, **kwargs) -> Any:
        if "selectable" in kwargs and kwargs["selectable"]:
            del kwargs["selectable"]
            do = lambda *_: newSelectable(message, args[0] if len(args) > 0 else None, **kwargs)
            if flags["selectableWaitAfterContent"]:
                return promise_then(waitDrawComplete(), do)
            do()
            return
        do = lambda *_: newInput(message, args[0] if len(args) > 0 else None, **kwargs)
        if flags["inputWaitAfterContent"]:
            return promise_then(waitDrawComplete(), do)
        return do()
    def getRootView():
            currentView = view
            while currentView["superview"] is not None and currentView["superview"] is not visual["toplevel"]:
                currentView = currentView["superview"]
            return currentView
    def metaAction(action: str, kwargs: dict) -> Any:
        nonlocal contentLastAttribute
        if action == "getVisual":
            return visual
        if action == "getRootView":
            return getRootView()
        if action == "setAsCurrentView":
            _visual_set_view(visual, getRootView())
            return
        if action == "setAttribute":
            contentLastAttribute = kwargs["value"]
            return
        if action == "getAttribute":
            return contentLastAttribute
        if action == "pushFlags":
            array_push(flagsStack, dict_with(flags))
            return
        if action == "popFlags":
            lastFlag = array_pop(flagsStack)
            if lastFlag is not None:
                dict_clear(flags)
                dict_set(flags, lastFlag)
            return
        if action == "clear":
            array_splice(content, 0)
            drawnContentPosition = 0
            contentLastAttribute = RuneAttribute_clear
            clearSelectables()
            clearInputs()
            doDraw()
            return
        if action == "waitContent":
            return waitDrawComplete()
        if action == "clearSelectables":
            clearSelectables()
            return
        if action == "select":
            def executor(resolve, _):
                array_push(selectableListeners, lambda s: resolve(s))
            return promise_new(executor)
        if action == "clearInputs":
            clearInputs()
            return
        raise f"Unknown action {action}"
    def meta(*args, **kwargs) -> Any:
        nonlocal contentDrawnPosition, contentLastAttribute
        if len(args) == 2 and type(args[0]) is str:
            name = args[0]
            value = args[1]
            flags[name] = value
            return
        if len(args) == 1:
            name = args[0]
            return flags[name]
        if "action" in kwargs:
            action = kwargs["action"]
            return metaAction(action, kwargs)
    return (print, input, meta)

def _fg(r: Union[int, str] = None, g: int = None, b: int = None) -> str:
    if r is None and g is None and b is None:
        return "§q|"
    if type(r) is str:
        if string_starts_with(r, "#"):
            r = string_slice(r, 1)
        b = int(string_slice(r, 4, 6), 16)
        g = int(string_slice(r, 2, 4), 16)
        r = int(string_slice(r, 0, 2), 16)
    return f'§w{string_replace_all(base64_encode(chr(r) + chr(g) + chr(b)), "=", "")}|'
def _bg(r: Union[int, str] = None, g: int = None, b: int = None) -> str:
    if r is None and g is None and b is None:
        return "§a|"
    if type(r) is str:
        if string_starts_with(r, "#"):
            r = string_slice(r, 1)
        b = int(string_slice(r, 4, 6), 16)
        g = int(string_slice(r, 2, 4), 16)
        r = int(string_slice(r, 0, 2), 16)
    return f'§s{string_replace_all(base64_encode(chr(r) + chr(g) + chr(b)), "=", "")}|'
def _fbg(r: Union[int, str] = None, g: int = None, b: int = None) -> str:
    if r is None and g is None and b is None:
        return "§z|"
    if type(r) is str:
        if string_starts_with(r, "#"):
            r = string_slice(r, 1)
        b = int(string_slice(r, 4, 6), 16)
        g = int(string_slice(r, 2, 4), 16)
        r = int(string_slice(r, 0, 2), 16)
    return f'§x{string_replace_all(base64_encode(chr(r) + chr(g) + chr(b)), "=", "")}|'

def __now() -> float:
    return time.monotonic() * 1000
def __load_splash_suspendable(state, args):
    if state == SuspendableInitial:
        path, progress = args
        rawFrames = csv_read_from_file(path)
        rawFrames = array_map(rawFrames, lambda f, *_: array_join(f, "\n"))
        processedFrames = [[] for _ in range(len(rawFrames))]
        return 1, rawFrames, processedFrames, progress, 0, 0, RuneAttribute_clear
    if state == 1:
        rawFrames, processedFrames, progress, i, offset, lastAttribute = args
        rawFrame = rawFrames[i]
        if offset >= len(rawFrame):
            i += 1
            offset = 0
            if i >= len(rawFrames):
                return SuspendableReturn, processedFrames
            rawFrame = rawFrames[i]
        endOffset = min(len(rawFrame), offset + 12259)
        lastAttributeStart = string_last_index_of(rawFrame, "§", endOffset)
        if lastAttributeStart != -1:
            lastAttributeEnd = string_index_of(rawFrame, "|", lastAttributeStart + 1)
            if lastAttributeEnd != -1 and lastAttributeEnd + 1 > endOffset:
                endOffset = lastAttributeEnd + 1
        rawSection = string_slice(rawFrame, offset, endOffset)
        processedSection, lastAttribute = __parse_colored_text(rawSection, lastAttribute)
        array_push(processedFrames[i], *processedSection)
        if progress is not None:
            frameProgress = 1 / len(rawFrames)
            progress(i * frameProgress + endOffset / len(rawFrame) * frameProgress)
        return promise_from_wait(0, 1), rawFrames, processedFrames, progress, i, endOffset, lastAttribute
def __reverse_background_foreground(text: list[Rune]) -> list[Rune]:
    def reverseAttribute(attribute: RuneAttribute) -> RuneAttribute:
        newForeground = attribute.background
        newBackground = attribute.foreground
        if newForeground == None:
            newForeground = (0, 0, 0)
        if newBackground == None:
            newBackground = (255, 255, 255)
        return namedtuple_with(attribute, foreground=newForeground, background=newBackground)
    return array_map(text, lambda c, *_: Rune(c.character, reverseAttribute(c.attribute)))
def __parse_colored_text(text: __Text, lastAttribute: RuneAttribute = RuneAttribute_clear) -> tuple[list[Rune], RuneAttribute]:
    result: list[Rune] = []
    currentAttribute = lastAttribute
    if type(text) is list:
        for entry in text:
            if type(entry) is str:
                parsed, currentAttribute = __parse_colored_text(entry, currentAttribute)
                array_push(result, *parsed)
            else:
                currentAttribute = entry.attribute
                array_push(result, entry)
        return result, currentAttribute
    i = 0
    while i < len(text):
        if text[i] == "§":
            nextIndex = string_index_of(text, "|", i + 1)
            if nextIndex != -1:
                parameter = string_slice(text, i + 1, nextIndex)
                parsedParameter = __parse_parameter(parameter, currentAttribute)
                if parsedParameter is not None:
                    currentAttribute = parsedParameter
                    i = nextIndex + 1
                    continue
        array_push(result, Rune(text[i], currentAttribute))
        i += 1
    return result, currentAttribute
def __parse_parameter(parameter: str, lastAttribute: RuneAttribute) -> Optional[RuneAttribute]:
    newAttribute = lastAttribute
    commands = string_split(parameter, ",")
    for command in commands:
        if string_starts_with(command, "q"): # Foreground reset
            newAttribute = namedtuple_with(newAttribute, foreground=None)
        if string_starts_with(command, "w"): # Foreground RGB
            value = base64_decode(string_slice(command, 1))
            newForeground = (ord(value[0]), ord(value[1]), ord(value[2]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground)
        if string_starts_with(command, "e"): # Foreground RG
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _0=ord(value[0]), _1=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground)
        if string_starts_with(command, "r"): # Foreground GB
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _1=ord(value[0]), _2=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground)
        if string_starts_with(command, "t"): # Foreground BR
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _2=ord(value[0]), _0=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground)
        if string_starts_with(command, "y"): # Foreground R
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _0=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground)
        if string_starts_with(command, "u"): # Foreground G
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _1=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground)
        if string_starts_with(command, "i"): # Foreground B
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _2=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground)

        if string_starts_with(command, "a"): # Background reset
            newAttribute = namedtuple_with(newAttribute, background=None)
        if string_starts_with(command, "s"): # Background RGB
            value = base64_decode(string_slice(command, 1))
            newBackground = (ord(value[0]), ord(value[1]), ord(value[2]))
            newAttribute = namedtuple_with(newAttribute, background=newBackground)
        if string_starts_with(command, "d"): # Background RG
            value = base64_decode(string_slice(command, 1))
            oldBackground = newAttribute.background if newAttribute.background is not None else (0, 0, 0)
            newBackground = tuple_with(oldBackground, _0=ord(value[0]), _1=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, background=newBackground)
        if string_starts_with(command, "f"): # Background GB
            value = base64_decode(string_slice(command, 1))
            oldBackground = newAttribute.background if newAttribute.background is not None else (0, 0, 0)
            newBackground = tuple_with(oldBackground, _1=ord(value[0]), _2=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, background=newBackground)
        if string_starts_with(command, "g"): # Background BR
            value = base64_decode(string_slice(command, 1))
            oldBackground = newAttribute.background if newAttribute.background is not None else (0, 0, 0)
            newBackground = tuple_with(oldBackground, _2=ord(value[0]), _0=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, background=newBackground)
        if string_starts_with(command, "h"): # Background R
            value = base64_decode(string_slice(command, 1))
            oldBackground = newAttribute.background if newAttribute.background is not None else (0, 0, 0)
            newBackground = tuple_with(oldBackground, _0=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, background=newBackground)
        if string_starts_with(command, "j"): # Background G
            value = base64_decode(string_slice(command, 1))
            oldBackground = newAttribute.background if newAttribute.background is not None else (0, 0, 0)
            newBackground = tuple_with(oldBackground, _1=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, background=newBackground)
        if string_starts_with(command, "k"): # Background B
            value = base64_decode(string_slice(command, 1))
            oldBackground = newAttribute.background if newAttribute.background is not None else (0, 0, 0)
            newBackground = tuple_with(oldBackground, _2=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, background=newBackground)
        
        if string_starts_with(command, "z"): # Foreground&Foreground reset
            newAttribute = namedtuple_with(newAttribute, foreground=None, background=None)
        if string_starts_with(command, "x"): # Foreground&Foreground RGBA
            value = base64_decode(string_slice(command, 1))
            newForeground = (ord(value[0]), ord(value[1]), ord(value[2]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground, background=newForeground)
        if string_starts_with(command, "c"): # Foreground&Foreground RG
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _0=ord(value[0]), _1=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground, background=newForeground)
        if string_starts_with(command, "v"): # Foreground&Foreground GB
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _1=ord(value[0]), _2=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground, background=newForeground)
        if string_starts_with(command, "b"): # Foreground&Foreground BR
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _2=ord(value[0]), _0=ord(value[1]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground, background=newForeground)
        if string_starts_with(command, "n"): # Foreground&Foreground R
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _0=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground, background=newForeground)
        if string_starts_with(command, "m"): # Foreground&Foreground G
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _1=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground, background=newForeground)
        if string_starts_with(command, "l"): # Foreground&Foreground B
            value = base64_decode(string_slice(command, 1))
            oldForeground = newAttribute.foreground if newAttribute.foreground is not None else (0, 0, 0)
            newForeground = tuple_with(oldForeground, _2=ord(value[0]))
            newAttribute = namedtuple_with(newAttribute, foreground=newForeground, background=newForeground)
    return newAttribute
