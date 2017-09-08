import logging
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import dweepy
import utils

DEVICE_ID = 'pysousvide'


def dweet(**payload):
    while True:
        try:
            dweepy.dweet_for(DEVICE_ID, payload)
            break
        except dweepy.DweepyError as ex:
            if not ex.message.startswith('Rate limit exceeded'):
                pass
        except Exception:
            pass


class Logger(object):

    def __init__(self):
        self.controller = None
        self.run = None

    def dispose(self):
        pass

    def init_logger(self, controller):
        print "Follow me at http://dweet.io/follow/{}".format(DEVICE_ID)
        self.controller = controller
        dweet(
            controller="{c.name} {c.version}".format(c=self.controller),
            wlan_ip=utils.inet_address('wlan0'),
        )

    def log_run_start(self, run):
        self.run = run
        dweet(
            controller="{c.name} {c.version}".format(c=self.controller),
            wlan_ip=utils.inet_address('wlan0'),
            target='{} C'.format(self.run.target),
        )

    def log_run_end(self, run):
        pass

    def log_ramp_up(self, measurement):
        dweet(
            controller="{c.name} {c.version}".format(c=self.controller),
            wlan_ip=utils.inet_address('wlan0'),
            version=self.controller.version,
            target='{} C'.format(self.run.target),
            state='Warm up',
            update_time=measurement.timestamp.strftime('%x %X'),
            temperature=measurement.temperature,
            relay_state='on' if measurement.relay else 'off',
        )

    def log_control_loop(self, measurement):
        dweet(
            target='{} C'.format(self.run.target),
            state='Holding',
            update_time=measurement.timestamp.strftime('%x %X'),
            temperature=measurement.temperature,
            relay_state='on' if measurement.relay else 'off',
            power=measurement.control_info.power,
            control_loop_temperature=measurement.control_info.temperature,
            control_loop_index=measurement.control_info.index,
        )
