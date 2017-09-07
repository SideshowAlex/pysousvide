import os
import subprocess as sp


def _device_file():
    os.system('sudo modprobe w1-gpio && sudo modprobe w1-therm')
    path = '/sys/bus/w1/devices'
    device_ids = (
        i for i in os.listdir(path)
        if os.path.isdir(os.path.join(path, i)) and i.startswith('28-')
    )
    device_id = next(device_ids)

    return '/sys/bus/w1/devices/{device_id}/w1_slave'.format(
        device_id=device_id
    )


class Probe(object):

    def __init__(self):
        self.device = _device_file()

    @property
    def temperature(self):
        pipe = sp.Popen(['cat', self.device], stdout=sp.PIPE)
        result = pipe.communicate()[0]
        result_list = result.split('=')
        temp_mC = int(result_list[-1])
        return temp_mC
