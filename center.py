import numpy as np
import cv2
import argparse
import cv2
import numpy as np
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (3280,2464)
camera.start_preview()
sleep(2)
camera.stop_preview()
#Tar bilde og lager bildet som "im"
camera.capture('center0.jpg')
im = cv2.imread("center0.jpg")
#Bildet gjoeres mindre
reshape = cv2.resize(im, (820, 616))
image = reshape.copy()

# convert image to grayscale image


bilateral_filtered_image = cv2.bilateralFilter(image, 5, 175, 175)

edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)

contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_list = []
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if ((len(approx) > 15) & (len(approx) < 35) & (area < 82000) & (area > 71000) ):
        contour_list.append(contour)

M = cv2.moments(contour_list[0])
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

print(cX)
print(cY)
cv2.drawContours(image, contour_list,  -1, (255,0,0), 2)
cv2.imshow('Objects Detected',image)
cv2.waitKey(0)
