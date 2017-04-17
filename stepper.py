import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

controlPin = [11, 12, 13, 15]

for pin in controlPin:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)

seq = [ [1,0,0,0],
		[1,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,1,0],
		[0,0,1,1],
		[0,0,0,1],
		[1,0,0,1] ]

for i in range(512):
	for halfstep in range(8):
		for pin in range(4):
			GPIO.output(controlPin[pin], seq[halfstep][pin])
		time.sleep(0.001)

GPIO.cleanup()