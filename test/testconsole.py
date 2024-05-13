from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from utils.math import *
import time

driver = driverstd_new()
driver_clear_contents(driver)

textFormatter = text_formatter_new(driver)

frameCount = 0
lastFrame = time.monotonic() * 1000
def loop():
    global frameCount, lastFrame
    frameCount += 1
    now = time.monotonic() * 1000
    deltaTime = now - lastFrame
    lastFrame = now
    driver_tick(driver)
    driverSize = driver_get_size(driver)
    text = rune_from_string(f"Size: {driverSize.w} x {driverSize.h} FPS: {1000 / deltaTime:.2f}", RuneAttribute_clear)
    text_formatter_set_text(textFormatter, text)
    text_formatter_draw(textFormatter, rectangle_from_point_size(EmptyPoint, driverSize))
    centerRectangle = Rectangle(driverSize.w // 4, driverSize.h // 4, driverSize.w // 2, driverSize.h // 2)
    driver_fill_rect(driver, centerRectangle, Rune("L", RuneAttribute(0, 0, False, False, (frameCount % 255, 0, 0), (0, 0, 0))))
    driver_draw(driver)

looper = looper_new("Main")
with looper_closure(looper):
    set_interval(loop, 15)
while True:
    looper_tick(looper)
