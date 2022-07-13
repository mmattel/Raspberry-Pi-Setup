#!/usr/bin/python
# -*- coding: utf-8 -*-

# check the fan speed by:
# changing the PWM pin used
# changing value pairs for temp and speed
# use another shell to create load to see the impact
# use the final values in fan_control.py
# you also must have a minimum temp/0 speed pair that will definitely
# be reached coming from top down !

import RPi.GPIO as GPIO
import time
import sys
#import os

FAN_PIN = 18
WAIT_TIME = 1
PWM_FREQ = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)

fan=GPIO.PWM(FAN_PIN,PWM_FREQ)
fan.start(0);
i = 0

hyst = 1
tempSteps = [50, 70]
speedSteps = [0, 100]
cpuTempOld=0

try:
    while 1:
        fanSpeed=float(input("Fan Speed: "))
        fan.ChangeDutyCycle(fanSpeed)

except(KeyboardInterrupt):
    print("\rFan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()

