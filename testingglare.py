import math
import numpy as np
import cv2
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (3280,2464)
camera.start_preview()
sleep(1)
camera.stop_preview()
#Tar bilde og lager bildet som "im"
camera.capture('image0.jpg')
im = cv2.imread("image0.jpg")
#Bildet gjoeres mindre
reshape = cv2.resize(im, (820, 616))
output = reshape.copy()
gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)[1]

green = np.copy(output)

green[mask>0]=(0,128,0)

# Konverterer bildet fra RGB-farger til HSV, for bedre fargegjenkjenning
hsv = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
#Bildet blurres for å kunne finne sirkelkanter enklere
blurred = cv2.bilateralFilter(gray,10,30,75)
blue_blurred = blurred.copy()
red_blurred = blurred.copy()

#Fargedetection
#Blått deteksjonsområde
low_blue = np.array([90, 50, 2])
high_blue = np.array([126, 255, 255])

#Rødt deteksjonsområde
low_red = np.array([1, 100, 138])
high_red = np.array([25, 255, 255])

# Lager en "maske" som filtrerer bort alt i bildet bortsett fra det blå og det røde:
blue_mask = cv2.inRange(hsv, low_blue, high_blue)
red_mask = cv2.inRange(hsv, low_red, high_red)

#Lager en tom liste for rød og blå steiner
redstones = []
bluestones = []

#Her defineres noen variabler som brukes i sirkeldeteksjonen
minDist = 10
param1 = 300 #500
param2 = 10 #200 #smaller value-> more false circles
minRadius = 20
maxRadius = 26
#Selve sirkeldeteksjonen:
blue_circles = cv2.HoughCircles(blue_mask, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
red_circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

#Finner og definerer de blå sirklene:
if blue_circles is not None:
    blue_circles = np.round(blue_circles[0, :]).astype("int")
    for (x, y, r) in blue_circles:
        cv2.circle(green, (x, y), r, (0, 255, 0), 4)
        print(x,y, r, "blue")
        bluestones.append((x,y))


#Finner og definerer de røde sirklene:
if red_circles is not None:
    red_circles = np.round(red_circles[0, :]).astype("int")
    for (x, y, r) in red_circles:
        cv2.circle(green, (x, y), r, (0, 255, 0), 4)
        print(x,y, r, "red")
        redstones.append((x,y))


#Printer koordinatene til steinene:
print("The red stone coordinates are: ", redstones)
print("The blue stone coordinates are: ", bluestones)

#Definerer tomme lister for avstandssortering:
bluedist = []
reddist = []
resolution = [792,588]
#Definerer sentrum av boet som sentrum av bildet:
origo = [resolution[0] / 2, resolution[1] / 2]

#Finnner avstanden fra origo til blå steiner
for i in range(len(bluestones)):
    xdist = abs(bluestones[i][0]-origo[0])
    ydist = abs(bluestones[i][1]-origo[1])
    bluedist.append(math.sqrt(xdist**2 + ydist**2))

#Finnner avstanden fra origo til rød steiner
for i in range(len(redstones)):
    xdist = abs(redstones[i][0]-origo[0])
    ydist = abs(redstones[i][1]-origo[1])
    reddist.append(math.sqrt(xdist**2 + ydist**2))

#Kutter alle steiner som er lengre en 325 piksler unna origo, altså utafor boet.
bluedist[:] = [x for x in bluedist if x <= 252]
reddist[:] = [x for x in reddist if x <= 252]

#Sorterer etter avstand
bluedist.sort()
reddist.sort()

#Teller antall registrerte steiner
bluecount = len(bluedist)
redcount = len(reddist)

#Printer den sorterte lista for blå og rød
print("Blue stones distance, sorted:", bluedist)
print("Red stones distance, sorted:", reddist)

#Definerer tomme variabler for poeng:
bluepoints = 0
redpoints = 0
blueopen = True
redopen = True

#Litt logisk triksing: dersom det ikke er noen registrerte steiner er poengene 0.
if bluecount == 0  and redcount == 0:
    bluepoint = 0
    redpoint = 0
elif redcount == 0:
    bluepoints = len(bluedist)
elif bluecount == 0:
    redpoints = len(reddist)

#Dersom det er registrerte steiner skal de sammenliknes mellom blå og rød avstandsliste
#og deretter legges til i poeng.
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

#Printer poeng
print("Blue points:", bluepoints)
print("Red points:", redpoints)

#Viser alle bildene gjennom prossesseringsfasen.
green_resized = cv2.resize(green, (615,454))
cv2.imshow('blue', blue_mask)
cv2.imshow('red', red_mask)
cv2.imshow("output", output)
cv2.imshow("green", green_resized)
cv2.waitKey(0)
