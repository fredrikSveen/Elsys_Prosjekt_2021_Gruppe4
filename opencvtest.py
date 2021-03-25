# import the necessary packages
#from email.mime import image
import math
import numpy as np
#import argparse
import cv2
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True, help = "Path to the image")
#args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
#image = cv2.imread(args["image"])
im = cv2.imread("image2.jpg")
reshape = cv2.resize(im, (820, 616))
output = reshape.copy()
gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
# Konverterer bildet fra RGB-farger til HSV, for bedre fargegjenkjenning
hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
blurred = cv2.bilateralFilter(gray,10,30,75)
blue_blurred = blurred.copy()
red_blurred = blurred.copy()

#Fargedetection
#Blå range
low_blue = np.array([94, 80, 1])
high_blue = np.array([126, 255, 255])

#Rød range
low_red = np.array([1, 100, 138])
high_red = np.array([255, 255, 255])

# Lager en "maske" som filtrerer bort alt i bildet bortsett fra det blå:
blue_mask = cv2.inRange(hsv, low_blue, high_blue)
red_mask = cv2.inRange(hsv, low_red, high_red)

redstones = []
bluestones = []
redcount = 0
bluecount = 0

minDist = 10
param1 = 300 #500
param2 = 14#200 #smaller value-> more false circles
minRadius = 26
maxRadius = 33 #10
blue_circles = cv2.HoughCircles(blue_mask, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
red_circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)


#contours_blue, h_blue = cv2.findContours(blue_mask,   cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#for cont in contours_blue:
  #  (blue_circle = cv2.)
#contours_red, h_red = cv2.findContours(red_mask,   cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# detect circles in the image
# ensure at least some circles were found
if blue_circles is not None:
    blue_circles = np.round(blue_circles[0, :]).astype("int")
    for (x, y, r) in blue_circles:
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        print(x,y, r, "blue")
        bluestones.append((x,y))
        bluecount +=1

if red_circles is not None:
    red_circles = np.round(red_circles[0, :]).astype("int")
    for (x, y, r) in red_circles:
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        print(x,y, r, "red")
        redstones.append((x,y))
        redcount +=1
print("The red stone coordinates are: ", redstones)
print("The blue stone coordinates are: ", bluestones)
print("Red count: ", redcount)
print("Blue count: ", bluecount)


bluedist = []
reddist = []
resolution = [820,616]
origo = [resolution[0] / 2, resolution[1] / 2]
#houselimit = Størrelsen på boet i piksler??

for i in range(len(bluestones)):
    xdist = abs(bluestones[i][0]-origo[0])
    ydist = abs(bluestones[i][1]-origo[1])
    bluedist.append(math.sqrt(xdist**2 + ydist**2))

for i in range(len(redstones)):
    xdist = abs(redstones[i][0]-origo[0])
    ydist = abs(redstones[i][1]-origo[1])
    reddist.append(math.sqrt(xdist**2 + ydist**2))


bluedist.sort()
reddist.sort()

print("Blue stones distance, sorted:", bluedist)
print("Red stones distance, sorted:", reddist)

bluepoints = 0
redpoints = 0
blueopen = True
redopen = True

if redcount == 0:
    bluepoints = len(bluestones)
if bluecount == 0:
    redpoints = len(redstones)

while min(len(bluedist), len(reddist)) > 0:
    if bluedist[0] < reddist[0] and blueopen:
        bluepoints += 1
        del bluedist[0]
        redopen = False
    elif bluedist[0] > reddist[0] and redopen:
        redpoints += 1
        del reddist[0]
        blueopen = False
    else:
        break

print("Blue points:", bluepoints)
print("Red points:", redpoints)

cv2.imshow('blue', blue_mask)
cv2.imshow('red', red_mask)
cv2.imshow("output", output)
cv2.waitKey(0)

#Colorpicker?

