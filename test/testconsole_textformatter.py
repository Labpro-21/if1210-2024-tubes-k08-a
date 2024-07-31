from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from utils.math import *
import time
import random

driver = driverstd_new()
driver_clear_rect(driver)

textFormatter = text_formatter_new(driver)
text_formatter_set_direction(textFormatter, "LeftRight_BottomTop")
text_formatter_set_horizontal_alignment(textFormatter, "Center")
text_formatter_set_vertical_alignment(textFormatter, "Middle")

frameCount = 0
lastFrame = time.monotonic() * 1000
textStyle = 0
def loop():
    global frameCount, lastFrame, textStyle
    frameCount += 1
    now = time.monotonic() * 1000
    deltaTime = now - lastFrame
    lastFrame = now
    
    if frameCount % 70 == 0:
        driver_clear_rect(driver)
        directions = ["LeftRight_TopBottom", "TopBottom_LeftRight", "RightLeft_TopBottom", "TopBottom_RightLeft", "LeftRight_BottomTop", "BottomTop_LeftRight", "RightLeft_BottomTop", "BottomTop_RightLeft"]
        text_formatter_set_direction(textFormatter, directions[int(random.random() * len(directions))])
    if frameCount % 150 == 0:
        driver_clear_rect(driver)
        textStyle = (textStyle + 1) % 9
        if textStyle == 0:
            text_formatter_set_horizontal_alignment(textFormatter, "Left")
            text_formatter_set_vertical_alignment(textFormatter, "Top")
        if textStyle == 1:
            text_formatter_set_horizontal_alignment(textFormatter, "Center")
            text_formatter_set_vertical_alignment(textFormatter, "Top")
        if textStyle == 2:
            text_formatter_set_horizontal_alignment(textFormatter, "Right")
            text_formatter_set_vertical_alignment(textFormatter, "Top")
        if textStyle == 3:
            text_formatter_set_horizontal_alignment(textFormatter, "Left")
            text_formatter_set_vertical_alignment(textFormatter, "Middle")
        if textStyle == 4:
            text_formatter_set_horizontal_alignment(textFormatter, "Center")
            text_formatter_set_vertical_alignment(textFormatter, "Middle")
        if textStyle == 5:
            text_formatter_set_horizontal_alignment(textFormatter, "Right")
            text_formatter_set_vertical_alignment(textFormatter, "Middle")
        if textStyle == 6:
            text_formatter_set_horizontal_alignment(textFormatter, "Left")
            text_formatter_set_vertical_alignment(textFormatter, "Bottom")
        if textStyle == 7:
            text_formatter_set_horizontal_alignment(textFormatter, "Center")
            text_formatter_set_vertical_alignment(textFormatter, "Bottom")
        if textStyle == 8:
            text_formatter_set_horizontal_alignment(textFormatter, "Right")
            text_formatter_set_vertical_alignment(textFormatter, "Bottom")
    
    driver_tick(driver)
    driverSize = driver_get_size(driver)
    
    centerRectangle = Rectangle(driverSize.w // 4, driverSize.h // 4, driverSize.w // 2, driverSize.h // 2)
    driver_fill_rect(driver, centerRectangle, Rune("L", RuneAttribute(0, 0, False, False, (frameCount % 255, 0, 0), (0, 0, 0))))
    
    text = rune_from_string(f"FPS: {1000 / deltaTime:.2f}\nSize: {driverSize.w} x {driverSize.h}", RuneAttribute_clear)
    text_formatter_set_text(textFormatter, text)
    text_formatter_draw(textFormatter, rectangle_from_point_size(EmptyPoint, driverSize))
    
    driver_draw(driver)

looper = looper_new("Main")
with looper_closure(looper):
    set_interval(loop, 1)
while True:
    looper_tick(looper)
