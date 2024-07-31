from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from utils.math import *
import time
import random

driver = driverstd_new()
driver_clear_rect(driver)

toplevel = toplevel_new(driver)

dialogView = view_new(driver)
view_add_child(toplevel, dialogView)
view_set_x(dialogView, pos_from_factor(0.1))
view_set_y(dialogView, pos_from_factor(0.1))
view_set_width(dialogView, dim_from_factor(0.8))
view_set_height(dialogView, dim_from_factor(0.8))
adornment_set_thickness(view_get_border(dialogView), Thickness(1, 1, 1, 1))

titleView = view_new(driver)
view_add_child(dialogView, titleView)
view_set_x(titleView, pos_from_absolute(0))
view_set_y(titleView, pos_from_absolute(0))
view_set_width(titleView, dim_from_fill(0))
view_set_height(titleView, dim_from_absolute(2))
textFormatter = view_get_text_formatter(titleView)
text_formatter_set_text(textFormatter, rune_from_string("FPS", RuneAttribute_clear))

contentView = view_new(driver)
view_add_child(dialogView, contentView)
view_set_x(contentView, pos_from_absolute(0))
view_set_y(contentView, pos_from_absolute(3))
view_set_width(contentView, dim_from_fill(0))
view_set_height(contentView, dim_from_fill(0))
textFormatter = view_get_text_formatter(contentView)
text_formatter_set_text(textFormatter, rune_from_string("00.00", RuneAttribute_clear))

frameCount = 0
lastFrame = time.monotonic() * 1000
textStyle = 0
def loop():
    global frameCount, lastFrame, textStyle
    frameCount += 1
    now = time.monotonic() * 1000
    deltaTime = now - lastFrame
    lastFrame = now
    
    text_formatter_set_text(view_get_text_formatter(contentView), rune_from_string(f"{1000/deltaTime:.2f}", RuneAttribute_clear))
    
    driver_tick(driver)
    
    view_mark_recompute_layout(toplevel)
    view_recompute_layout(toplevel)
    view_mark_recompute_display(toplevel)
    view_draw(toplevel)
    
    driver_draw(driver)

looper = looper_new("Main")
with looper_closure(looper):
    set_interval(loop, 1)
while True:
    looper_tick(looper)
