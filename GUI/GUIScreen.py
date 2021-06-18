#!/usr/bin/env python3

from tkinter import Button, Label, Tk, Entry, END, PhotoImage, NW, Canvas, BOTH
from PIL import ImageTk,Image
from math import floor
from itertools import count
window = Tk()
window.title("Curling game")
window.geometry('800x480')
# import the necessary packages
import math
import numpy as np
import cv2
from picamera import PiCamera
import serial
import time
import spidev
import RPi.GPIO as GPIO
window.config(bg='hot pink')
window.iconphoto(False, PhotoImage(file="/home/pi/Elsys_Prosjekt_2021_Gruppe4/GUI/Images/yellowStone.png"))

#Globale variabler:
runder = 2
rundenr = 1
avsluttBool = False
stones = 0
winner = 1
winnerTeam = 2 # input fra openCV (Team Blue = 1, Team Orange = 2, uavgjort = 0)
points = 2 # Input fra openCV (antall poeng til winnerTeam, dersom uavgjort har ikke denne verdien noe å si)
camera = PiCamera()
camera.resolution = (3280,2464)
stonesPer = 1
stones1 = stonesPer
stones2 = stonesPer
sc1=0
sc2=0
aktivknapp = "forest green"
oransjefarge = "darkorange3"
knapp = "limegreen"
bakgrunn = "palegreen"
logo = Image.open("/home/pi/Elsys_Prosjekt_2021_Gruppe4/GUI/Images/logoTrans.png")
pinkL = Image.open("/home/pi/Elsys_Prosjekt_2021_Gruppe4/GUI/Images/persusPink2.png")
blueStone = Image.open("/home/pi/Elsys_Prosjekt_2021_Gruppe4/GUI/Images/plueStone.png")
orangeStone = Image.open("/home/pi/Elsys_Prosjekt_2021_Gruppe4/GUI/Images/orangeStone.png")
#gif = Image.open("/Users/Lillemina/Elsys_Prosjekt_2021_Gruppe4/GUI/curlingGif.gif", format="gif -index 2")
#filGif = 'GUI\Images\curlingGifTheOneAndOnly.gif'
curlingStones = Image.open("/home/pi/Elsys_Prosjekt_2021_Gruppe4/GUI/Images/curlingStones.png")
filConfetti = "/home/pi/Elsys_Prosjekt_2021_Gruppe4/GUI/Images/confetti.gif" 
bluePoints = 0
orangePoints = 0
name1 = "Blått Lag"
name2 = "Oransje Lag"
stoneLeft = "Stein igjen"
stonesLeft = "Steiner igjen"
origo = [0,0]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

value1=0
value2=0
#pinkL = Image.open("/Users/Lillemina/Elsys_Prosjekt_2021_Gruppe4/GUI/pinkLightning.png")

pos1x=0.03 #X-koordinat til Team Blue tekst
pos1y=0.2 #Y-koordinat til team blue og team orange tekst
pos2x=0.57 #X-koordinat til Team Orange tekst
pos3x=0.02 #X-koordinat til Team Blue stones tekst
pos3y=0.4 #Y-koordinat til team blue og team orange stones tekst
pos4x = 0.6 #X-koordinat til Team Orange stones tekst

# Lager liste med resultater
table = list(range(12))
for i in range(0,12):
    cols = list(range(3))
    cols[0] = str(i)        
    cols[1] = ''
    cols[2] = ''
    table[i] = cols
table[0][0] = "Lag/Runde"
table[0][1] = name1
table[0][2] = name2


class MCP3201(object):
    """
    Functions for reading the MCP3201 12-bit A/D converter using the SPI bus either in MSB- or LSB-mode
    """
    def __init__(self, SPI_BUS, CE_PIN):
        """
        initializes the device, takes SPI bus address (which is always 0 on newer Raspberry models)
        and sets the channel to either CE0 = 0 (GPIO pin BCM 8) or CE1 = 1 (GPIO pin BCM 7)
        """
        if SPI_BUS not in [0, 1]:
            raise ValueError('wrong SPI-bus: {0} setting (use 0 or 1)!'.format(SPI_BUS))
        if CE_PIN not in [0, 1]:
            raise ValueError('wrong CE-setting: {0} setting (use 0 for CE0 or 1 for CE1)!'.format(CE_PIN))
        self._spi = spidev.SpiDev()
        self._spi.open(SPI_BUS, CE_PIN)
        self._spi.max_speed_hz = 976000
        pass

    def readADC_MSB(self):
        """
        Reads 2 bytes (byte_0 and byte_1) and converts the output code from the MSB-mode:
        byte_0 holds two ?? bits, the null bit, and the 5 MSB bits (B11-B07),
        byte_1 holds the remaning 7 MBS bits (B06-B00) and B01 from the LSB-mode, which has to be removed.
        """
        bytes_received = self._spi.xfer2([0x00, 0x00])

        MSB_1 = bytes_received[1]
        MSB_1 = MSB_1 >> 1  # shift right 1 bit to remove B01 from the LSB mode

        MSB_0 = bytes_received[0] & 0b00011111  # mask the 2 unknown bits and the null bit
        MSB_0 = MSB_0 << 7  # shift left 7 bits (i.e. the first MSB 5 bits of 12 bits)

        return MSB_0 + MSB_1


    def readADC_LSB(self):
        """
        Reads 4 bytes (byte_0 - byte_3) and converts the output code from LSB format mode:
        byte 1 holds B00 (shared by MSB- and LSB-modes) and B01,
        byte_2 holds the next 8 LSB bits (B03-B09), and
        byte 3, holds the remaining 2 LSB bits (B10-B11).
        """
        bytes_received = self._spi.xfer2([0x00, 0x00, 0x00, 0x00])

        LSB_0 = bytes_received[1] & 0b00000011  # mask the first 6 bits from the MSB mode
        LSB_0 = bin(LSB_0)[2:].zfill(2)  # converts to binary, cuts the "0b", include leading 0s

        LSB_1 = bytes_received[2]
        LSB_1 = bin(LSB_1)[2:].zfill(8)  # see above, include leading 0s (8 digits!)

        LSB_2 = bytes_received[3]
        LSB_2 = bin(LSB_2)[2:].zfill(8)
        LSB_2 = LSB_2[0:2]  # keep the first two digits

        LSB = LSB_0 + LSB_1 + LSB_2  # concatenate the three parts to the 12-digits string
        LSB = LSB[::-1]  # invert the resulting string
        return int(LSB, base=2)

        
    def convert_to_voltage(self, adc_output, VREF=3.3):
        """
        Calculates analogue voltage from the digital output code (ranging from 0-4095)
        VREF could be adjusted here (standard uses the 3V3 rail from the Rpi)
        """
        return adc_output * (VREF / (2 ** 12 - 1))

def takePoints():
    global winnerTeam
    global points
    global camera
    global origo
    camera.start_preview()
    time.sleep(1)
    camera.stop_preview()
    camera.capture('image0.jpg')

    im = cv2.imread("image0.jpg")
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

    # Lager en "maske" som filtrerer bort alt i bildet bortsett fra det blå:
    blue_mask = cv2.inRange(hsv, low_blue, high_blue)
    red_mask = cv2.inRange(hsv, low_red, high_red)

    redstones = []
    bluestones = []
    #redcount = 0
    #bluecount = 0

    minDist = 10
    param1 = 300 #500
    param2 = 10 #200 #smaller value-> more false circles
    minRadius = 20
    maxRadius = 26 
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
            #cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print(x,y, r, "blue")
            bluestones.append((x,y))
            #bluecount +=1

    if red_circles is not None:
        red_circles = np.round(red_circles[0, :]).astype("int")
        for (x, y, r) in red_circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            #cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            print(x,y, r, "red")
            redstones.append((x,y))
            #redcount +=1
    print("The red stone coordinates are: ", redstones)
    print("The blue stone coordinates are: ", bluestones)
    #print("Red count: ", redcount)
    #print("Blue count: ", bluecount)


    bluedist = []
    reddist = []

    for i in range(len(bluestones)):
        xdist = abs(bluestones[i][0]-origo[0])
        ydist = abs(bluestones[i][1]-origo[1])
        bluedist.append(math.sqrt(xdist**2 + ydist**2))

    for i in range(len(redstones)):
        xdist = abs(redstones[i][0]-origo[0])
        ydist = abs(redstones[i][1]-origo[1])
        reddist.append(math.sqrt(xdist**2 + ydist**2))

    bluedist[:] = [x for x in bluedist if x <= 256]
    reddist[:] = [x for x in reddist if x <= 256]

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
    #cv2.imshow('blue', blue_mask)
    #cv2.imshow('red', red_mask)
    #cv2.imshow("output", output)
    #cv2.waitKey(0)
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

def defineCenter():
    global camera
    global origo
    #camera.start_preview()
    #time.sleep(1)
    #camera.stop_preview()
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
    if contour_list == []:
        defineCenter() 

    M = cv2.moments(contour_list[0])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    print(cX)
    print(cY)
    origo = [cX, cY]

    window.after(3000,clearFrame)
    window.after(3000, window1)

    """     cv2.drawContours(image, contour_list,  -1, (255,0,0), 2)
    cv2.imshow('Objects Detected',image)
    cv2.waitKey(0) """

class ImageLabel(Label): # Gif
    """a label that displays images, and plays them if they are gifs"""
    
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
            #im = im.resize(300, 200)
            
        self.loc = 0
        self.frames = []
        
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)

        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()
    
    

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
            self.config(heigh = 200)
            self.config(width = 800)

class ImageLabel2(Label): # Gif
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
            #im = im.resize(300, 200)
        self.loc = 0
        self.frames = []
    
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
            self.config(bg = bakgrunn)

def pointsInTable(winnerTeam, points):
    global winner
    if winnerTeam == 1:
        table[rundenr][1] = points
        table[rundenr][2] = 0
        winner = 1
        ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser0.flush()
        timer = 0
        while timer < 4:
            ser0.write(b"1\n")
            # line = ser1.readline().decode('utf-8').rstrip()
            # print(line)
            time.sleep(0.2)
            timer += 1
    elif winnerTeam == 2:
        table[rundenr][2] = points
        table[rundenr][1] = 0
        winner = 2
        ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser0.flush()
        timer = 0
        while timer < 4:
            ser0.write(b"2\n")
            # line = ser1.readline().decode('utf-8').rstrip()
            # print(line)
            time.sleep(0.2)
            timer += 1
    else:
        table[rundenr][2] = 0
        table[rundenr][1] = 0

#Funksjonercont
#roundKeeper(tar inn data fra pi-en):
#Øker rundenr med 1 hver gang en stein registreres
def clearFrame(): # Destroys all widgets from frame
    for widget in window.winfo_children():
       widget.destroy()
       
def Avslutt(): # Åpner varslingsvindu
    w = Tk()
    w.config(bg=bakgrunn)
    w.geometry('400x240')  
    v = Label(w, text="Ved å avslutte nå vil\n ikke gjeldende runde telle", font=("Arial Bold", 10), bg = bakgrunn)
    v.place(relx = 0.3, rely = 0.2)
    def closeW(): # Lukker vinduet
        w.destroy()
    def A(): #Avsluttknapp i det lille vinduet
        global avsluttBool
        global stones
        avsluttBool = True
        stones = 0
        w.destroy()
        clearFrame()
        window3()

    avsluttSpill = Button(w, text="Avslutt spill", command=A, font=("Arial Bold", 16),bg = knapp, activebackground = aktivknapp)
    avsluttSpill.place(relx = 0.35, rely = 0.65)
    
    tilbake = Button(w, text="Tilbake til spillet", command=closeW, font=("Arial Bold", 16),bg = knapp, activebackground = aktivknapp)
    tilbake.place(relx = 0.3, rely = 0.4)

def logoWindow():
    def startLyssekvens():
        ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser0.flush()
        timer = 0
        while timer < 4:
            ser0.write(b"0\n")
            time.sleep(0.2)
            timer += 1
        window.after(100, defineCenter)
    img4 = ImageTk.PhotoImage(logo.rotate(0, expand = 1).resize((600, 480))) 
    label4 = Label(window, image=img4, bg = 'hot pink')
    label4.image = img4
    label4.pack()
    window.after(100, startLyssekvens)
    




def window1(): # Åpner første vindu
    window.config(bg = "palegreen")
    x = Label(window, text="Velg antall runder og steiner per lag", font=("Arial Bold", 20), bg = bakgrunn)
    x.place(relx = 0.2, rely = 0.1)
    chooseRounds = Label(window, text="Runder:", font=("Arial Bold", 20), bg = bakgrunn)
    chooseRounds.place(relx = 0.27, rely = 0.25)
    chooseStones = Label(window, text="Steiner:", font=("Arial Bold", 20), bg = bakgrunn)
    chooseStones.place(relx = 0.57, rely = 0.25)
    l = Label(window, text=str(runder), font=("Arial Bold", 60), bg = bakgrunn)
    l.place(relx = 0.4, rely = 0.42)
    s = Label(window, text=str(stonesPer), font=("Arial Bold", 60), bg = bakgrunn)
    s.place(relx=0.7, rely= 0.42)
 
    def pilOpp(): # Øker antall runder
        value = int(l["text"])
        if value < 10:
            l["text"] = f"{value + 1}"
            global runder
            runder += 1
    
    def pilNed():# Minker antall runder
        value = int(l["text"])
        if value > 1:
            l["text"] = f"{value - 1}"
            global runder
            runder -= 1

    def pilOpp2(): # Øker antall steiner
        value = int(s["text"])
        if value < 8:
            s["text"] = f"{value + 1}"
            global stonesPer
            stonesPer += 1
    
    def pilNed2():# Minker antall steiner
        value = int(s["text"])
        if value > 1:
            s["text"] = f"{value - 1}"
            global stonesPer
            stonesPer -= 1
    
    def Start():# Hopper til vindu 2
        clearFrame()
        window2()   

    opp = Button(window, text="\u2191", command=pilOpp, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp) # Oppknapp
    opp.place(relx = 0.3, rely = 0.35)
    
    ned = Button(window, text="\u2193", command=pilNed, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Nedknapp
    ned.place(relx = 0.3, rely = 0.53)

    opp2 = Button(window, text="\u2191", command=pilOpp2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Oppknapp steiner
    opp2.place(relx = 0.6, rely = 0.35)
    
    ned2 = Button(window, text="\u2193", command=pilNed2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Nedknapp steiner
    ned2.place(relx = 0.6, rely = 0.53)
    
    start = Button(window, text="Start", command=Start, font=("Arial Bold", 40),bg = knapp, activebackground = aktivknapp) # Startknapp
    start.place(relx = 0.389, rely = 0.73)

def window2(): # Vinduet under spill
    global stones1
    global stones2

    l = Label(window, text=f"Runde {str(rundenr)}", font=("Arial", 55, 'bold italic'),bg = bakgrunn)
    l.place(relx = 0.3)

    avslutt = Button(window, text="Avslutt", command=Avslutt, font=("Arial Bold", 21),bg = knapp, activebackground = aktivknapp)
    avslutt.place(relx = 0.843, rely = 0.872)
    
    # Forstørre Team Blue og Team oransje og midtstille. Dette må også gjøres i s- og regret-funksjonen
    if winner == 2:
        lag1 = Label(window, text=name1, fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
        lag2 = Label(window, text=name2, font=("Arial bold", 40),bg = bakgrunn) 
    else: 
        lag1 = Label(window, text=name1, font=("Arial bold", 40),bg = bakgrunn)  
        lag2 = Label(window, text=name2, fg = oransjefarge, bg = bakgrunn, font=("Arial bold", 40)) 
        
    lag1.place(relx = pos1x, rely = pos1y)
    lag2.place(relx = pos2x, rely = pos1y)         

    
    stones1 = stonesPer # Startverdi antall steiner igjen team 1
    stones2 = stonesPer # Startverdi antall steiner igjen team 2
    
    team1stones = Label(window, text=str(stones1), font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 1 (tall)
    if stones1==1:
        team1stonesText = Label(window, text=stoneLeft, font=("Arial bold", 30),bg = bakgrunn)
    else:
        team1stonesText = Label(window, text=stonesLeft, font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 1 (tekst)
    
    
    team2stones = Label(window, text=str(stones2), font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 2 (tall)
    if stones2==1:
        team2stonesText = Label(window, text=stoneLeft, font=("Arial bold", 30),bg = bakgrunn)
    else:
        team2stonesText = Label(window, text=stonesLeft, font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 2 (text)
    
    team1stones.place(relx = pos3x, rely = pos3y)
    team1stonesText.place(relx = pos3x+0.05, rely = pos3y)
    team2stones.place(relx = pos4x, rely = pos3y)
    team2stonesText.place(relx = pos4x+0.05, rely = pos3y)

    def checkForStone():
        #Automatisk registrering av passerte steiner.
        global stones
        global stones1
        global winnerTeam
        global points
        global rundenr
        global stones2
        global value1
        global value2
        stonesBefore = stones
        value1 = int(team1stones["text"])
        value2 = int(team2stones["text"])
        beginning = True
                    
        if __name__ == '__main__':
            GPIO.output(18,GPIO.HIGH)
            time.sleep(0.01)
            SPI_bus = 0
            CE = 0
            MCP3201X = MCP3201(SPI_bus, CE)
            
            try:
                while stonesBefore == stones:

                    if beginning:
                        for i in range(4):
                            ADC_output_code = MCP3201X.readADC_MSB()
                            time.sleep(0.005)
                        beginning = False
                    
                    ADC_output_code = MCP3201X.readADC_MSB()
                    time.sleep(0.005)  # wait minimum of 100 ms between ADC measurements
                    
                    #ADC_output_code = MCP3201X.readADC_LSB()
                    #ADC_voltage = MCP3201X.convert_to_voltage(ADC_output_code)
                    
                    #time.sleep(0.1)
                    print(ADC_output_code)

                    
                    if (ADC_output_code < 500):
                        print("LED on")
                        
                        if winner == 1:
                            if (stones % 2 == 0):
                                stones2 -= 1
                                if stones2 == 1:
                                    team2stonesText["text"] = stoneLeft
                                if stones2 == 0 or stones2>1:
                                    team2stonesText["text"] = stonesLeft
                                team2stones["text"] = str(value2 - 1)
                                lag1 = Label(window, text=name1, fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                                lag1.place(relx = pos1x, rely = pos1y)
                                lag2 = Label(window, text=name2, bg = bakgrunn, font=("Arial bold", 40)) 
                                lag2.place(relx = pos2x, rely = pos1y)
                            else:
                                stones1 -= 1
                                if stones1 == 1:
                                    team1stonesText["text"] = stoneLeft
                                if stones1 == 0 or stones1>1:
                                    team1stonesText["text"] = stonesLeft
                                team1stones["text"] = str(value1 - 1)
                                lag1 = Label(window, text=name1, bg = bakgrunn, font=("Arial bold", 40))  
                                lag1.place(relx = pos1x, rely = pos1y)
                                lag2 = Label(window, text=name2, fg = "darkorange3", bg = bakgrunn, font=("Arial bold", 40)) 
                                lag2.place(relx = pos2x, rely = pos1y)
                        else:
                            if (stones % 2 == 0):
                                stones1 -= 1
                                if stones1 == 1:
                                    team1stonesText["text"] = stoneLeft
                                if stones1 == 0 or stones1>1:
                                    team1stonesText["text"] = stonesLeft
                                team1stones["text"] = str(value1 - 1)
                                lag1 = Label(window, text=name1, bg = bakgrunn, font=("Arial bold", 40))  
                                lag1.place(relx = pos1x, rely = pos1y)
                                lag2 = Label(window, text=name2, fg = oransjefarge, font=("Arial bold", 40),bg = bakgrunn) 
                                lag2.place(relx = pos2x, rely = pos1y)
                            else:
                                stones2 -= 1
                                if stones2 == 1:
                                    team2stonesText["text"] = stoneLeft
                                if stones2 == 0 or stones2>1:
                                    team2stonesText["text"] = stonesLeft
                                team2stones["text"] = str(value2 - 1)
                                lag1 = Label(window, text=name1, fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                                lag1.place(relx = pos1x, rely = pos1y)
                                lag2 = Label(window, text=name2, bg = bakgrunn, font=("Arial bold", 40)) 
                                lag2.place(relx = pos2x, rely = pos1y)
                        stones += 1
                        time.sleep(0.3)
                        
                        break

            except (KeyboardInterrupt):
                print('\n', "Exit on Ctrl-C: Good bye!")

            except:
                print("Other error or exception occurred!")
                raise

            finally:
                print()


        
        #Check if the round is finished
        if (stones == stonesPer*2):
            stones = 0
            GPIO.output(18,GPIO.LOW)
            time.sleep(1.7)
            takePoints()
            pointsInTable(winnerTeam, points)
            #global rundenr
            rundenr+=1
            clearFrame()
            window3()
        else:
            window.after(200, checkForStone)

    #stonesButton=Button(window, text="Steiner", command=s, font=("Arial bold", 20), bg = knapp, activebackground = aktivknapp) # "Øke antall steiner"-knapp
    #stonesButton.place(relx = 0.4, rely = 0.7)

    def regret(): # Knapp for å angre stein
        global stones
        global stones2
        global stones1
        if stones != 0:
            stones-=1
            value1 = int(team1stones["text"])
            value2 = int(team2stones["text"])
            if (winner == "orange"):
                if (stones % 2 == 0):
                    stones2 += 1
                    if stones2 == 1:
                        team2stonesText["text"] = stoneLeft
                    if stones2 == 0 or stones2>1:
                        team2stonesText["text"] = stonesLeft
                    team2stones["text"] = str(value2 + 1)
                    
                    lag1 = Label(window, text=name1, font=("Arial bold", 40), bg = bakgrunn)  
                    lag1.place(relx = pos1x, rely = pos1y)
                    lag2 = Label(window, text=name2, fg = oransjefarge, bg = bakgrunn, font=("Arial bold", 40)) 
                    lag2.place(relx = pos2x, rely = pos1y)


                else:
                    stones1 += 1
                    if stones1 == 1:
                        team1stonesText["text"] = stoneLeft
                    if stones1 == 0 or stones1>1:
                        team1stonesText["text"] = stonesLeft
                    team1stones["text"] = str(value1 + 1)

                    lag1 = Label(window, text=name1, fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                    lag1.place(relx = pos1x, rely = pos1y)
                    lag2 = Label(window, text=name2, font=("Arial bold", 40), bg = bakgrunn) 
                    lag2.place(relx = pos2x, rely = pos1y)

            if (winner == "blue"):
                if (stones % 2 == 0):
                    stones1 += 1
                    if stones1 == 1:
                        team1stonesText["text"] = stoneLeft
                    if stones1 == 0 or stones1>1:
                        team1stonesText["text"] = stonesLeft
                    team1stones["text"] = str(value1 + 1)

                    lag1 = Label(window, text=name1, fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                    lag1.place(relx = pos1x, rely = pos1y)
                    lag2 = Label(window, text=name2, font=("Arial bold", 40), bg = bakgrunn) 
                    lag2.place(relx = pos2x, rely = pos1y)
                    
                else:
                    stones2 += 1
                    if stones2 == 1:
                        team2stonesText["text"] = stoneLeft
                    if stones2 == 0 or stones2>1:
                        team2stonesText["text"] = stonesLeft
                    team2stones["text"] = str(value2 + 1)

                    lag1 = Label(window, text=name1, font=("Arial bold", 40), bg = bakgrunn)  
                    lag1.place(relx = pos1x, rely = pos1y)
                    lag2 = Label(window, text=name2, fg = oransjefarge, bg = bakgrunn, font=("Arial bold", 40)) 
                    lag2.place(relx = pos2x, rely = pos1y)
    
    # Justere plasseringen(midtstilt?) og teksstørrelsen(større) til denne knappen
    regretStone = Button(window, text="Angre stein", font=("Arial bold", 21), command=regret, bg = knapp, activebackground = aktivknapp)
    regretStone.place(relx = 0.0005, rely = 0.872)


    # photo = PhotoImage(file = "pinkLightning.png")
    # pinkL = Label(window, image=photo)
    # pinkL.pack()

    # canvas = Canvas(window, width = 300, height = 300)      
    # canvas.pack()      
    # img = PhotoImage(file="pinkLightning.png")      
    # canvas.create_image(20,20, anchor=NW, image=img)

    # canvas = Canvas(window, width = 300, height = 300)  
    # canvas.pack()  
    # img = ImageTk.PhotoImage(Image.open("pinkLightning.png"))  
    # canvas.create_image(20, 20, anchor=NW, image=img)

    # global img
    # c = Canvas(window, width=500, height=500)
    # c.pack()
    # c.create_image(0, 0, image=img, anchor=NW)

    # myImage = Image.open("/Users/Lillemina/Elsys_Prosjekt_2021_Gruppe4/GUI/pinkLightning.png")
    # myImage.show()

    # img = Image.open("/Users/Lillemina/Elsys_Prosjekt_2021_Gruppe4/GUI/pinkLightning.png")
    # img = img.resize((250, 250))
    # tkimage = ImageTk.PhotoImage(img)
    # Label(window, image=tkimage).grid()

    # load = Image.open("/Users/Lillemina/Elsys_Prosjekt_2021_Gruppe4/GUI/pinkLightning2.jpeg")
    # render = ImageTk.PhotoImage(load)
    # img = Label(window, image=render)
    # img.place(x=100, y=100)

    # Versus:
    img = ImageTk.PhotoImage(pinkL.rotate(0, expand = 1).resize((150, 200))) 
    label = Label(window, image=img, bg = bakgrunn)
    label.image = img
    label.place(relx = 0.37, rely = 0.2)

    # Blue stone:
    img2 = ImageTk.PhotoImage(blueStone.rotate(0, expand = 1).resize((150, 120))) 
    label2 = Label(window, image=img2, bg = bakgrunn)
    label2.image = img2
    label2.place(relx = 0.1, rely = 0.55)

    # Orange stone:
    orangeStone2 = orangeStone.transpose(Image.FLIP_LEFT_RIGHT)
    img3 = ImageTk.PhotoImage(orangeStone2.rotate(0, expand = 1).resize((150, 120))) 
    label3 = Label(window, image=img3, bg = bakgrunn)
    label3.image = img3
    label3.place(relx = 0.65, rely = 0.55)

    # img2 = ImageTk.PhotoImage(gif.resize((250, 150))) 
    # label2 = Label(window, image=img2, bg = bakgrunn)
    # label2.image = img2
    # label2.place(relx = 0.3, rely = 0.65)'''

    # frames = [PhotoImage(file = fil, format = 'gif -index %i' %(i)) for i in range(212)]
    # def update(ind):
    #     frame = frames[ind]
    #     ind += 1
    #     label.configure(image=frame)
    #     window.after(212, update, ind)
    # label2 = Label(window)
    # label2.place(relx = 0.3, rely = 0.65)
    # window.after(0, update, 0)

    window.after(200,checkForStone)  

def window3(): # Vindu med resultater
    for i in range(1,11):
        table[i][0] = str(i)
    def w4(): # Åpner vindu 4
        clearFrame()
        window4()
    def w3_1(): # vindu 3 versjon 1
        def n_r(): # Åpner vindu 2
            clearFrame()
            window2()
        def a2(): # Åpner et "sikker på at du vil avslutte"-vindu
            w2 = Tk()
            w2.config(bg=bakgrunn)
            w2.geometry('400x240')
            v2 = Label(w2, text="Er du sikker på at du\n vil avslutte nå?", font=("Arial Bold", 10), bg = bakgrunn)
            v2.place(relx = 0.35, rely = 0.2)
            def closeW2(): # Lukker det lille vinduet
                w2.destroy()
            def a3(): # Lukker det lille vinduet og åpner vindu 4
                w2.destroy()
                clearFrame()
                window4()
            
            avsluttSpill2 = Button(w2, text="Avslutt spill",command=a3, font=("Arial Bold", 16),bg = knapp, activebackground = aktivknapp) # Avsluttknapp i det lille vinduet
            avsluttSpill2.place(relx = 0.35, rely = 0.65)
            
            tilbake2 = Button(w2, text="Tilbake til spillet", command=closeW2, font=("Arial Bold", 16), bg = knapp, activebackground = aktivknapp) # Fortsettknapp i det lille vinduet
            tilbake2.place(relx = 0.3, rely = 0.4)
        nesteRunde = Button(window, text="Neste runde", font = ("Arial Bold", 21), command=n_r, bg = knapp, activebackground = aktivknapp) # "Neste runde"-knapp
        nesteRunde.place(relx=0.37, rely=0.7)
        
        avslutt2 = Button(window, text="Avslutt", command=a2, font=("Arial Bold", 21), bg = knapp, activebackground = aktivknapp) # Avsluttknapp
        avslutt2.place(relx = 0.843, rely = 0.872)
    def w3_2(): # vindu 3 versjon 2
        fortsett = Button(window, text="Fortsett", font =("Arial Bold", 21), command=w4, bg = knapp, activebackground = aktivknapp) # Fortsettknapp
        fortsett.place(relx=0.41, rely=0.7)

    #lbl = ImageLabel(window)
    #lbl.place(relx = 0, rely = 0.25)
    #lbl.load(filGif)
    # lbl.next_frame.config(heigh = 200)
    # lbl.next_frame.config(width = 800)

    img5 = ImageTk.PhotoImage(curlingStones.rotate(0, expand = 1).resize((548, 175))) 
    label5 = Label(window, image=img5, bg = bakgrunn)
    label5.image = img5
    label5.place(relx = 0.15, rely = 0.3)

    table[runder + 1][0] = 'Poeng'
    global sc1
    global sc2
    sc1 = 0
    sc2 = 0
    for i in range(1, rundenr):
        sc1 += table[i][1]
        sc2 += table[i][2]
    table[runder + 1][1] = sc1 
    table[runder + 1][2] = sc2 

    # Oppretter tabell
    class Table: 
        def __init__(self,window):
            skrift = 24
            kant = 1

            self.e = Entry(window, width=11, font=('Arial',skrift,'bold'), bd = kant)
            self.e.grid(row=0, column=0) 
            self.e.insert(END, table[0][0]) 

            self.e = Entry(window, width=11, font=('Arial',skrift,'bold'), fg = 'blue', bd = kant) 
            self.e.grid(row=1, column=0) 
            self.e.insert(END, table[0][1]) 

            self.e = Entry(window, width=11, font=('Arial',skrift,'bold'), fg = 'orange', bd = kant) 
            self.e.grid(row=2, column=0) 
            self.e.insert(END, table[0][2])
            for i in range(total_rows):
                for j in range(1, runder+1): 
                    self.e = Entry(window, width=floor(24/runder), font=('Arial',skrift,'bold'), justify = 'center', bd = kant) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, table[j][i])
               
                self.e = Entry(window, width=32-floor(24/runder)*runder, font=('Arial',skrift,'bold'), justify = 'center', bd = kant)
                self.e.grid(row=i, column=runder + 1) 
                self.e.insert(END, table[runder + 1][i])
 

    # Number of rows and colums in the list
    total_columns = runder + 2
    total_rows = 3
    t = Table(window)
    # Tabell slutt
    
    def Manually():
        clearFrame()

        x = Label(window, text="Legg til poeng", font=("Arial Bold", 50), bg = bakgrunn)
        x.place(relx = 0.2, rely = 0.05)
        tb = Label(window, text=name1 + ":", font=("Arial Bold", 20), bg = bakgrunn)
        tb.place(relx = 0.27, rely = 0.25)
        to = Label(window, text=name2 + ":", font=("Arial Bold", 20), bg = bakgrunn)
        to.place(relx = 0.57, rely = 0.25)
        l = Label(window, text=str(0), font=("Arial Bold", 60), bg = bakgrunn)
        l.place(relx = 0.4, rely = 0.42)
        s = Label(window, text=str(0), font=("Arial Bold", 60), bg = bakgrunn)
        s.place(relx=0.7, rely= 0.42)

        def pilOpp(): # Øker poeng team blue
            value = int(l["text"])
            if value < stonesPer:
                global bluePoints
                global orangePoints
                if orangePoints > 0:
                    bluePoints = 0
                    l["text"] = f"{value}"
                else:
                    bluePoints += 1
                    l["text"] = f"{value + 1}"

        def pilNed():# Minker poeng team blue
            value = int(l["text"])
            if value > 0:
                l["text"] = f"{value - 1}"
                global bluePoints
                bluePoints -= 1

        def pilOpp2(): # Øker poeng team orange
            value = int(s["text"])
            if value < stonesPer:
                
                global orangePoints
                global bluePoints
                if bluePoints > 0:
                    orangePoints = 0
                    s["text"] = f"{value}"
                else:
                    orangePoints += 1
                    s["text"] = f"{value + 1}"
                
        def pilNed2():# Minker poeng team orange
            value = int(s["text"])
            if value > 0:
                s["text"] = f"{value - 1}"
                global orangePoints
                orangePoints -= 1
        
        def Cont():
            global table
            global bluePoints
            global orangePoints
            table[rundenr-1][1] = bluePoints
            table[rundenr-1][2] = orangePoints
            bluePoints = 0
            orangePoints = 0
            clearFrame()
            window3()
 

        opp = Button(window, text="\u2191", command=pilOpp, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp)
        opp.place(relx = 0.3, rely = 0.35)
        
        ned = Button(window, text="\u2193", command=pilNed, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp)
        ned.place(relx = 0.3, rely = 0.53)

        opp2 = Button(window, text="\u2191", command=pilOpp2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp)
        opp2.place(relx = 0.6, rely = 0.35)
        
        ned2 = Button(window, text="\u2193", command=pilNed2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp)
        ned2.place(relx = 0.6, rely = 0.53)
        
        cont = Button(window, text="Fortsett", command=Cont, font=("Arial Bold", 35),bg = knapp, activebackground = aktivknapp)
        cont.place(relx = 0.355, rely = 0.77)
    
    def Recalc():
        global rundenr
        rundenr -= 1
        takePoints()
        pointsInTable(winnerTeam, points)
        rundenr += 1
        clearFrame()
        window3()


    manually = Button(window, text="Legg til poeng manuelt", font=("Arial bold", 21), command=Manually, bg = knapp, activebackground = aktivknapp)
    manually.place(relx = 0.0005, rely = 0.872)

    recalc = Button(window, text="Sjekk poeng på nytt", font=("Arial bold", 21), command=Recalc, bg = knapp, activebackground = aktivknapp)
    recalc.place(relx = 0.45, rely = 0.872) 

    if avsluttBool or (runder < rundenr): #Bestemmer hvilken versjon av vindu 3
        w3_2()
    else:
        w3_1()
    
def window4():

    def nyttSpill(): # Starter spillet på nytt (åpner vindu 1)
        global avsluttBool
        global runder
        global stonesPer
        avsluttBool=False
        runder = 5
        stonesPer = 1
        for i in range(1,len(table)):
            table[i][1] = ''
            table[i][2] = ''
        clearFrame()
        window1()
    
    global rundenr
    rundenr = 1

    if sc1 != sc2:
        confetti = ImageLabel2(window)
        confetti.pack()
        confetti.load(filConfetti)

    ns = Button(window, text="Nytt spill", command=nyttSpill, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp) # "Nytt spill"-knapp
    ns.place(relx=0.35, rely=0.6)

    # Forstørr og midtstill
    if sc1 > sc2:
        vinnerText = Label(window, text="Vinneren er " + name1, fg = 'blue', bg = bakgrunn, font=("Arial Bold", 40))
        vinnerText.place(relx=0.14, rely=0.3)
        ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser0.flush()
        timer = 0
        while timer < 4:
            ser0.write(b"3\n")
            # line = ser1.readline().decode('utf-8').rstrip()
            # print(line)
            time.sleep(0.2)
            timer += 1
    elif sc1 < sc2:
        vinnerText = Label(window, text="Vinneren er " + name2, fg = oransjefarge, bg = bakgrunn, font=("Arial Bold", 40))
        vinnerText.place(relx=0.1, rely=0.3)
        ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser0.flush()
        timer = 0
        while timer < 4:
            ser0.write(b"4\n")
            # line = ser1.readline().decode('utf-8').rstrip()
            # print(line)
            time.sleep(0.2)
            timer += 1
    else: 
         vinnerText = Label(window, text="Det ble uavgjort", bg = bakgrunn, font=("Arial Bold", 50))
         vinnerText.place(relx=0.17, rely=0.3)
        


logoWindow()


    
window.mainloop()
