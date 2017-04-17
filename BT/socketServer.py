"""
A simple Python script to receive messages from a client over 
Bluetooth using Python sockets (with Python 3.3 or above). 
"""

import socket

hostMACAddress = '5c:f3:70:65:b6:dd' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
port = 3   # 3 is an arbitrary choice. However, it must match the port used by the client.  
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind(("192.168.2.15",50001))

s.listen(backlog)
try:
	client, address = s.accept()
	while 1:
		data = client.recv(size)
		if data:
			print(data)
			client.send(data)
except:	
	print("Closing socket")				
	client.close() 
	s.close()
"""
import socket

UDP_IP = "192.168.2.15"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data

"""