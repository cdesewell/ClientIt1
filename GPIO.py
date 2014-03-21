import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)

GPIO.output(13,True)
time.sleep(20)
GPIO.output(13,False)
GPIO.cleanup()
