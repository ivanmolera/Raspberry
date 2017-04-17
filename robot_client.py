# CLIENT
import socket
import sys
import pygame

UDP_IP = "192.168.2.15"
UDP_PORT = 5005



# PYGAME
pygame.init()

# JOYSTICK
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

hat = joystick.get_hat(0)

done = False
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")

        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            done = True

    hats = joystick.get_numhats()

    for i in range( hats ):
        hat = joystick.get_hat( i )

        yaw = hat[0]
        pitch = hat[1]

        if yaw != 0:
            MESSAGE = "Hello, World!"

            print ("UDP target IP:", UDP_IP)
            print ("UDP target port:", UDP_PORT)
            print ("message:", MESSAGE)

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


pygame.quit ()
