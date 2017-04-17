#imports
import argparse
import datetime
import imutils
import time
import cv2

#arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="video path")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# reading from video
else:
	camera = cv2.VideoCapture(args["video"])

# init first frame
firstFrame = None

# loop frames
while True:
	
	# grab current frame
	(grabbed, frame) = camera.read()
	text = "Unoccupied"


	# end of file
	if not grabbed:
		break;

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	# escala de grisos
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# fem un desenfoque gausiano per suavitzar les diferències entre dos frames consecutius
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	# assumim que el primer frame és el fons sense moviment
	if firstFrame is None:
		firstFrame = gray
		continue

	# absolute difference between first frame anb current frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	# pixels amb una diferència d'intensitat > 25
	thresh = cv2.threshold(frameDelta, 40, 255, cv2.THRESH_BINARY)[1]

	# dilate threshold image to fill in holes, then find contours
	thresh = cv2.dilate(thresh, None, iterations=2)
	#(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	_, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# loop over contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame, and update text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
		text = "Occupied"

	# draw text and timestamp on the frame
	cv2.putText(frame, "Room status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)



	# show the frame
	cv2.imshow("Security feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# q break the loop
	if key == ord("q"):
		break

#cleanup the camera and close windows
camera.release()
cv2.destroyAllWindows()


