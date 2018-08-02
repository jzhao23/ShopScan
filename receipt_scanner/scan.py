#### PACKAGES ####
from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

#construct argument parser, parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image to be scanned")
args = vars(ap.parse_args())

#load and resize image (to improve edge detection)
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

#image touch ups/conversions
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

#find all contours in the touched up image and keep only the largest ones
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

#loop over largest contours, pick largest contour with 4 points
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

#top-down transform, convert to grayscale and threshold it
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255 #turn array into image
if (warped.shape[0] < warped.shape[1]):
	warped = cv2.rotate(warped, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)

print("RESULTS:")
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", warped)
cv2.imwrite("/Users/jasonzhao/Downloads/pic_example.jpg", warped)
cv2.waitKey(0) 

