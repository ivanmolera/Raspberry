"""
A simple Python script to send messages to a sever over Bluetooth 
using PyBluez (with Python 2).
"""

import bluetooth

serverMACAddress = '5c:f3:70:65:b6:dd'
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
	text = input() # Note change to the old (Python 2) raw_input
	if text == "quit":
		break
	s.send(text)
sock.close()