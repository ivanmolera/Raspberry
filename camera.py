import pygame
from pygame.locals import *
import cv2
import numpy

color=False#True#False
camera_index = 0
camera=cv2.VideoCapture(camera_index)
camera.set(3,640)
camera.set(4,480)

#This shows an image the way it should be
cv2.namedWindow("w1",cv2.WINDOW_AUTOSIZE)
retval,frame=camera.read()
if not color:
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
cv2.flip(frame,1,frame)#mirror the image
cv2.imshow("w1",frame)

#This shows an image weirdly...
screen_width, screen_height = 640, 480
screen=pygame.display.set_mode((screen_width,screen_height))

def getCamFrame(color,camera):
    retval,frame=camera.read()
    if not color:
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame=numpy.rot90(frame)
    frame=pygame.surfarray.make_surface(frame) #I think the color error lies in this line?
    return frame

def blitCamFrame(frame,screen):
    screen.blit(frame,(0,0))
    return screen

screen.fill(0) #set pygame screen to black
frame=getCamFrame(color,camera)
screen=blitCamFrame(frame,screen)
pygame.display.flip()

running=True
while running:
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == KEYDOWN:
            running=False
pygame.quit()
cv2.destroyAllWindows()