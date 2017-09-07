import datetime
import thread
import time

import lcd
import utils


class Logger(object):

    def __init__(self):
        self.lcd = lcd.LCD()
        self.alive = True
        self.run = None
        self.measurement = None
        self.state = None
        self.controller = None

    def dispose(self):
        self.lcd.dispose()

    def init_logger(self, controller):
        self.state = 'CONTROLLER_INIT'
        self.controller = controller
        self.lcd.messages = self.idle_messages()
        thread.start_new_thread(self.scroller, ())

    def log_run_start(self, run):
        self.run = run
        self.state = 'RUN_INIT'

    def log_run_end(self, run):
        self.run = None
        self.lcd.messages = self.idle_messages()
        self.state = 'COMPLETE'

    def log_ramp_up(self, measurement):
        self.measurement = measurement
        if self.state != self.run.state:
            self.lcd.messages = self.ramp_up_messages()
            self.state = self.run.state

    def log_control_loop(self, measurement):
        self.measurement = measurement
        if self.state != self.run.state:
            self.lcd.messages = self.control_loop_messages()
            self.state = self.run.state

    def scroller(self):
        while self.alive:
            self.lcd.page_down(loop=True)
            time.sleep(2)

    def idle_messages(self):
        return [
            self.controller.name,
            'v' + self.controller.version,
            'wlan0 IP:',
            utils.inet_address('wlan0')
        ]

    def control_loop_messages(self):
        return [
            'Holding',
            lambda: datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'),
            lambda: 'Temp: {}'.format(self.measurement.temperature),
            lambda: 'Ctrl: {}'.format(self.measurement.control_info.temperature),
            lambda: 'Target: {}'.format(self.run.target),
            lambda: 'Relay: {}'.format('on' if self.measurement.relay else 'off'),
            lambda: 'Power: {}'.format(self.measurement.control_info.power),
            lambda: 'Index: {}'.format(self.measurement.control_info.index),
            'wlan0 IP:',
            utils.inet_address('wlan0')
        ]

    def ramp_up_messages(self):
        return [
            'Warm Up',
            lambda: datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'),
            lambda: 'Temp: {}'.format(self.measurement.temperature),
            lambda: 'Target: {}'.format(self.run.target),
            lambda: 'Relay: {}'.format('on' if self.measurement.relay else 'off'),
            '',
            'wlan0 IP:',
            utils.inet_address('wlan0'),
        ]

