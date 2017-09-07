
import datetime
import temperature_probe
import relay
import time
import model


class Controller(object):
    def __init__(self, run, logger):
        self._run = run
        self.probe = temperature_probe.Probe()
        self.relay = relay.Relay()
        self.int_error = 0
        self.logger = logger
        self.is_active = True

    def control(self):
        self.logger.log_run_start(self._run)
        while self.is_active:
            state = self._run.state
            if state == model.INITIALIZED:
                new_state = self.initialize()
            elif state == model.RAMP_UP:
                new_state = self.ramp_up()
            elif state == model.CONTROL_LOOP:
                new_state = self.control_loop()

            if new_state != state:
                self._run.state = new_state
                self._run.save()

        self._run.state = model.COMPLETE
        self._run.save()
        self.relay.powered = False
        self.logger.log_run_end(self._run)

    def initialize(self):
        return model.RAMP_UP

    def control_loop(self):
        temperature = self.probe.temperature
        temperature_c = temperature / 1000.0
        target = self._run.target * 1000.0

        error = target - temperature
        self.int_error += error
        B = self._run.pid_constants.bias
        I = self._run.pid_constants.integral
        P = self._run.pid_constants.prop
        power = B + ((P * error) + ((I * self.int_error)/100))/100


        # Long duration pulse width modulation
        for x in range(1, 100):
            powered = power > x
            self.relay.powered = powered

            measurement = model.Measurement(
                run=self._run,
                state=self._run.state,
                temperature=self.probe.temperature / 1000.0,
                relay=self.relay.powered,
                control_info=model.ControlLoopData(
                    loop_start=datetime.datetime.now(),
                    temperature=temperature_c,
                    power=power,
                    index=x,
                )
            )
            measurement.save()
            self.logger.log_control_loop(measurement)
            time.sleep(2)
        return model.CONTROL_LOOP

    def ramp_up(self):
        rampup_tolerance = self._run.ramp_up_target

        temperature = self.probe.temperature
        temperature_c = temperature / 1000.0
        if self._run.target - temperature_c < rampup_tolerance:
            return model.CONTROL_LOOP

        self.relay.powered = True

        measurement = model.Measurement(
            run=self._run,
            state=self._run.state,
            temperature=temperature_c,
            relay=self.relay.powered,
        )
        measurement.save()
        self.logger.log_ramp_up(measurement)
        time.sleep(15)
        return model.RAMP_UP



