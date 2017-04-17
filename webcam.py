# USAGE
# python webcam.py --face cascades/haarcascade_frontalface_default.xml

# import the necessary packages
from pyimagesearch.facedetector import FaceDetector
from pyimagesearch import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import time
import cv2

import sys
import threading
import numpy
import RPi.GPIO as GPIO
import pygame

GPIO.setmode(GPIO.BOARD)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

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
            self.frame = self.rot180(imutils.resize(self.frame, width = 300))
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
            cv2.imshow("Robopot", self.frameClone)

            self.rawCapture.truncate(0)

            # if the 'q' key is pressed, stop the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

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


# CAMERA
cam = Camera()

def cam_thread():
    cam.show_camera()

t_cam = threading.Thread(target=cam_thread)
t_cam.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
t_cam.start()

# STEPPERS
stepperYaw = Stepper("yaw")
stepperPitch = Stepper("pitch")


# PYGAME
pygame.init()

# Set the width and height of the screen [width,height]
size = [710, 700]
pygame.display.set_caption("Robopot")
screen = pygame.display.set_mode(size)

screen.fill(WHITE)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

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

        stepperYaw.rotate(yaw)
        stepperPitch.rotate(pitch)

pygame.quit ()
GPIO.cleanup()
