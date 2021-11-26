# -*- coding: utf-8 -*-
"""
Event Types
===========
Modified: 2021-04

Namespace to store the system event types

Dependencies:
-------------
```
from typing import Any, Callable, Dict, Union
from hwi.events.event import Event
from hwi.events.pipeline import Pipeline
```
Copyright © 2021 Incuvers. All rights reserved.
"""
import os
import time
import logging
import wiringpi
import numpy as np
from hwi.amqp.payloads import ISR
from hwi.icb.hardware import ICBHardware as hardware
from hwi.icb.hardware import ROT_ENC_TABLE
from hwi.events.registry import Registry as events


class RotaryEncoder:

    def __init__(self):
        """
        push_callback (function): callback function for push button click
        rotate_cw_callback (function): callback function for clockwise rotation
        rotate_ccw_callback (function): callback function for counter-clockwise rotation
        """
        self._logger = logging.getLogger(__name__)
        self.push_pin = hardware.PUSH_PIN  # reset pin on GPIO 10
        self.clk_pin = hardware.CLK_PIN
        self.dt_pin = hardware.DT_PIN
        self.push_state_multiplier = 5
        self.push_called = time.time()
        error_code = wiringpi.wiringPiSetupGpio()
        if error_code != 0:
            err_message = "Could not setup wiringPi, error code {}".format(error_code)
            self._logger.error(err_message)
            raise OSError(err_message)
        self._logger.info("wiringpi gpio setup successful")
        wiringpi.pinMode(self.push_pin, wiringpi.GPIO.INPUT)
        wiringpi.pinMode(self.clk_pin, wiringpi.GPIO.INPUT)
        wiringpi.pinMode(self.dt_pin, wiringpi.GPIO.INPUT)
        self._logger.info(
            "wiringpi pins %s, %s, and %s set to GPIO input",
            self.push_pin, self.clk_pin, self.dt_pin
        )
        wiringpi.pullUpDnControl(self.push_pin, wiringpi.GPIO.PUD_UP)
        wiringpi.pullUpDnControl(self.clk_pin, wiringpi.GPIO.PUD_UP)
        wiringpi.pullUpDnControl(self.dt_pin, wiringpi.GPIO.PUD_UP)
        self._logger.info(
            "wiringpi pins %s, %s, and %s set to GPIO pull up down control",
            self.push_pin, self.clk_pin, self.dt_pin)
        self.prev_state = wiringpi.digitalRead(self.clk_pin)
        self.prevNextCode = np.uint8(0)
        self.store = np.uint16(0)
        wiringpi.wiringPiISR(
            self.push_pin, wiringpi.GPIO.INT_EDGE_FALLING, self._push_filter_callback)
        wiringpi.wiringPiISR(
            self.clk_pin, wiringpi.GPIO.INT_EDGE_BOTH, self._rotate_filter_callback)
        wiringpi.wiringPiISR(
            self.dt_pin, wiringpi.GPIO.INT_EDGE_BOTH, self._rotate_filter_callback)
        self._logger.info(
            "wiringpi pins %s, %s, and %s set to GPIO ISRs %s, %s and %s respectively",
            self.push_pin, self.clk_pin, self.dt_pin, wiringpi.GPIO.INT_EDGE_FALLING,
            wiringpi.GPIO.INT_EDGE_BOTH, wiringpi.GPIO.INT_EDGE_BOTH
        )
        self._logger.info("Instantiation successful")

    def _read_rotary(self):
        """
        Reads the rotary instruction(s)
        :return: boolean
        """
        # disabling rotary functions if push knob depressed
        if wiringpi.digitalRead(self.push_pin) == 0:
            self.push_called = time.time()
            self._logger.debug("debouncing from push button")
            return 0
        clk_state = wiringpi.digitalRead(self.clk_pin)
        dt_state = wiringpi.digitalRead(self.dt_pin)
        self._logger.debug("saved digital read states for pins %s and %s",
                           self.clk_pin, self.dt_pin)
        self.prevNextCode <<= np.uint8(2)
        self.prevNextCode &= np.uint8(0x0f)  # just hold to the 4 LSB
        if (clk_state):
            self.prevNextCode |= np.uint8(0x02)
        if (dt_state):
            self.prevNextCode |= np.uint8(0x01)
        self.prevNextCode &= np.uint8(0x0f)  # just hold to the 4 LSB
        # If valid then store as 16 bit data.
        if (ROT_ENC_TABLE[self.prevNextCode]):
            self.store <<= np.uint16(4)
            self.store |= self.prevNextCode
            if (self.store & 0xff) == 0x2b:
                return 1
            if (self.store & 0xff) == 0x17:
                return -1
        return 0

    def _push_filter_callback(self):
        self._logger.debug("push button ISR callback triggered")
        push_state = wiringpi.digitalRead(self.push_pin)
        if time.time() - self.push_called > 0.4:
            if push_state == 0:
                self.publish_isr(ISR.PUSH)
        self.push_called = time.time()

    def _rotate_filter_callback(self):
        self._logger.debug("rotary ISR callback triggered")
        direction = self._read_rotary()
        if not direction == 0:
            if direction == 1:
                self.publish_isr(ISR.CW)
            elif direction == -1:
                self.publish_isr(ISR.CCW)

    def publish_isr(self, _type: ISR) -> None:
        events.amqp_publish.trigger(
            'topic/isr',
            {
                'type': _type
            }
        )
        self._logger.info("Published rotary encoder ISR for event type: %s", _type)


if __name__ == "__main__":
    knob = RotaryEncoder()
    print("reset monitor started...")
    while True:
        time.sleep(1000)
