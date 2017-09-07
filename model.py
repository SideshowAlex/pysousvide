import datetime
import uuid

import mongoengine

INITIALIZED = 'INITIALIZED'
RAMP_UP = 'RAMP_UP'
CONTROL_LOOP = 'CONTROL_LOOP'
COMPLETE = 'COMPLETE'

RUN_STATES = (INITIALIZED, RAMP_UP, CONTROL_LOOP, COMPLETE)


class PidConstants(mongoengine.EmbeddedDocument):
    prop = mongoengine.FloatField()
    integral = mongoengine.FloatField()
    bias = mongoengine.FloatField()


class Run(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    start_time = mongoengine.DateTimeField(default=datetime.datetime.now)
    end_time = mongoengine.DateTimeField()
    state = mongoengine.StringField(choices=RUN_STATES, default=INITIALIZED)
    target = mongoengine.FloatField()
    ramp_up_target = mongoengine.FloatField()
    pid_constants = mongoengine.EmbeddedDocumentField(PidConstants)
    notes = mongoengine.StringField()


class ControlLoopData(mongoengine.EmbeddedDocument):
    loop_start = mongoengine.DateTimeField(default=datetime.datetime.now)
    index = mongoengine.IntField()
    temperature = mongoengine.FloatField()
    power = mongoengine.IntField()


class Measurement(mongoengine.Document):
    run = mongoengine.ReferenceField(Run, reverse_delete_rule=mongoengine.CASCADE)
    timestamp = mongoengine.DateTimeField(default=datetime.datetime.now)
    temperature = mongoengine.FloatField()
    relay = mongoengine.BooleanField()
    control_info = mongoengine.EmbeddedDocumentField(ControlLoopData)
    state = mongoengine.StringField()
