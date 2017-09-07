import RPi.GPIO as GPIO
import time
import random
red_pin = 18
green_pin =23 
blue_pin = 24 
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
pwm_red = GPIO.PWM(red_pin, 500)
pwm_blue = GPIO.PWM(blue_pin, 500)
pwm_green = GPIO.PWM(green_pin, 500)
pwm_red.start(100)
pwm_green.start(100)
pwm_red.start(100)
try:
   while True:
      pwm_red.ChangeDutyCycle(random.randint(0,100))
      pwm_green.ChangeDutyCycle(random.randint(0,100))
      pwm_blue.ChangeDutyCycle(random.randint(0,100))
      time.sleep(0.2)
except:
    GPIO.cleanup()
