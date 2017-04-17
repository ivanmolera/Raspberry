import RPi.GPIO as gpio
import time

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(7, gpio.OUT)
	gpio.setup(31, gpio.OUT)
	gpio.setup(33, gpio.OUT)
	gpio.setup(35, gpio.OUT)

def forward(tf):
	init()
	gpio.output(7, False)
	gpio.output(31, True)
	gpio.output(33, True)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def reverse(tf):
	init()
	gpio.output(7, True)
	gpio.output(31, False)
	gpio.output(33, False)
	gpio.output(35, True)
	time.sleep(tf)
	gpio.cleanup()

def turn_left(tf):
	init()
	gpio.output(7, True)
	gpio.output(31, True)
	gpio.output(33, True)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def turn_right(tf):
	init()
	gpio.output(7, False)
	gpio.output(31, True)
	gpio.output(33, False)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def pivot_right(tf):
	init()
	gpio.output(7, True)
	gpio.output(31, False)
	gpio.output(33, True)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def pivot_left(tf):
	init()
	gpio.output(7, False)
	gpio.output(31, True)
	gpio.output(33, False)
	gpio.output(35, True)
	time.sleep(tf)
	gpio.cleanup()

forward(0.25)
reverse(0.25)
pivot_right(1)
pivot_left(1)
