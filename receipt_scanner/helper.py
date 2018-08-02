#### PACKAGES ####
from scipy.spatial import distance as dist
import numpy as np
import cv2
from skimage.filters import threshold_local
import imutils
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import pytesseract
import os

#pythagorean theorem, helper functions
def pythagorean(a, b):
	return np.sqrt((a ** 2) + (b ** 2))

#orders 4 points of a rectangle for the transform
#source: https://www.pyimagesearch.com/2016/03/21/ordering-coordinates-clockwise-with-python-and-opencv/
def order_points(pts): 
	#create list of coordinates from pts (list of four points of rectangle)
	#such that order will be:
	#1. top left corner (rect[0])
	#2. top right (rect[1])
	#3. bottom right (rect[2])
	#4. bottom left (rect[3])
	
	#sort pts by x values
	xSorted = pts[np.argsort(pts[:,0]), : ]

	#get the two left points in rectangle, and the two right points
	leftMost = xSorted[:2, : ]
	rightMost = xSorted[2:, : ]

	#separate top left and bottom left points
	leftMost = leftMost[np.argsort(leftMost[:, 1]), : ]
	(tl, bl) = leftMost

	#top right will be closer to to top left than bottom right, so can seperate those as well
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]

	return np.array([tl, tr, br, bl], dtype = "float32")

#compute the 4-pt transform
#source: https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def four_point_transform(image, pts):
	#image is the image to be transformed, pts are 4 points indicating ROI of the image
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	#compute max width of new img, the largest diff between tl-tr or bl-br corners
	widthA = pythagorean((tl[0] - tr[0]), (tl[1] - tr[1]))
	widthB = pythagorean((bl[0] - br[0]), (bl[1] - br[1]))
	maxWidth = max(int(widthA), int(widthB))

	#compute max height of new img, largest diff between tl-bl or tr-br corners
	heightA = pythagorean((tl[0] - bl[0]), (tl[1] - bl[1]))
	heightB = pythagorean((tr[0] - br[0]), (tr[1] - br[1]))
	maxHeight = max(int(heightA), int(heightB))

	#now we have dimensions of new image and can make new list to keep track of destination points
	dst = np.array([
		[0,0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	#use cv2 to apply perspective transform
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warped

def scan(image):
	#load and resize image (to improve edge detection)
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height = 500)

	#do some PIL touching up before cv2 conversions
	temp = Image.fromarray(image)

	temp.show()

	temp = temp.filter(ImageFilter.SHARPEN)
	temp = temp.filter(ImageFilter.CONTOUR)
	temp = temp.filter(ImageFilter.DETAIL)
	enhancer1 = ImageEnhance.Sharpness(temp)
	temp = enhancer1.enhance(2.0)

	temp.show()

	#convert image back from PIL to np array
	image_edited = np.array(temp)

	#image touch ups/conversions
	gray = cv2.cvtColor(image_edited, cv2.COLOR_BGR2GRAY)
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

	"""print("RESULTS:")
	cv2.imshow("Original", imutils.resize(orig, height = 650))
	cv2.imshow("Scanned", warped)
	cv2.waitKey(10000)"""

	cv2.imwrite("/Users/jasonzhao/Downloads/pic_example.jpg", warped)
	return warped

#perform OCR (takes in pre-processed image from scan)
def ocr(image):
	#make temp file to conduct OCR
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, image)

	#apply OCR then delete temp file
	edited_img = Image.open(filename)
	edited_img = edited_img.filter(ImageFilter.DETAIL)
	edited_img = edited_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	edited_img = edited_img.filter(ImageFilter.SHARPEN)
	enhancer1 = ImageEnhance.Sharpness(edited_img)
	enhancer2 = ImageEnhance.Contrast(edited_img)
	enhancer3 = ImageEnhance.Brightness(edited_img)
	edited_img = enhancer1.enhance(2.0)
	edited_img = enhancer2.enhance(2.0)
	edited_img = enhancer3.enhance(2.0)
	text = pytesseract.image_to_string(edited_img, config='--psm 6')
	os.remove(filename)
	print(text)

	# show the output images
	cv2.imshow("Output", image)
	cv2.waitKey(5000)

	return text



