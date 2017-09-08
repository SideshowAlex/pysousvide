import datetime
import uuid

import attrdict

INITIALIZED = 'INITIALIZED'
RAMP_UP = 'RAMP_UP'
CONTROL_LOOP = 'CONTROL_LOOP'
COMPLETE = 'COMPLETE'

RUN_STATES = (INITIALIZED, RAMP_UP, CONTROL_LOOP, COMPLETE)
