import RPi.GPIO as gpio
import time
import sys
import tkinter as tk

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(7, gpio.OUT)
	gpio.setup(31, gpio.OUT)
	gpio.setup(33, gpio.OUT)
	gpio.setup(35, gpio.OUT)

def forward(tf):
	gpio.output(7, False)
	gpio.output(31, True)
	gpio.output(33, True)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def reverse(tf):
	gpio.output(7, True)
	gpio.output(31, False)
	gpio.output(33, False)
	gpio.output(35, True)
	time.sleep(tf)
	gpio.cleanup()

def turn_left(tf):
	gpio.output(7, True)
	gpio.output(31, True)
	gpio.output(33, True)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def turn_right(tf):
	gpio.output(7, False)
	gpio.output(31, True)
	gpio.output(33, False)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def pivot_right(tf):
	gpio.output(7, True)
	gpio.output(31, False)
	gpio.output(33, True)
	gpio.output(35, False)
	time.sleep(tf)
	gpio.cleanup()

def pivot_left(tf):
	gpio.output(7, False)
	gpio.output(31, True)
	gpio.output(33, False)
	gpio.output(35, True)
	time.sleep(tf)
	gpio.cleanup()

def key_input(event):
	init()
	print ('Key:', event.char)
	key_press = event.char
	sleep_time = 0.030

	if key_press.lower() == 'w':
		forward(sleep_time)
	elif key_press.lower() == 's':
		reverse(sleep_time)
	elif key_press.lower() == 'a':
		turn_left(sleep_time)
	elif key_press.lower() == 'd':
		turn_right(sleep_time)
	elif key_press.lower() == 'q':
		pivot_left(sleep_time)
	elif key_press.lower() == 'e':
		pivot_right(sleep_time)
	else:
		pass

command = tk.Tk()
command.blind('<KeyPress>', key_input)
command.mainloop()