import contextlib

import lcd_logger
import led_logger
import logging_logger
import dweet_logger


LOGGERS = [
    lcd_logger.Logger,
    led_logger.Logger,
    logging_logger.Logger,
    dweet_logger.Logger,
]


@contextlib.contextmanager
def observers():
    loggers = [logger_cls() for logger_cls in LOGGERS]
    logger = Logger(loggers)
    try:
        yield logger
    finally:
        logger.dispose()


class Logger(object):
    def __init__(self, loggers):
        self._loggers = loggers

    def init_logger(self, manager):
        for logger in self._loggers:
            logger.init_logger(manager)

    def dispose(self):
        for logger in self._loggers:
            try:
                logger.dispose()
            except Exception:
                pass

    def log_run_start(self, run):
        for logger in self._loggers:
            try:
                logger.log_run_start(run)
            except Exception:
                pass

    def log_run_end(self, run):
        for logger in self._loggers:
            try:
                logger.log_run_end(run)
            except Exception:
                pass

    def log_ramp_up(self, measurement):
        for logger in self._loggers:
            try:
                logger.log_ramp_up(measurement)
            except Exception:
                pass

    def log_control_loop(self, measurement):
        for logger in self._loggers:
            try:
                logger.log_control_loop(measurement)
            except Exception:
                pass

