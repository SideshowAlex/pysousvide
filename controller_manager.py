import datetime
import thread
import time
import uuid

import attrdict

import model
import logger
import controller

RUN_DEFAULTS = {
    'target': 65.0,
    'prop': 6.0,
    'integral': 9.0,
    'bias': 22.0,
    'notes': None,
    'ramp_up': 6.0,
}


def run_param(params, name):
    return params.get(name, RUN_DEFAULTS[name])


class Manager(object):
    name = 'PySousVide'
    version = '0.1.0'

    def __init__(self, is_daemon=False):
        self._run = None
        self._loggers = None
        self._controller = None
        self.is_daemon = is_daemon

    @property
    def loggers(self):
        return self._loggers

    @loggers.setter
    def loggers(self, loggers):
        self._loggers = loggers
        self._loggers.init_logger(self)

    def start_run(self, **params):

        if self._controller and self._controller.is_active:
            raise ValueError('Run in progress')

        pid_const_names = ('prop', 'integral', 'bias',)
        pid_constants = {
            k: run_param(params, k) for k in pid_const_names
        }
        run = attrdict.AttrDict(
            id=str(uuid.uuid4()),
            pid_constants=attrdict.AttrDict(**pid_constants),
            notes=run_param(params, 'notes'),
            target=run_param(params, 'target'),
            ramp_up_target=run_param(params, 'ramp_up'),
            start_time=datetime.datetime.now(),
            end_time=None,
            state=model.INITIALIZED,
        )
        self._run = run
        self._controller = controller.Controller(self._run, self._loggers)

        if self.is_daemon:
            thread.start_new_thread(self._controller.control, ())
        else:
            self._controller.control()

    def end_run(self):
        self._controller.is_active = False


if __name__ == '__main__':
    with logger.observers() as loggers:
        manager = Manager()
        manager.loggers = loggers
        time.sleep(10)
        manager.start_run(notes="Foo", target=24.0)
