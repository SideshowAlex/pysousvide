#!/usr/bin/env python

import relay
from RPi import GPIO
import sys
import os.path as path


def main():

    if len(sys.argv) > 1:
        state = sys.argv[1]
        if state not in ('on', 'off'):
            state = None
    else:
        state = None

    if not state:
        usage()
        return

    initial_state = (state == 'on')
    a_relay = relay.Relay(initial_state=initial_state)

def usage():
    print "Usage: "
    print "  {} (on|off)".format(path.basename(sys.argv[0]))


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    try:
        main()
    except KeyboardInterrupt:
        pass
