import contextlib
import time

from RPi import GPIO
import Adafruit_CharLCD

LCD_RS = 'LCD_RS'
LCD_E = 'LCD_E'
LCD_DATA1 = 'LCD_DATA1'
LCD_DATA2 = 'LCD_DATA2'
LCD_DATA3 = 'LCD_DATA3'
LCD_DATA4 = 'LCD_DATA4'

DEFAULT_PINS = {
    LCD_RS: 25,
    LCD_E: 24,
    LCD_DATA1: 23,
    LCD_DATA2: 17,
    LCD_DATA3: 21,
    LCD_DATA4: 22,
}


LEFT, RIGHT = 0, 1
ROWS, COLUMNS = 2, 16


@contextlib.contextmanager
def new_lcd(pins=None):
    lcd = LCD(pins)
    try:
        yield lcd
    finally:
        lcd.dispose()


def get_pin(pins, pin_id):
    pins = pins or {}
    return pins.get(pin_id, DEFAULT_PINS[pin_id])


class LCD(object):
    def __init__(self, pins=None):
        self._driver = Adafruit_CharLCD.Adafruit_CharLCD(
            pin_rs=get_pin(pins, LCD_RS),
            pin_e=get_pin(pins, LCD_E),
            pins_db=[
                get_pin(pins, LCD_DATA1),
                get_pin(pins, LCD_DATA2),
                get_pin(pins, LCD_DATA3),
                get_pin(pins, LCD_DATA4),
            ],
        )
        self._driver.begin(COLUMNS, ROWS)
        self._on = True
        self._displayed_message = []
        self._buffer = []
        self._line_index = 0

    def dispose(self):
        self.on = False

    def _reset_buffer(self):
        self._buffer = []
        self._line_index = 0

    def _build_message(self):

        def get_lines():
            for index in xrange(0, ROWS):
                try:
                    buffer_line = self._buffer[self._line_index + index]
                    try:
                        yield buffer_line()
                    except TypeError:
                        yield buffer_line
                except IndexError:
                    yield ''
        message = '\n'.join([line[:COLUMNS] for line in get_lines()])
        self._displayed_message = message

    def _update_lcd(self):
        if self._on:
            self._driver.clear()
            self._driver.message(self._displayed_message)
            self._driver.display()
        else:
            self._driver.noDisplay()

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, value):
        self._on = value
        self._update_lcd()

    def clear(self):
        self._reset_buffer()
        self._build_message()
        self._update_lcd()

    @property
    def message(self):
        return '\n'.join(self.messages)

    @message.setter
    def message(self, value):
        self.messages = value.split('\n')

    @property
    def messages(self):
        return [line[0] for line in self._buffer]

    @messages.setter
    def messages(self, lines):
        self._line_index = 0
        self._buffer = [line for line in lines]
        self._build_message()
        self._update_lcd()

    @property
    def index(self):
        return self._line_index

    @index.setter
    def index(self, value):
        self._line_index = max(min(value, len(self._buffer) - 1), 0)
        self._build_message()
        self._update_lcd()

    def add_message(self, text):
        self._buffer.append(text)
        self._build_message()
        self._update_lcd()

    def up(self, n_items=1, loop=False):
        new_index = self.index - n_items

        if loop and new_index < 0:
            new_index = len(self._buffer) - 1
        self.index = new_index

    def down(self, n_items=1, loop=False):
        new_index = self.index + n_items

        if loop and new_index >= len(self._buffer):
            new_index = 0
        self.index = new_index

    def page_down(self, loop=False):
        self.down(ROWS, loop)

    def page_up(self, loop=False):
        self.up(ROWS, loop)

    def top(self):
        self.index = 0

    def bottom(self):
        self.index = len(self._buffer) - 1

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    with new_lcd() as a_lcd:
        a_lcd.clear()
        a_lcd.messages = [
            '123456789012345678901234567890',
            'abcdefghijklmnopqrstuvwxyz',
            lambda: 'foo {}'.format(time.time())
        ]
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(2)
        a_lcd.down(loop=True)
        time.sleep(10)

