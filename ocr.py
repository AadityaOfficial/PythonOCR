from PIL import Image
import pytesseract
import argparse
import cv2
import os
import sys
ap=argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())
# load the example image and convert it to grayscale
img = cv2.imread(args["image"])
if img is None:
	print "None"
	sys.exit(0)
gaussian= cv2.GaussianBlur(img, (11,11), 25)
image = cv2.addWeighted(img, 1.5, gaussian, -0.5, 0, img)
cv2.imshow("Trial",image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)
# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)
# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
im=Image.open(filename)
text = pytesseract.image_to_string(im)
os.remove(filename)
print(text)
# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
cv2.waitKey(0)