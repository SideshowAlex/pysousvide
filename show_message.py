import datetime
import thread
import time

import lcd
import utils


messages = [
        "Don is a turd.",
        "A smelly turd.",
        "wlan IP:",
        lambda: utils.inet_address('wlan0'),
        lambda: datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'),
]

with lcd.new_lcd() as display:
    display.messages = messages
    while True:
        display.page_down(loop=True)
        time.sleep(1)
