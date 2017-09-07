import contextlib
import time

from RPi import GPIO

RELAY_CONTROL = 'RELAY_CONTROL'

DEFAULT_PINS = {
    RELAY_CONTROL: 16,
}


@contextlib.contextmanager
def new_relay(pins=None):
    relay = Relay(pins, False)
    try:
        yield relay
    except Exception as ex:
        raise ex
    finally:
        relay._set_power(False, forced=True)


class Relay(object):

    def __init__(self, pins=None, initial_state=False):
        pins = pins or DEFAULT_PINS
        self.control_pin = pins.get(RELAY_CONTROL, DEFAULT_PINS[RELAY_CONTROL])
        self.state = initial_state
        self.last_switch = 0
        self._init()

    def _init(self):
        time.sleep(2)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.control_pin, GPIO.OUT)
        GPIO.output(self.control_pin, self.state)
        self.last_switch = time.time()
        time.sleep(2)

    @property
    def powered(self):
        return self.state

    @powered.setter
    def powered(self, state):
        self._set_power(state)

    def _set_power(self, state, forced=False):
        if state == self.state:
            return

        now = time.time()

        if not forced and now - self.last_switch < 2:
            raise ValueError('Too Frequent')

        self.state = state
        GPIO.output(self.control_pin, self.state)
        self.last_switch = now
