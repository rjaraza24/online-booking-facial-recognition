
# usage python3 face-recognition-video-2.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle --door1 14 --door2 17

# import libraries needed
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import requests
import RPi.GPIO as GPIO

# Parsing Argument
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d1", "--door1", required=True,
	help="path to gpio port of door lock 1")
ap.add_argument("-d2", "--door2", required=True,
	help="path to gpio port of door lock 2")
args = vars(ap.parse_args())

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
l1 = int(args["door1"]) # 4
l2 = int(args["door2"]) # 17
# l1 = 4 # 4
# l2 = 17 # 17

GPIO.setup(l1, GPIO.OUT) # Door Lock 1
GPIO.setup(l2, GPIO.OUT) #pin gpio17
# Create PWM channel on the servo pin with a frequency of 50Hz
pwm_servo = GPIO.PWM(l2, 50)
pwm_servo.start(2.5)
#pwm_servo.ChangeDutyCycle(0)

# load face detection from OpenCV cascade file
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

# Camera Initialization
print("[INFO] Webcam and Raspi Camera Initializing...")
vs = VideoStream(src=1).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# Start FPS Counter(Frame per Second)
fps = FPS().start()

# loop of all frames obtained
while True:
# get the frame, and resize to 500pixel to make it faster
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

	# RGB Conversion into Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# face detection from grayscale frames
        rects = detector.detectMultiScale(gray, scaleFactor=1.1,
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

   # Show squares on detected faces
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
#        pwm_servo.ChangeDutyCycle(0)

	# loop on all detected faces
        for encoding in encodings:
           matches = face_recognition.compare_faces(data["encodings"],encoding)
           name = "Unknown Person"

		# check if there is a recognized face
           if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        for i in matchedIdxs:
                               name = data["names"][i]
				#name = "booker"
                               counts[name] = counts.get(name, 0) + 1
                        name = max(counts, key=counts.get)
                        if name == "door1":
#                                print("Door Lock 1 ON")
#                                time.sleep(1)
#                                GPIO.output(l1, GPIO.LOW)
#                                time.sleep(2) # Door Lock 1
#                                GPIO.output(l1, GPIO.HIGH)
#                                print("Door Lock 1 OFF")
                                #time.sleep(1)
                                pwm_servo.ChangeDutyCycle(7.5)
                                print("Door Lock 1 ON")
#				GPIO.setup(int(args["door2"]), GPIO.OUT) # Door Lock 2
			  # turn towards 90 degrees
                                time.sleep(2) # sleep 1 second
                                pwm_servo.ChangeDutyCycle(2.5)
#                                pwm_servo.ChangeDutyCycle(0)
                                print("Door Lock 1 OFF")
                                time.sleep(1)

                        elif name == "door2":
#                                 pwm_servo.ChangeDutyCycle(12.5)
#                                 print("Door Lock 2 ON")
# #				GPIO.setup(int(args["door2"]), GPIO.OUT) # Door Lock 2
# 			  # turn towards 90 degrees
#                                 time.sleep(2) # sleep 1 second
#                                 pwm_servo.ChangeDutyCycle(2.5)
# #                                pwm_servo.ChangeDutyCycle(0)
#                                 print("Door Lock 2 OFF")
#                                 time.sleep(1)
#				GPIO.setup(int(args["door2"]), GPIO.IN)

           names.append(name)

	# loop on all familiar faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
		# tampilkan nama di wajah yang di kenali
                cv2.rectangle(frame, (left, top), (right, bottom),
                    (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

	# Show image on screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

	# wait for button 1 to exit
        if key == ord("q"):
             break

	# update FPS
        fps.update()

# show FPS info
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# cleanup
cv2.destroyAllWindows()
vs.stop()
#vs2.stop()
