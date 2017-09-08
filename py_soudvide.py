#!/usr/bin/env python

"""
Usage:
  py_sousvide.py.py [options] TARGET
  py_sousvide.py.py --version

Arguments:
  TARGET               sets the target temperature, in Celsius

Options:
  -h --help                  show this help message and exit
  --version                  show version and exit
  -p VALUE --prop=VALUE      set the prop constant
  -i VALUE --integral=VALUE  set the integral constant
  -b VALUE --bias=VALUE      set the bias constant
  -n NOTES --notes=NOTES     set notes about the run
  -r VALUE --ramp-up=VALUE   set the temperature tolerance for ramp up
"""
import uuid

from docopt import docopt

import logger
import controller_manager


def parse_command_line(version):
    arguments = docopt(__doc__, version=version)

    params = {}
    if arguments['TARGET'] is not None:
        params['target'] = float(arguments['TARGET'])

    if arguments['--bias'] is not None:
        params['bias'] = float(arguments['--bias'])

    if arguments['--prop'] is not None:
        params['prop'] = float(arguments['--prop'])

    if arguments['--integral'] is not None:
        params['integral'] = float(arguments['--integral'])

    if arguments['--ramp-up'] is not None:
        params['ramp_up'] = float(arguments['--ramp-up'])

    if arguments['--notes'] is not None:
        params['notes'] = arguments['--notes']

    return params


def main():
    manager = controller_manager.Manager(is_daemon=False)
    params = parse_command_line(manager.version)

    with logger.observers() as loggers:
        manager.loggers = loggers
        manager.start_run(**params)

if __name__ == '__main__':
    main()
