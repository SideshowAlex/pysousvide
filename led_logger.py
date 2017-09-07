import thread

import led


class Logger(object):

    def __init__(self):
        self.led = led.LED()
        self.alive = True
        self.run = None
        self.measurement = None
        self.state = None

    def lights(self):
        while True:
            run = self.run
            measurement = self.measurement
            if not run:
                yield led.RED
            elif run.state == 'RAMP_UP':
                yield led.YELLOW
            else:
                yield led.GREEN

            if not run or not measurement:
                yield led.RED
            elif measurement.relay:
                yield led.GREEN
            else:
                yield led.YELLOW

            if not measurement or not run:
                yield led.RED
            elif -0.5 <= measurement.temperature - run.target <= 0.5:
                yield led.GREEN
            elif measurement.temperature < run.target:
                yield led.YELLOW
            else:
                yield led.RED

    def blinker(self):
        colors = self.lights()

        while True:
            if self.run:
                sequence = (
                    led.Sequence()
                        .on(color_seq=colors, n_secs=.66, off_secs=.33)
                        .on(color_seq=colors, n_secs=.66, off_secs=.33)
                        .on(color_seq=colors, n_secs=.66)
                        .off(n_secs=1.33)
                )
            else:
                sequence = (
                    led.Sequence()
                        .on(color_seq=colors, n_secs=.17, off_secs=.17)
                        .on(color_seq=colors, n_secs=.17, off_secs=.17)
                        .on(color_seq=colors, n_secs=.17)
                        .off(n_secs=4.17)
                )
            sequence.run(self.led)

    def dispose(self):
        self.led.dispose()

    def init_logger(self, controller):
        self.state = 'CONTROLLER_INIT'
        thread.start_new_thread(self.blinker, ())

    def log_run_start(self, run):
        self.run = run
        self.state = 'RUN_INIT'

    def log_run_end(self, run):
        self.run = None
        self.state = 'COMPLETE'

    def log_ramp_up(self, measurement):
        self.measurement = measurement

    def log_control_loop(self, measurement):
        self.measurement = measurement
