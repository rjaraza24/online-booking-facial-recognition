
# usage python3 face-encoding.py --dataset dataset --encodings encodings.pickle --detection-method hog

# import libraries
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# Parsing Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())


# Take pictures from dataset folder
print("[INFO] Gathering Face Model...")
imagePaths = list(paths.list_images(args["dataset"]))

# familiar face initialization
knownEncodings = []
knownNames = []

# loop in image directory
for (i, imagePath) in enumerate(imagePaths):
	# Retrieve the name of each folder
	print("[INFO] Processing images {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect (x,y) coordinates of face box
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# Face Processing
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop all encoding process
	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] Processing serialize encoding...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
