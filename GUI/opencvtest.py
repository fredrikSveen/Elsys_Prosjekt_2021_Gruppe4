import math
import numpy as np
import cv2
from picamera import PiCamera
import serial
import time

#Globale variabler:
runder = 5
rundenr = 1
avsluttBool = False
stones = 0
winner = 1
winnerTeam = 2 # input fra openCV (Team Blue = 1, Team Orange = 2, uavgjort = 0)
points = 2 # Input fra openCV (antall poeng til winnerTeam, dersom uavgjort har ikke denne verdien noe å si)
totalStones = 6
stones1 = int(totalStones/2)
stones2 = int(totalStones/2)
camera = PiCamera()
camera.resolution = (3280,2464)

def takePoints():
    global winnerTeam
    global points
    global camera
    camera.start_preview()
    time.sleep(2)
    camera.stop_preview()
    camera.capture('image0.jpg')

    im = cv2.imread("image0.jpg")
    reshape = cv2.resize(im, (820, 616))
    output = reshape.copy()
    #gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    # Konverterer bildet fra RGB-farger til HSV, for bedre fargegjenkjenning
    hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
    #blurred = cv2.bilateralFilter(gray,10,30,75)
    #blue_blurred = blurred.copy()
    #red_blurred = blurred.copy()

    #Fargedetection
    #Blå range
    low_blue = np.array([94, 80, 1])
    high_blue = np.array([126, 255, 255])

    #Rød range
    low_red = np.array([1, 100, 130])
    high_red = np.array([255, 255, 255])

    # Lager en "maske" som filtrerer bort alt i bildet bortsett fra det blå:
    blue_mask = cv2.inRange(hsv, low_blue, high_blue)
    red_mask = cv2.inRange(hsv, low_red, high_red)

    redstones = []
    bluestones = []
    #redcount = 0
    #bluecount = 0

    minDist = 10
    param1 = 300 #500
    param2 = 16 #200 #smaller value-> more false circles
    minRadius = 27
    maxRadius = 35 #10
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
            #bluecount +=1

    if red_circles is not None:
        red_circles = np.round(red_circles[0, :]).astype("int")
        for (x, y, r) in red_circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print(x,y, r, "red")
            redstones.append((x,y))
            #redcount +=1
    print("The red stone coordinates are: ", redstones)
    print("The blue stone coordinates are: ", bluestones)
    #print("Red count: ", redcount)
    #print("Blue count: ", bluecount)


    bluedist = []
    reddist = []
    resolution = [820,616]
    origo = [resolution[0] / 2, resolution[1] / 2]

    for i in range(len(bluestones)):
        xdist = abs(bluestones[i][0]-origo[0])
        ydist = abs(bluestones[i][1]-origo[1])
        bluedist.append(math.sqrt(xdist**2 + ydist**2))

    for i in range(len(redstones)):
        xdist = abs(redstones[i][0]-origo[0])
        ydist = abs(redstones[i][1]-origo[1])
        reddist.append(math.sqrt(xdist**2 + ydist**2))

    bluedist[:] = [x for x in bluedist if x <= 325]
    reddist[:] = [x for x in reddist if x <= 325]

    bluedist.sort()
    reddist.sort()

    bluecount = len(bluedist)
    redcount = len(reddist)

    print("Blue stones distance, sorted:", bluedist)
    print("Red stones distance, sorted:", reddist)

    bluepoints = 0
    redpoints = 0
    blueopen = True
    redopen = True

    if bluecount == 0  and redcount == 0:
        bluepoints = 0
        redpoints = 0
    elif redcount == 0:
        bluepoints = len(bluedist)
    elif bluecount == 0:
        redpoints = len(reddist)

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

    #Functions available to show the picture qith red og blue mask
    reshape1 = cv2.resize(im, (410, 308))

    cv2.imshow('blue', blue_mask)
    cv2.imshow('red', red_mask)
    cv2.imshow("output", reshape1)
    cv2.waitKey(0)
    if bluepoints > 0:
        winnerTeam = 1
        points = bluepoints
        #pointsInTable(winnerTeam, bluepoints)
    elif redpoints > 0:
        winnerTeam = 2
        points = redpoints
        #pointsInTable(winnerTeam, redpoints)
    else:
        winnerTeam = 0
        points = 0

takePoints()