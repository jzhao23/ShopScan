import helper as h
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image to be scanned")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

if __name__ == "__main__":
	preprocessed = h.scan(image)
	rough_text = h.ocr(preprocessed)
