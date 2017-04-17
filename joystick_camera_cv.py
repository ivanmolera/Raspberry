import sys
import time
import threading

import pygame
import pygame.camera

import RPi.GPIO as GPIO

from pyimagesearch.facedetector import FaceDetector
from pyimagesearch import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import cv2

import numpy

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

GPIO.setmode(GPIO.BOARD)

#LASER
laser = 36
GPIO.setup(laser, GPIO.OUT)
GPIO.output(laser, 1)

class Camera(object):
    def __init__(self):
        self.size = (640,480)

        # initialize the camera and grab a reference to the raw camera
        # capture
        self.camera = PiCamera()
        self.camera.resolution = self.size
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=self.size)

        # construct the face detector and allow the camera to warm
        # up
        self.fd = FaceDetector("cascades/haarcascade_frontalface_default.xml")
        time.sleep(0.1)

    def show_camera(self):
        # capture frames from the camera
        for f in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image
            self.frame = f.array

            # resize the frame and convert it to grayscale
            self.frame = imutils.resize(self.frame, width = 300)
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the image and then clone the frame
            # so that we can draw on it
            self.faceRects = self.fd.detect(self.gray, scaleFactor = 1.1, minNeighbors = 5,
                minSize = (30, 30))
            self.frameClone = self.frame.copy()

            # loop over the face bounding boxes and draw them
            for (fX, fY, fW, fH) in self.faceRects:
                cv2.rectangle(self.frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)

            # Desactivo el laser si detecto una cara
            if len(self.faceRects) > 0:
                GPIO.output(laser, 0)
            else:
                GPIO.output(laser, 1)

            # show our detected faces, then clear the frame in
            # preparation for the next frame
            #cv2.imshow("Face", self.frameClone)
            self.frame2 = self.rot180(numpy.rot90(self.frameClone))
            self.frame2 = pygame.surfarray.make_surface(self.frame2)
            screen.blit(self.frame2, (400,10))

            pygame.display.update()
            #pygame.display.flip()

            self.rawCapture.truncate(0)

    def rot180(self, frame):
        self.frame = frame
        return numpy.rot90(numpy.rot90(self.frame))


        

class Stepper(object):
    def __init__(self, eix_rotacio):
        self.eix_rotacio = eix_rotacio
        self.controlPin = []

        if self.eix_rotacio == "yaw":
            self.controlPin = [11, 12, 13, 15]
        elif self.eix_rotacio == "pitch":
            self.controlPin = [31, 32, 33, 35]

        for pin in self.controlPin:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        self.seq = [ [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1] ]

    def rotate(self, sentit_rotacio):
        self.sentit_rotacio = sentit_rotacio
        if sentit_rotacio != 0:
            for i in range(64):
                for halfstep in range(8):
                    for pin in range(4):
                        GPIO.output(self.controlPin[pin * self.sentit_rotacio], self.seq[halfstep][pin])
                    time.sleep(0.001)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def Print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

pygame.init()


# Set the width and height of the screen [width,height]
size = [710, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Robopot")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

cam = Camera()
#cam.show_camera()

def cam_thread():
    cam.show_camera()

t_cam = threading.Thread(target=cam_thread)
t_cam.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
t_cam.start()

yaw, pitch = 0, 0

stepperYaw = Stepper("yaw")
stepperPitch = Stepper("pitch")

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
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.Print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.Print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.Print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.Print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.Print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
        textPrint.unindent()
            
        buttons = joystick.get_numbuttons()
        textPrint.Print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.Print(screen, "Button {:>2} value: {}".format(i,button) )
        textPrint.unindent()
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.Print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.Print(screen, "Hat {} value: {}".format(i, str(hat)) )

            yaw = hat[0]
            pitch = hat[1]

            stepperYaw.rotate(yaw)
            stepperPitch.rotate(pitch)

        textPrint.unindent()
        
        textPrint.unindent()
    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    #pygame.display.flip()
    #pygame.display.update()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
GPIO.cleanup()