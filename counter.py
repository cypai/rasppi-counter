#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

button_in = 36
led_outs = [7, 11, 13, 15]

counter = 0
count_max = 15

def setup():
    GPIO.setmode(GPIO.BOARD)
    for led_out in led_outs:
        GPIO.setup(led_out, GPIO.OUT)
        GPIO.output(led_out, GPIO.LOW)
    GPIO.setup(button_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_in, GPIO.FALLING, callback=increment_counter, bouncetime=200)

def increment_counter(ev=None):
    counter += 1
    if counter > count_max:
        counter = 0
    adjust_leds(counter)

def adjust_leds(number):
    led_states = []
    k = number
    current_binary = 2**(len(led_outs) - 1)

    while current_binary > 0:
        if k > current_binary:
            led_states.append(GPIO.HIGH)
            k -= current_binary
        else:
            led_states.append(GPIO.LOW)
        current_binary /= 2

    for i in range(len(led_outs)):
        GPIO.output(led_outs[i], led_states[i])

if __name__ == '__main__':
    setup()
    try:
        while True:
            time.sleep(1)
    except:
        GPIO.cleanup()
