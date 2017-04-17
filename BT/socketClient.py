"""
A simple Python script to send messages to a sever over Bluetooth using 
Python sockets (with Python 3.3 or above). 
"""

import socket

serverMACAddress = '5c:f3:70:65:b6:dd'
port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("192.168.1.194",50001))
while 1:
	text = input()
	if text == "quit":
		break
	s.send(bytes(text, 'UTF-8'))
s.close()
"""

import socket

UDP_IP = "192.168.2.15"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
"""