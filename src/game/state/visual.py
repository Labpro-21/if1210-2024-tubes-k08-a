from utils.primordials import *
from utils.console import *
from utils.coroutines import *
from utils.csv import *
from utils.codec import *
from utils.mixin import *
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
    __visual_attach_mock_view_add_remove_child_method(visual, toplevel)
    __visual_attach_connect_handler(visual, toplevel)
    __visual_attach_disconnect_handler(visual, toplevel)
    __visual_attach_key_handler(visual, toplevel)
    toplevel["__connected"] = True
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
    driver = visual["driver"]
    if visual["view"] is view:
        return
    if visual["view"] is not None:
        view_remove_child(toplevel, visual["view"])
    driver_clear_rect(driver)
    visual["view"] = view
    if view is None:
        return
    view_add_child(toplevel, view)
def _visual_set_directory(visual: _Visual, directory: str) -> None:
    visual["directory"] = directory

def _visual_get_root_view(visual: _Visual, view: View) -> View:
    currentView = view
    while currentView["superview"] is not None and currentView["superview"] is not visual["toplevel"]:
        currentView = currentView["superview"]
    return currentView

def __visual_attach_mock_view_add_remove_child_method(visual: _Visual, view: View):
    if "__mock_view_add_remove_child" in view and view["__mock_view_add_remove_child"] is not None:
        viewVisual, original_view_add_child, original_view_remove_child = view["__mock_view_add_remove_child"]
        if viewVisual is visual:
            return
        __visual_detach_mock_view_add_remove_child_method(viewVisual, view)
    subviews = view["subviews"]
    for subview in subviews:
        __visual_attach_mock_view_add_remove_child_method(visual, subview)
        __visual_attach_connect_handler(visual, subview)
        __visual_attach_disconnect_handler(visual, subview)
        __visual_attach_key_handler(visual, subview)
    original_view_add_child = mixin_get_override(visual, "_view_add_child")
    original_view_remove_child = mixin_get_override(visual, "_view_remove_child")
    def _mock_add_child(view: View, subview: View):
        result = None
        if original_view_add_child is not None:
            result = original_view_add_child(view, subview)
        else:
            result = mixin_call_super(view, subview, __mixin_self=_mock_add_child)
        __visual_attach_mock_view_add_remove_child_method(visual, subview)
        __visual_attach_connect_handler(visual, subview)
        __visual_attach_disconnect_handler(visual, subview)
        __visual_attach_key_handler(visual, subview)
        if _visual_is_connected(visual, view):
            connectListeners = subview["__connect_listeners"]
            for connectListener in connectListeners:
                connectListener()
        return result
    def _mock_remove_child(view: View, subview: View):
        result = None
        wasAChild = view_has_child(view, subview)
        if original_view_add_child is not None:
            result = original_view_remove_child(view, subview)
        else:
            result = mixin_call_super(view, subview, __mixin_self=_mock_remove_child)
        if wasAChild and _visual_is_connected(visual, view):
            disconnectListeners = subview["__disconnect_listeners"]
            for disconnectListener in disconnectListeners:
                disconnectListener()
        __visual_detach_mock_view_add_remove_child_method(visual, subview)
        return result
    view["__mock_view_add_remove_child"] = (visual, original_view_add_child, original_view_remove_child)
    mixin_set_override(view, 
        _view_add_child=_mock_add_child,
        _view_remove_child=_mock_remove_child,
    )
def __visual_detach_mock_view_add_remove_child_method(visual: _Visual, view: View):
    if "__mock_view_add_remove_child" not in view or view["__mock_view_add_remove_child"] is None:
        return
    viewVisual, original_view_add_child, original_view_remove_child = view["__mock_view_add_remove_child"]
    if viewVisual is not visual:
        return
    view["__mock_view_add_remove_child"] = None
    mixin_set_override(view, 
        _view_add_child=original_view_add_child,
        _view_remove_child=original_view_remove_child,
    )
    subviews = view["subviews"]
    for subview in subviews:
        __visual_detach_mock_view_add_remove_child_method(visual, subview)

def _visual_add_connect_listener(visual: _Visual, view: View, callback: Callable[[], Any]) -> None:
    connectListeners = view["__connect_listeners"]
    if array_includes(connectListeners, callback):
        return
    array_push(connectListeners, callback)
def _visual_remove_connect_listener(visual: _Visual, view: View, callback: Callable[[], Any]) -> None:
    connectListeners = view["__connect_listeners"]
    listenerIndex = array_index_of(connectListeners, callback)
    if listenerIndex == -1:
        return
    array_splice(connectListeners, listenerIndex, 1)

def _visual_add_disconnect_listener(visual: _Visual, view: View, callback: Callable[[], Any]) -> None:
    disconnectListeners = view["__disconnect_listeners"]
    if array_includes(disconnectListeners, callback):
        return
    array_push(disconnectListeners, callback)
def _visual_remove_disconnect_listener(visual: _Visual, view: View, callback: Callable[[], Any]) -> None:
    disconnectListeners = view["__disconnect_listeners"]
    listenerIndex = array_index_of(disconnectListeners, callback)
    if listenerIndex == -1:
        return
    array_splice(disconnectListeners, listenerIndex, 1)

def __visual_attach_connect_handler(visual: _Visual, view: View) -> None:
    connectListeners = None
    propagateHandler = None
    if "__connect_listeners" not in view:
        connectListeners = []
        view["__connect_listeners"] = connectListeners
    else:
        connectListeners = view["__connect_listeners"]
    if "__connect_propagate_handler" not in view:
        def propagateToSubviews() -> None:
            view["__connected"] = True
            subviews = view["subviews"]
            for subview in subviews:
                if "__connect_listeners" not in subview:
                    continue
                subviewConnectListeners = subview["__connect_listeners"]
                for subviewConnectListener in subviewConnectListeners:
                    subviewConnectListener()
        propagateHandler = propagateToSubviews
        view["__connect_propagate_handler"] = propagateHandler
    else:
        propagateHandler = view["__connect_propagate_handler"]
    if array_includes(connectListeners, propagateHandler):
        return
    array_push(connectListeners, propagateHandler)
def __visual_attach_disconnect_handler(visual: _Visual, view: View) -> None:
    disconnectListeners = None
    propagateHandler = None
    if "__disconnect_listeners" not in view:
        disconnectListeners = []
        view["__disconnect_listeners"] = disconnectListeners
    else:
        disconnectListeners = view["__disconnect_listeners"]
    if "__disconnect_propagate_handler" not in view:
        def propagateToSubviews() -> None:
            view["__connected"] = False
            subviews = view["subviews"]
            for subview in subviews:
                if "__disconnect_listeners" not in subview:
                    continue
                subviewConnectListeners = subview["__disconnect_listeners"]
                for subviewConnectListener in subviewConnectListeners:
                    subviewConnectListener()
        propagateHandler = propagateToSubviews
        view["__disconnect_propagate_handler"] = propagateHandler
    else:
        propagateHandler = view["__disconnect_propagate_handler"]
    if array_includes(disconnectListeners, propagateHandler):
        return
    array_push(disconnectListeners, propagateHandler)

def _visual_is_connected(visual: _Visual, view: View) -> bool:
    return ("__connected" in view and view["__connected"] and 
        "__mock_view_add_remove_child" in view and view["__mock_view_add_remove_child"][0] is visual)

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
    if "__key_listeners" not in view:
        keyListeners = []
        view["__key_listeners"] = keyListeners
    else:
        keyListeners = view["__key_listeners"]
    if "__key_propagate_handle" not in view:
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
    toplevel = visual["toplevel"]
    keyListeners = toplevel["__key_listeners"]
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
        frames: list[list[Rune]], /,
        x: Pos = pos_from_center(),
        y: Pos = pos_from_center(),
        width: Dim = dim_from_fill(0),
        height: Dim = dim_from_fill(0),
        border: tuple = (0, 0, 0, 0),
        padding: tuple = (0, 0, 0, 0),
        horizontalAlignment: TextHorizontalAlignment = "Center",
        verticalAlignment: TextVerticalAlignment = "Middle",
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
    textFormatter = view_get_text_formatter(mainView)
    text_formatter_set_wordwrap(textFormatter, False)
    text_formatter_set_horizontal_alignment(textFormatter, horizontalAlignment)
    text_formatter_set_vertical_alignment(textFormatter, verticalAlignment)

    __visual_attach_mock_view_add_remove_child_method(visual, mainView)
    __visual_attach_connect_handler(visual, mainView)
    __visual_attach_disconnect_handler(visual, mainView)
    __visual_attach_key_handler(visual, mainView)
    
    currentFrame = -1
    def setFrame(index: int) -> bool:
        nonlocal currentFrame
        if index < 0 or index >= len(frames):
            return False
        currentFrame = index
        text_formatter_set_text(textFormatter, frames[index])
        return True
    def nextFrame() -> None:
        nonlocal currentFrame
        return setFrame(currentFrame + 1)
    def previousFrame() -> None:
        nonlocal currentFrame
        return setFrame(currentFrame - 1)
    handle = None
    onConnectCb = None
    onDisconnectCb = None
    def onConnect(args):
        nonlocal onConnectCb
        _visual_remove_connect_listener(visual, mainView, onConnectCb)
        onConnectCb = None
        play(*args)
    def onDisconnect(args):
        nonlocal handle, onDisconnectCb, onConnectCb
        _visual_remove_disconnect_listener(visual, mainView, onDisconnectCb)
        onDisconnectCb = None
        clear_interval(handle)
        handle = None
        onConnectCb = lambda: onConnect(args)
        _visual_add_connect_listener(visual, mainView, onConnectCb)
    def play(fps: float = 60, loopFrame = False) -> None:
        nonlocal handle
        if handle is not None:
            stop()
        if len(frames) <= 1:
            setFrame(0)
            return
        def loop():
            nonlocal handle
            if nextFrame():
                return True
            if not loopFrame:
                stop()
                return False
            setFrame(0)
            return True
        if not _visual_is_connected(visual, mainView):
            onConnectCb = lambda: onConnect((fps, loopFrame))
            _visual_add_connect_listener(visual, mainView, onConnectCb)
            return
        if not loop():
            return
        onDisconnectCb = lambda: onDisconnect((fps, loopFrame))
        _visual_add_disconnect_listener(visual, mainView, onDisconnectCb)
        handle = set_interval(loop, 1000 / fps)
    def stop() -> None:
        nonlocal handle, onConnectCb, onDisconnectCb
        if onConnectCb is not None:
            _visual_remove_connect_listener(visual, mainView, onConnectCb)
            onConnectCb = None
        if onDisconnectCb is not None:
            _visual_remove_disconnect_listener(visual, mainView, onDisconnectCb)
            onDisconnectCb = None
        _visual_remove_connect_listener(visual, mainView, onConnect)
        if handle is None:
            return
        clear_interval(handle)
        handle = None
    mainView["setFrame"] = setFrame
    mainView["nextFrame"] = nextFrame
    mainView["previousFrame"] = previousFrame
    mainView["play"] = play
    mainView["stop"] = stop
    if parent is not None:
        view_add_child(parent, mainView)
    else:
        _visual_set_view(visual, mainView)
    return mainView

def _visual_show_splash(
        visual: _Visual, 
        splash: str,
        **kwargs
    ) -> View:
    splashes = visual["splashes"]
    splash = splashes[splash]
    return _visual_show_frame_sequence(visual, splash, **kwargs)

def _visual_show_simple_dialog(
        visual: _Visual,
        title: __Text = "",
        content: __Text = "",
        /,
        x: Pos = pos_from_center(),
        y: Pos = pos_from_center(),
        width: Dim = dim_from_factor(0.5),
        height: Dim = dim_from_factor(0.5),
        border: tuple = (1, 1, 1, 1),
        padding: tuple = (2, 1, 2, 1),
        horizontalAlignment: TextHorizontalAlignment = "Left",
        verticalAlignment: TextVerticalAlignment = "Top",
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
    view_set_y(contentView, pos_from_view_bottom(titleView) if titleView is not None else pos_from_absolute(0))
    view_set_width(contentView, dim_from_fill(0))
    view_set_height(contentView, dim_from_fill(0))
    textFormatter = view_get_text_formatter(contentView)
    text_formatter_set_text(textFormatter, __parse_colored_text(content)[0])
    text_formatter_set_horizontal_alignment(textFormatter, horizontalAlignment)
    text_formatter_set_vertical_alignment(textFormatter, verticalAlignment)

    __visual_attach_mock_view_add_remove_child_method(visual, mainView)
    __visual_attach_connect_handler(visual, mainView)
    __visual_attach_disconnect_handler(visual, mainView)
    __visual_attach_key_handler(visual, mainView)

    mainView["titleView"] = titleView
    mainView["contentView"] = contentView
    mainView["setTitle"] = lambda t: text_formatter_set_text(view_get_text_formatter(titleView), __parse_colored_text(t)[0])
    mainView["setContent"] = lambda t: text_formatter_set_text(view_get_text_formatter(contentView), __parse_colored_text(t)[0])
    if parent is not None:
        view_add_child(parent, mainView)
    else:
        _visual_set_view(visual, mainView)
    return mainView

def _visual_show_table(
        visual: _Visual,
        columns: list[tuple[__Text, float]],
        rows: list[list[__Text]], /,
        x: Pos = pos_from_absolute(0),
        y: Pos = pos_from_absolute(0),
        width: Dim = dim_from_fill(0),
        height: Dim = dim_from_fill(0),
        parent: Optional[View] = None
    ) -> View:
    driver = visual["driver"]
    mainView = view_new(driver)
    view_set_x(mainView, x)
    view_set_y(mainView, y)
    view_set_width(mainView, width)
    view_set_height(mainView, height)

    lastColumns: list[tuple[__Text, float]] = None
    rowViews: list[View] = []
    patchViews: list[View] = []
    cellValuePadX = [Rune(" ", RuneAttribute_clear) for _ in range(0, 50)]
    cellValuePadY = array_flat([[Rune("\n", RuneAttribute_clear), *cellValuePadX, Rune("\n", RuneAttribute_clear)] for _ in range(0, 5)])
    def addPatch(patchCharacter: str, patchPosX: Pos, patchPosY: Pos):
        patchView = view_new(driver)
        array_push(patchViews, patchView)
        view_set_x(patchView, patchPosX)
        view_set_y(patchView, patchPosY)
        view_set_width(patchView, dim_from_absolute(1))
        view_set_height(patchView, dim_from_absolute(1))
        patchTextFormatter = view_get_text_formatter(patchView)
        text_formatter_set_text(patchTextFormatter, [Rune(patchCharacter, RuneAttribute_clear)])
    def updateCellTextView(cellTextView: View, value: __Text, alignment: Optional[str]):
        textFormatter = view_get_text_formatter(cellTextView)
        text_formatter_set_wordwrap(textFormatter, False)
        parsedCellValue = __parse_colored_text(value)[0]
        if alignment is not None:
            paddedText = parsedCellValue
            if string_starts_with(alignment, "Left"):
                paddedText = [*paddedText, *cellValuePadX]
                text_formatter_set_horizontal_alignment(textFormatter, "Left")
            if string_starts_with(alignment, "Center"):
                paddedText = [*cellValuePadX, *paddedText, *cellValuePadX]
                text_formatter_set_horizontal_alignment(textFormatter, "Center")
            if string_starts_with(alignment, "Right"):
                paddedText = [*cellValuePadX, *paddedText]
                text_formatter_set_horizontal_alignment(textFormatter, "Right")
            if string_ends_with(alignment, "Top"):
                paddedText = [*paddedText, *cellValuePadY]
                text_formatter_set_vertical_alignment(textFormatter, "Top")
            if string_ends_with(alignment, "Middle"):
                paddedText = [*cellValuePadY, *paddedText]
                text_formatter_set_vertical_alignment(textFormatter, "Middle")
            if string_ends_with(alignment, "Bottom"):
                paddedText = [*cellValuePadY, *paddedText, *cellValuePadY]
                text_formatter_set_vertical_alignment(textFormatter, "Bottom")
            cellTextView["originalText"] = paddedText
            text_formatter_set_text(textFormatter, paddedText)
        else:
            paddedText = [*parsedCellValue, *cellValuePadX]
            cellTextView["originalText"] = paddedText
            text_formatter_set_text(textFormatter, paddedText)
    def updateTable(columns: list[tuple[__Text, float]], rows: list[list[__Text]]):
        nonlocal lastColumns, lastSelectableIndex
        for rowView in array_splice(rowViews, 0):
            view_remove_child(mainView, rowView)
        for patchView in array_splice(patchViews, 0):
            view_remove_child(mainView, patchView)
        
        lastColumns = columns
        rows = array_slice(rows)
        array_unshift(rows, array_map(columns, lambda c, *_: c[0]))
        lastRowView = None
        for i in range(0, len(rows)):
            rowData = rows[i]
            rowView = view_new(driver)
            array_push(rowViews, rowView)
            view_add_child(mainView, rowView)
            view_set_x(rowView, pos_from_absolute(0))
            view_set_y(rowView, pos_from_view_bottom(lastRowView) if lastRowView is not None else pos_from_absolute(0))
            view_set_width(rowView, dim_from_fill(0))
            view_set_height(rowView, dim_from_absolute(3 if i == 0 else 2))

            cellViews = []
            rowView["cellViews"] = cellViews
            lastCellView = None
            for j in range(0, len(columns)):
                columnSize = columns[j][1]
                cellView = view_new(driver)
                array_push(cellViews, cellView)
                view_add_child(rowView, cellView)
                view_set_x(cellView, pos_from_view_right(lastCellView) if lastCellView is not None else pos_from_absolute(0))
                view_set_y(cellView, pos_from_absolute(0))
                view_set_width(cellView, dim_from_factor(columnSize) if type(columnSize) is float else dim_add(columnSize, dim_from_absolute(2 if j == 0 else 1)) if dim_as_absolute(columnSize) else columnSize)
                view_set_height(cellView, dim_from_fill(0))
                adornment_set_thickness(view_get_border(cellView), Thickness(1 if j == 0 else 0, 1 if i == 0 else 0, 1, 1))
                if len(columns[j]) > 3:
                    padding = columns[j][3]
                    adornment_set_thickness(view_get_padding(cellView), Thickness(*padding))

                cellTextView = view_new(driver)
                cellView["textView"] = cellTextView
                view_add_child(cellView, cellTextView)
                view_set_x(cellTextView, pos_from_absolute(0))
                view_set_y(cellTextView, pos_from_absolute(0))
                view_set_width(cellTextView, dim_from_fill(0))
                view_set_height(cellTextView, dim_from_fill(0))
                updateCellTextView(cellTextView, rowData[j], columns[j][2] if len(columns[j]) > 2 else None)

                patchCharacter = None
                patchPosX = None
                patchPosY = None
                if i == 0 and j != 0:
                    addPatch(
                        "┬",
                        pos_sub(pos_from_view_left(cellView), pos_from_absolute(1)),
                        pos_from_view_top(cellView)
                    )
                if i == len(rows) - 1 and j != 0:
                    addPatch(
                        "┴",
                        pos_sub(pos_from_view_left(cellView), pos_from_absolute(1)),
                        pos_sub(pos_from_view_bottom(cellView), pos_from_absolute(1))
                    )
                if i != 0 and j == 0:
                    addPatch(
                        "├",
                        pos_from_view_left(cellView),
                        pos_sub(pos_from_view_top(cellView), pos_from_absolute(1))
                    )
                if i != 0 and j == len(columns) - 1:
                    addPatch(
                        "┤",
                        pos_sub(pos_from_view_right(cellView), pos_from_absolute(1)),
                        pos_sub(pos_from_view_top(cellView), pos_from_absolute(1))
                    )
                if i != 0 and j != 0:
                    addPatch(
                        "┼",
                        pos_sub(pos_from_view_left(cellView), pos_from_absolute(1)),
                        pos_sub(pos_from_view_top(cellView), pos_from_absolute(1))
                    )
                
                lastCellView = cellView
            lastRowView = rowView
        
        for patchView in patchViews:
            view_add_child(mainView, patchView)
        lastSelectableIndex = -1
        selectableChange()
    def updateRows(rows: list[list[__Text]]) -> None:
        nonlocal lastColumns, lastSelectableIndex
        if len(rows) != len(rowViews) - 1:
            updateTable(lastColumns, rows)
            return
        # Fasttrack
        for i in range(0, len(rows)):
            rowData = rows[i]
            rowView = rowViews[i + 1]
            cellViews = rowView["cellViews"]
            for j in range(0, len(columns)):
                cellView = cellViews[j]
                cellTextView = cellView["textView"]
                updateCellTextView(cellTextView, rowData[j], columns[j][2] if len(columns[j]) > 2 else None)
        lastSelectableIndex = -1
        selectableChange()

    __visual_attach_mock_view_add_remove_child_method(visual, mainView)
    __visual_attach_connect_handler(visual, mainView)
    __visual_attach_disconnect_handler(visual, mainView)
    __visual_attach_key_handler(visual, mainView)
    
    selectable = False
    selectableIndex = -1
    lastSelectableIndex = -1
    hoverListener = None
    enterListener = None
    def selectable0(value: bool) -> Optional[bool]:
        nonlocal selectable
        if value is None:
            return selectable
        selectable = value
        selectableChange()
        if selectable:
            _visual_add_key_listener(visual, mainView, onKey)
        else:
            _visual_remove_key_listener(visual, mainView, onKey)
    def onHover(value: Callable[[int], Any]) -> None:
        nonlocal hoverListener
        hoverListener = value
    def onEnter(value: Callable[[int], Any]) -> None:
        nonlocal enterListener
        enterListener = value
    def setSelection(index: int) -> None:
        nonlocal selectableIndex
        selectableIndex = index
        selectableChange()
    def selectableChange():
        nonlocal selectable, selectableIndex, lastSelectableIndex, hoverListener
        if selectableIndex < -1:
            selectableIndex = -1
        if selectableIndex >= len(rowViews) - 1:
            selectableIndex = len(rowViews) - 2
        if selectable and selectableIndex == lastSelectableIndex:
            return
        if lastSelectableIndex != -1:
            rowView = rowViews[lastSelectableIndex + 1]
            cellViews = rowView["cellViews"]
            for cellView in cellViews:
                cellTextView = cellView["textView"]
                originalText = cellTextView["originalText"]
                textFormatter = view_get_text_formatter(cellTextView)
                text_formatter_set_text(textFormatter, originalText)
        if not selectable:
            lastSelectableIndex = -1
            if hoverListener is not None:
                hoverListener(-1)
            return
        if selectableIndex != -1:
            rowView = rowViews[selectableIndex + 1]
            cellViews = rowView["cellViews"]
            for cellView in cellViews:
                cellTextView = cellView["textView"]
                originalText = cellTextView["originalText"]
                reversedColoredText = __reverse_background_foreground(originalText)
                textFormatter = view_get_text_formatter(cellTextView)
                text_formatter_set_text(textFormatter, reversedColoredText)
        lastSelectableIndex = selectableIndex
        if hoverListener is not None:
            hoverListener(selectableIndex)
    def onKey(event: KeyEvent):
        nonlocal selectable, selectableIndex, enterListener
        if not selectable or len(rowViews) < 1:
            return
        if event.key == "ControlCR" or event.key == "ControlLF":
            if selectableIndex == -1 or enterListener is None:
                return
            enterListener(selectableIndex)
            return
        if event.key == "Up":
            selectableIndex = max(0, selectableIndex - 1) if selectableIndex != -1 else len(rowViews) - 2
            selectableChange()
            return
        if event.key == "Down":
            selectableIndex = min(len(rowViews) - 2, selectableIndex + 1) if selectableIndex != -1 else 0
            selectableChange()
            return
    updateTable(columns, rows)
    mainView["rowViews"] = rowViews
    mainView["patchViews"] = patchViews
    mainView["updateTable"] = updateTable
    mainView["updateRows"] = updateRows
    mainView["selectable"] = selectable0
    mainView["onHover"] = onHover
    mainView["onEnter"] = onEnter
    mainView["setSelection"] = setSelection
    if parent is not None:
        view_add_child(parent, mainView)
    else:
        _visual_set_view(visual, mainView)
    return mainView

_ConsoleMock = tuple[Callable[[__Text], None], Callable[[__Text], Promise[str]], Callable[[str, Any], None]]
def _visual_with_mock(visual: _Visual, view: View, **kwargs) -> _ConsoleMock:
    driver = visual["driver"]
    setTitle = view["setTitle"]
    setContent = view["setContent"]
    flagsStack: list[dict[str, Any]] = []
    flags = dict_with(
        dict(
            keySpeed=-1, # characters per second
            keyAnimationAllowSkip=True,
            hasTitle=False,
            selectableWaitAfterContent=True,
            selectableClearAfterSelection=True,
            selectableAllowEscape=True,
            selectableAlignment="CenterMiddle",
            selectableXOffset=0,
            selectableYOffset=0,
            inputWaitAfterContent=True,
            inputAllowEscape=True,
            inputBoxOffset=1,
            doNotRaiseSignal=False
        ),
        **kwargs
    )

    lastDrawing: Optional[float] = None
    drawingOnCompletes: list[Callable[[], None]] = []
    contentLastAttribute = RuneAttribute_clear
    content: list[Rune] = []
    contentDrawnPosition = 0
    printKeyListenerAttached = False
    def onPrintKey(event: KeyEvent):
        nonlocal contentDrawnPosition
        if event.key == "Up" or event.key == "Down" or event.key == "ControlCR" or event.key == "ControlLF":
            if not flags["keyAnimationAllowSkip"]:
                return
            contentDrawnPosition = len(content)
            setContent(content)
    def doPrintDraw():
        nonlocal lastDrawing, contentDrawnPosition, printKeyListenerAttached
        if not _visual_is_connected(visual, view):
            return
        keySpeed = flags["keySpeed"]
        if keySpeed == -1:
            contentDrawnPosition = len(content)
            setContent(content)
            if printKeyListenerAttached:
                _visual_remove_key_listener(visual, view, onPrintKey)
                printKeyListenerAttached = False
            for drawingOnComplete in array_splice(drawingOnCompletes, 0):
                drawingOnComplete()
            return
        now = __now()
        deltaTime = now - lastDrawing if lastDrawing is not None else 0
        lastDrawing = now
        if int(contentDrawnPosition) == len(content):
            lastDrawing = None
            if printKeyListenerAttached:
                _visual_remove_key_listener(visual, view, onPrintKey)
                printKeyListenerAttached = False
            for drawingOnComplete in array_splice(drawingOnCompletes, 0):
                drawingOnComplete()
            return
        if not printKeyListenerAttached:
            _visual_add_key_listener(visual, view, onPrintKey)
            printKeyListenerAttached = True
        advancePosition = keySpeed * deltaTime / 1000 if keySpeed != -1 else len(content) - contentDrawnPosition
        contentDrawnPosition += advancePosition
        contentDrawnPosition = min(contentDrawnPosition, len(content))
        drawnContent = array_slice(content, 0, int(contentDrawnPosition))
        setContent(drawnContent)
        set_timeout(doPrintDraw, 15)
    def waitPrintDrawComplete():
        if lastDrawing is None:
            return promise_resolved(None)
        def executor(resolve, _):
            array_push(drawingOnCompletes, lambda: resolve(None))
        return promise_new(executor)
    def clearPrint():
        nonlocal contentDrawnPosition, contentLastAttribute
        array_splice(content, 0)
        contentDrawnPosition = 0
        contentLastAttribute = RuneAttribute_clear
        doPrintDraw()
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
    _visual_add_connect_listener(visual, view, doPrintDraw)

    def encapsulatePromise(promise: Promise[Any], kwargs: dict, onSignalCb: Callable[[], Any] = None) -> Promise[Any]:
        if "signal" not in kwargs or kwargs["signal"] is None:
            return promise
        doneFirst = False
        def onResolve(result):
            nonlocal doneFirst
            doneFirst = True
            return result
        promise = promise_then(promise, onResolve)
        signal = kwargs["signal"]
        signalPromise = promise_from_abortsignal(signal)
        if flags["doNotRaiseSignal"]:
            def onReject(_):
                nonlocal doneFirst
                if doneFirst:
                    return signal
                if onSignalCb is not None:
                    onSignalCb()
                return signal
            signalPromise = promise_catch(signalPromise, onSignalCb)
        elif onSignalCb is not None:
            def onReject(reason):
                nonlocal doneFirst
                if not doneFirst:
                    onSignalCb()
                raise reason
            signalPromise = promise_catch(signalPromise, onSignalCb)
        return promise_race([promise, signalPromise])

    selectableIndex = -1
    selectables: list[View] = []
    selectableDescription: View = None
    selectableListeners: list[Callable[[str], None]] = []
    lastSelectableIndex = -1
    lastSelectables: list[View] = []
    def newSelectable(
            message: __Text, 
            description: __Text, /, 
            id: Any = None, 
            onChange: Callable[[bool], Any] = None):
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
        selectable["selectableOnChange"] = onChange
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
            view_set_y(selectableDescription, pos_add(pos_from_end(None), pos_from_absolute(1)))
            view_set_width(selectableDescription, dim_from_fill(0))
            view_set_height(selectableDescription, dim_from_absolute(2))
            adornment_set_thickness(view_get_border(selectableDescription), Thickness(0, 1, 0, 0))
            _visual_add_key_listener(visual, view, selectableOnKey)
        selectableAlignment = flags["selectableAlignment"]
        selectableXOffset = flags["selectableXOffset"]
        selectableYOffset = flags["selectableYOffset"]
        for i in range(len(selectables)):
            selectable = selectables[i]
            if string_starts_with(selectableAlignment, "Left"):
                view_set_x(selectable, pos_add(pos_from_absolute(0, pos_from_absolute(selectableXOffset))))
            if string_starts_with(selectableAlignment, "Center"):
                view_set_x(selectable, pos_add(pos_from_center(), pos_from_absolute(selectableXOffset)))
            if string_starts_with(selectableAlignment, "Right"):
                view_set_x(selectable, pos_add(pos_from_end(), pos_from_absolute(selectableXOffset)))
            if string_ends_with(selectableAlignment, "Top"):
                view_set_y(selectable, pos_add(pos_from_absolute(i + 2), pos_from_absolute(selectableYOffset)))
            if string_ends_with(selectableAlignment, "Middle"):
                view_set_y(selectable, pos_add(pos_add(pos_from_center(), pos_from_absolute(i - (len(selectables) // 2) + 2)), pos_from_absolute(selectableYOffset)))
            if string_ends_with(selectableAlignment, "Bottom"):
                view_set_y(selectable, pos_add(pos_sub(pos_from_end(), pos_from_absolute(len(selectables) - i - 1)), pos_from_absolute(selectableYOffset)))
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
            onChange = selectable["selectableOnChange"]
            if onChange is not None:
                onChange(False)
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
            onChange = selectable["selectableOnChange"]
            if onChange is not None:
                onChange(True)
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

    inputParent: View = None
    inputDescription: View = None
    inputIndex = -1
    inputViews: list[View] = []
    lastInputIndex = -1
    lastInputViews: list[View] = []
    def newInput(
            message: __Text, 
            description: __Text, /, 
            renderer: Callable[[list[Rune]], list[Rune]] = None, 
            onChange: Callable[[str], Any] = None, signal: AbortSignal = None):
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
        inputView["inputOnChange"] = onChange
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
        if signal is not None:
            def cleanUp():
                index = array_index_of(inputViews, inputView)
                if index == -1:
                    return
                array_splice(inputViews, inputView)
                layoutInput()
                inputChange()
            promise = encapsulatePromise(promise, dict(signal=signal), cleanUp)
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
            inputBoxOffset = flags["inputBoxOffset"]
            view_set_x(inputParent, pos_from_center())
            view_set_y(inputParent, pos_add(pos_from_center(), pos_from_absolute(inputBoxOffset)))
            view_set_width(inputParent, dim_from_factor(0.8))
            view_set_height(inputParent, dim_from_absolute(0))
            adornment_set_thickness(view_get_border(inputParent), Thickness(1, 1, 1, 1))
            view_add_child(view, inputParent)
            _visual_add_key_listener(visual, view, inputOnKey)
        if inputDescription is None:
            inputDescription = view_new(driver)
            view_set_x(inputDescription, pos_from_absolute(0))
            view_set_y(inputDescription, pos_add(pos_from_end(None), pos_from_absolute(1)))
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
                newInputIndex = array_find_last_index(inputViews, lambda v, i, *_: not v["inputDone"] and i < inputIndex)
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
        if event.key == "ControlBS":
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            value = inputCurrent["inputValue"]
            cursor = inputCurrent["inputCursor"]
            onChange = inputCurrent["inputOnChange"]
            if cursor == 0:
                return
            valueBefore = array_slice(value, 0, cursor - 1)
            valueAfter = array_slice(value, cursor)
            inputCurrent["inputValue"] = valueBefore + valueAfter
            if inputCurrent["inputCursor"] > 0:
                inputCurrent["inputCursor"] -= 1
            inputCurrent["inputUpdate"]()
            if onChange is not None:
                onChange(inputCurrent["inputValue"])
            return
        if len(event.key) == 1:
            if inputIndex == -1:
                return
            inputCurrent = inputViews[inputIndex]
            value = inputCurrent["inputValue"]
            cursor = inputCurrent["inputCursor"]
            onChange = inputCurrent["inputOnChange"]
            valueBefore = array_slice(value, 0, cursor)
            valueAfter = array_slice(value, cursor)
            inputCurrent["inputValue"] = valueBefore + event.key + valueAfter
            inputCurrent["inputCursor"] += 1
            inputCurrent["inputUpdate"]()
            if onChange is not None:
                onChange(inputCurrent["inputValue"])
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
        doPrintDraw()
    def input(message: __Text, *args, **kwargs) -> Any:
        if "selectable" in kwargs and kwargs["selectable"]:
            del kwargs["selectable"]
            do = lambda *_: newSelectable(message, args[0] if len(args) > 0 else None, **kwargs)
            if flags["selectableWaitAfterContent"]:
                return encapsulatePromise(promise_then(waitPrintDrawComplete(), do), kwargs)
            do()
            return
        do = lambda *_: newInput(message, args[0] if len(args) > 0 else None, **kwargs)
        if flags["inputWaitAfterContent"]:
            return encapsulatePromise(promise_then(waitPrintDrawComplete(), do), kwargs)
        return do()
    def metaAction(action: str, kwargs: dict) -> Any:
        nonlocal contentDrawnPosition, contentLastAttribute
        if action == "getVisual":
            return visual
        if action == "getRootView":
            return _visual_get_root_view(visual, view)
        if action == "setAsCurrentView":
            _visual_set_view(visual, _visual_get_root_view(visual, view))
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
        if action == "foreign":
            return __ConsoleMockClosureType((print, input, meta))
        if action == "clear":
            clearPrint()
            clearSelectables()
            clearInputs()
            return
        if action == "clearPrint":
            clearPrint()
            return
        if action == "waitContent":
            return encapsulatePromise(waitPrintDrawComplete(), kwargs)
        if action == "clearSelectables":
            clearSelectables()
            return
        if action == "select":
            def executor(resolve, _):
                array_push(selectableListeners, lambda s: resolve(s))
            def cleanup():
                if not flags["selectableClearAfterSelection"]:
                    return
                clearSelectables()
            return encapsulatePromise(promise_new(executor), kwargs, cleanup)
        if action == "clearInputs":
            clearInputs()
            return
        raise f"Unknown action {action}"
    def meta(*args, **kwargs) -> Any:
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

def __make_console_mock_closure_type():
    import builtins
    def __init__(self, console: _ConsoleMock):
        self.console = console
        self.lastConsole = None
    def __enter__(self):
        lastPrint = builtins.print
        lastInput = builtins.input
        lastMeta = builtins.meta if hasattr(builtins, "meta") else None
        self.lastConsole = (lastPrint, lastInput, lastMeta)
        builtins.print = self.console[0]
        builtins.input = self.console[1]
        builtins.meta = self.console[2]
    def __exit__(self, *_):
        builtins.print = self.lastConsole[0]
        builtins.input = self.lastConsole[1]
        builtins.meta = self.lastConsole[2]
        self.lastConsole = None
        return False
    ConsoleMockClosureType = type("ConsoleMockClosure", (object,), dict(
        __init__=__init__,
        __enter__=__enter__,
        __exit__=__exit__
    ))
    return ConsoleMockClosureType
__ConsoleMockClosureType = __make_console_mock_closure_type()

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

def _smnstr(name: str) -> str: # Coloring for self monster
    return f"{_fg('39ACF6')}{name}{_fg()}"
def _omnstr(name: str) -> str: # Coloring for opponent monster
    return f"{_fg('E3111A')}{name}{_fg()}"
def _ptncl(potion: str) -> str:
    return f"{_fg('DEB462')}{potion}{_fg()}"
def _stbar(value: float, max: float, desc: str = None, bounds: Union[View, int] = 10) -> str: # Coloring for stats bar
    if desc is None:
        desc = f"{value:.2f}/{max:.2f}"
    if type(bounds) is dict:
        view = bounds
        bounds = view["frame"].w # This is illegal access
        bounds -= thickness_get_horizontal(adornment_get_thickness(view_get_margin(view)))
        bounds -= thickness_get_horizontal(adornment_get_thickness(view_get_border(view)))
        bounds -= thickness_get_horizontal(adornment_get_thickness(view_get_padding(view)))
    ratio = value / max
    ratioWidth = int(bounds * ratio)
    result = _bg("52A441") if ratio > 0.5 else _bg("FCD216") + _fg(0, 0, 0) if ratio > 0.2 else _bg("BD0820")
    result += array_join([desc[i] if i < len(desc) else " " for i in range(0, min(ratioWidth, bounds))], "")
    result += _bg("C5B4B4") + _fg(0, 0, 0)
    result += array_join([desc[i] if i < len(desc) else " " for i in range(ratioWidth, bounds)], "")
    result += _fbg()
    return result
def _ratmod(ratio: float) -> str:
    return f"{_fg('52A441') + '+' if ratio >= 0 else _fg('BD0820')}{ratio * 100:.2f}%{_fg()}"
def _txtk(text: str) -> str:
    return f"{_fg('C5B4B4')}{text}{_fg()}"
def _txtv(text: str) -> str:
    return f"{_fg()}{text}"
def _txtkv(key: str, value: str) -> str:
    return f"{_fg('C5B4B4')}{key}{_fg()}{value}"
def _txtqty(qty: int) -> str:
    return f"{_fg('CD94C5')}{qty}{_fg()}"
def _txtcrcy(currency: int) -> str:
    return f"{_fg('A3E2BB')}{currency}{_fg()}"
def _txtplnm(name: int) -> str:
    return f"{_fg('E69C00')}{name}{_fg()}"
def _txtdngr(danger: str) -> str:
    return f"{_fg('E63131')}{danger}{_fg()}"
def _txtprcd(proceed: str) -> str:
    return f"{_fg('52A441')}{proceed}{_fg()}"
def _txtcncl(cancel: str) -> str:
    return f"{_fg('FCD216')}{cancel}{_fg()}"
def _txthint(hint: str) -> str:
    return f"{_fg('E63131')}{hint}{_fg()}"
def _scrlup(arr: int = None) -> Union[str, list[str]]:
    result = _fg("C5B4B4") + string_repeat("▲", 10) + _fg()
    if arr is None:
        return result
    return [result for _ in range(arr)]
def _scrldw(arr: int = None) -> Union[str, list[str]]:
    result = _fg("C5B4B4") + string_repeat("▼", 10) + _fg()
    if arr is None:
        return result
    return [result for _ in range(arr)]
def _scrlad(arr: int = None) -> Union[str, list[str]]:
    result = _fg("52A441") + string_repeat("+", 10) + _fg()
    if arr is None:
        return result
    return [result for _ in range(arr)]

def __now() -> float:
    return time.monotonic() * 1000
def __load_splash_suspendable(state, args):
    if state == SuspendableInitial:
        path, progress = args
        rawFrames = None
        if string_ends_with(path, ".gif.txt"):
            rawFrames = csv_read_from_file(path)
            rawFrames = array_map(rawFrames, lambda f, *_: array_join(f, "\n"))
        if string_ends_with(path, ".png.txt"):
            with open(path, encoding="utf-8") as f:
                rawFrames = [f.read()]
        processedFrames = [[] for _ in range(len(rawFrames))]
        return 1, rawFrames, processedFrames, progress, 0, 0, RuneAttribute_clear
    if state == 1:
        rawFrames, processedFrames, progress, i, offset, lastAttribute = args
        rawFrame = rawFrames[i]
        if offset >= len(rawFrame):
            i += 1
            offset = 0
            if i >= len(rawFrames):
                if progress is not None:
                    progress(1)
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
    return SuspendableExhausted
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
