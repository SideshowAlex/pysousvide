import contextlib
import itertools
import threading
import time

from RPi import GPIO


LED_COMMON = 'LED_COMMON'
LED_RED = 'LED_RED'
LED_GREEN = 'LED_GREEN'
LED_BLUE = 'LED_BLUE'

DEFAULT_PINS = {
    LED_COMMON: 6,
    LED_RED: 13,
    LED_GREEN: 19,
    LED_BLUE: 26,
}

OFF = (False, False, False)
RED = (True, False, False)
GREEN = (False, True, False)
BLUE = (False, False, True)
YELLOW = (True, True, False)
MAGENTA = (True, False, True)
CYAN = (False, True, True)
WHITE = (True, True, True)

COLORS = (RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, WHITE)


def ncycles(iterable, n):
    return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))


@contextlib.contextmanager
def new_led(pins=None):
    led = LED(pins)
    try:
        yield led
    finally:
        led.dispose()


class LED(object):
    def __init__(self, pins=None):
        pins = pins or DEFAULT_PINS
        self._common_pin = pins[LED_COMMON]
        self._red_pin = pins[LED_RED]
        self._green_pin = pins[LED_GREEN]
        self._blue_pin = pins[LED_BLUE]
        self._on = True
        self._color = OFF
        self._init_gpio()
        self._terminated = False
        self._update_lock = threading.Lock()

    def _init_gpio(self):
        GPIO.setup(self._common_pin, GPIO.OUT)
        GPIO.setup(self._red_pin, GPIO.OUT)
        GPIO.setup(self._green_pin, GPIO.OUT)
        GPIO.setup(self._blue_pin, GPIO.OUT)

    def _update_led(self):
        with self._update_lock:
            if not self._terminated and self._on:
                color = self._color
                GPIO.output(self._red_pin, not color[0])
                GPIO.output(self._green_pin, not color[1])
                GPIO.output(self._blue_pin, not color[2])
                GPIO.output(self._common_pin, True)
            else:
                GPIO.output(self._common_pin, False)

    def dispose(self):
        self._terminated = True
        self._update_led()

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, value):
        self._on = value
        self._update_led()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if color not in COLORS:
            raise ValueError()
        self._color = color
        self._update_led()

import collections

SequenceContext = collections.namedtuple('SequenceContext', 'led parent')

class Sequence(object):
    def __init__(self):
        self._n_times = 1
        self._cycle = False
        self._actions = []

    def run(self, led):
        if self._cycle:
            actions = itertools.cycle(self._actions)
        else:
            actions = ncycles(self._actions, self._n_times)

        for action in actions:
            action(led)

    def on(self, color=None, color_seq=None, n_secs=None, off_secs=None):
        def action(led):

            if n_secs:
                on_seq = (
                    Sequence()
                        .on(color=color, color_seq=color_seq, n_secs=None)
                        .sleep(n_secs)
                        .off(off_secs)
                )
                on_seq.run(led)
                return

            if color_seq:
                led.color = next(color_seq)
            elif color:
                led.color = color

            led.on = True

        self._actions.append(action)
        return self

    def off(self, n_secs=None):
        def action(led):
            if n_secs:
                off_sequence = (
                    Sequence()
                        .off(n_secs=None)
                        .sleep(n_secs)
                        .on()
                )
                off_sequence.run(led)
            else:
                led.on = False

        self._actions.append(action)
        return self

    def sleep(self, n_secs):
        def action(__):
            time.sleep(n_secs)

        self._actions.append(action)
        return self

    def sequence(self, seq, n_times=1, cycle=False):
        def action(led):
            if cycle:
                repeating_seq = itertools.repeat(seq)
            else:
                repeating_seq = itertools.repeat(seq, n_times)

            for item in repeating_seq:
                item.run(led)

        self._actions.append(action)
        return self

    def blink(self, on_time=1, color=None, color_seq=None, off_time=None, n_times=None):
        off_time = off_time or on_time
        n_times = n_times or 0
        cycle = not bool(n_times)

        def action(led):
            blink_sequence = Sequence().on(
                color=color,
                color_seq=color_seq,
                n_secs=on_time,
                off_secs=off_time
            )

            if cycle:
                blink_sequence.cycle()
            else:
                blink_sequence.repeat(n_times)

            blink_sequence.run(led)

        self._actions.append(action)
        return self

    def cycle(self):
        self._cycle = True
        return self

    def repeat(self, n_times):
        self._n_times = n_times
        return self
