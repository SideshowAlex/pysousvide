import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Logger(object):

    def __init__(self):
        pass

    def dispose(self):
        pass
        self.led.dispose()

    def init_logger(self, controller):
        logger.info('Starting {} - {}'.format(controller.name, controller.version))

    def log_run_start(self, run):
        logger.info('Run started: {r.id}'.format(r=run))

    def log_run_end(self, run):
        logger.info('Run stopped: {r.id}'.format(r=run))

    def log_ramp_up(self, measurement):
        logger.info(
            '{m.state} - Temperature: {m.temperature}, Relay: {m.relay}'.format(
                m=measurement
            )
        )

    def log_control_loop(self, measurement):
        logger.info(
            '{m.state} - Temperature: {m.temperature}, Control Temperature: {c.temperature}, Relay: {m.relay}, Power: {c.power}, Index: {c.index}'.format(
                m=measurement,
                c=measurement.control_info
            )
        )
