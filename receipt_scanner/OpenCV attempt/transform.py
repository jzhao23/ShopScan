#### PACKAGES ####
from scipy.spatial import distance as dist
import numpy as np
import cv2

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

