from tkinter import Button, Label, Tk, Entry, END
window = Tk()
window.title("Curling game")
window.geometry('800x480')
# import the necessary packages
#from email.mime import image
import math
import numpy as np
#import argparse
import cv2
from picamera import PiCamera
#from time import sleep
import serial
import time
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True, help = "Path to the image")
#args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
#image = cv2.imread(args["image"])

#Globale variabler:
runder = 5
rundenr = 1
avsluttBool = False
stones = 0
winner = "blue"
winnerTeam = 2 # input fra openCV (Team Blue = 1, Team Orange = 2, uavgjort = 0)
points = 2 # Input fra openCV (antall poeng til winnerTeam, dersom uavgjort har ikke denne verdien noe å si)
totalStones = 4
stones1 = int(totalStones/2)
stones2 = int(totalStones/2)

def takePoints():
    global winnerTeam
    global points
    #camera = PiCamera()
    #camera.resolution = (3280,2464)
    #camera.start_preview()
    #sleep(2)
    #camera.stop_preview()
    #camera.capture('image0.jpg')

    #im = cv2.imread("image0.jpg")
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
    low_red = np.array([1, 100, 138])
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
    param2 = 15#200 #smaller value-> more false circles
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
    #houselimit = Størrelsen på boet i piksler??

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








# Lager liste med resultater
table = list(range(12))
for i in range(0,12):
    cols = list(range(3))
    cols[0] = str(i)        
    cols[1] = ''
    cols[2] = ''
    table[i] = cols
table[0][0] = "Team/Round"
table[0][1] = "Team Blue"
table[0][2] = "Team Orange"


def pointsInTable(winnerTeam, points):
    global winner
    if winnerTeam == 1:
        table[rundenr][1] = points
        table[rundenr][2] = 0
        winner = 1
    elif winnerTeam == 2:
        table[rundenr][2] = points
        table[rundenr][1] = 0
        winner = 2
    else:
        table[rundenr][2] = 0
        table[rundenr][1] = 0

#Funksjoner
#roundKeeper(tar inn data fra pi-en):
#Øker rundenr med 1 hver gang en stein registreres
def clearFrame(): # Destroys all widgets from frame
    for widget in window.winfo_children():
       widget.destroy()
       
def Avslutt(): # Åpner varslingsvindu
    w = Tk()
    w.geometry('400x240')  
    v = Label(w, text="By exiting now the\n current round won't count", font=("Arial Bold", 10))
    v.place(relx = 0.3, rely = 0.2)
    def closeW(): # Lukker vinduet
        w.destroy()
    def A(): #Avsluttknapp i det lille vinduet
        global avsluttBool
        avsluttBool = True
        w.destroy()
        clearFrame()
        window3()

    avsluttSpill = Button(w, text="End game",command=A, font=("Arial Bold", 10))
    avsluttSpill.place(relx = 0.6, rely = 0.4)
    
    tilbake = Button(w, text="Back to the game", command=closeW, font=("Arial Bold", 10))
    tilbake.place(relx = 0.2, rely = 0.4)

def window1(): # Åpner første vindu
    x = Label(window, text="How many rounds would you like to play?", font=("Arial Bold", 20))
    x.place(relx = 0.15, rely = 0.2)
    l = Label(window, text=str(runder), font=("Arial Bold", 60))
    l.place(relx = 0.4, rely = 0.42)
    
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
    
    def Start():# Hopper til vindu 2
        clearFrame()
        window2()   


    opp = Button(window, text="\u2191", command=pilOpp, font=("Arial Bold", 30)) # Oppknapp
    opp.place(relx = 0.55, rely = 0.35)
    
    ned = Button(window, text="\u2193", command=pilNed, font=("Arial Bold", 30)) # Nedknapp
    ned.place(relx = 0.55, rely = 0.53)
    
    start = Button(window, text="Start", command=Start, font=("Arial Bold", 25)) # Startknapp
    start.place(relx = 0.45, rely = 0.8)

def window2(): # Vinduet under spill
    global rundenr
    global stones
    l = Label(window, text=f"Round {str(rundenr)}", font=("Arial Bold", 40))
    l.place(relx = 0.4)

    avslutt = Button(window, text="Quit", command=Avslutt, font=("Arial Bold", 30))
    avslutt.place(relx = 0.856, rely = 0.83)
    
    if winner == 'blue':
        lag1 = Label(window, text="Team Blue", fg = 'blue', font=("Arial bold", 40))  
        lag1.place(relx = 0.05, rely = 0.2)
        lag2 = Label(window, text="Team Orange", font=("Arial bold", 40)) 
        lag2.place(relx = 0.45, rely = 0.2) 
    else: 
        lag1 = Label(window, text="Team Blue", font=("Arial bold", 40))  
        lag1.place(relx = 0.05, rely = 0.2)
        lag2 = Label(window, text="Team Orange", fg = 'orange', font=("Arial bold", 40)) 
        lag2.place(relx = 0.45, rely = 0.2)         

    
    stones1 = int(totalStones/2) # Startverdi antall steiner igjen team 1
    stones2 = int(totalStones/2) # Startverdi antall steiner igjen team 2
    
    team1stones = Label(window, text=str(stones1), font=("Arial bold", 30)) # Label antall steiner igjen team 1 (tall)
    team1stones.place(relx = 0, rely = 0.4)
    team1stonesText = Label(window, text="Stone(s) left", font=("Arial bold", 30)) # Label antall steiner igjen team 1 (tekst)
    team1stonesText.place(relx = 0.05, rely = 0.4)
    
    team2stones = Label(window, text=str(stones2), font=("Arial bold", 30)) # Label antall steiner igjen team 2 (tall)
    team2stones.place(relx = 0.5, rely = 0.4)
    team2stonesText = Label(window, text="Stone(s) left", font=("Arial bold", 30)) # Label antall steiner igjen team 2 (text)
    team2stonesText.place(relx = 0.55, rely = 0.4)

    #simulasjon av steinkast
    """ def s(): # Funksjon til knapp som øker antall steiner kastet ved trykk på knapp, samt reduserer antall steiner igjen på hvert lag
        global stones
        global stones2
        global stones1
        global winnerTeam
        global points
        stones+=1
        value1 = int(team1stones["text"])
        value2 = int(team2stones["text"])
        if winner == "blue":
            if (stones % 2 == 0):
                stones2 -= 1
                team2stones["text"] = str(value2 - 1)
                lag1 = Label(window, text="Team Blue", fg = 'blue', font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
            else:
                stones1 -= 1
                team1stones["text"] = str(value1 - 1)
                lag1 = Label(window, text="Team Blue", font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", fg = 'orange', font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
        else:
            if (stones % 2 == 0):
                stones1 -= 1
                team1stones["text"] = str(value1 - 1)
                lag1 = Label(window, text="Team Blue", font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", fg = 'orange', font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
            else:
                stones2 -= 1
                team2stones["text"] = str(value2 - 1)
                lag1 = Label(window, text="Team Blue", fg = 'blue', font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
    

        if (stones == totalStones):
            stones = 0
            takePoints()
            pointsInTable(winnerTeam, points)
            global rundenr
            rundenr+=1
            clearFrame()
            window3() """


    while stones != totalStones:
        #Automatisk registrering av passerte steiner.
        value1 = int(team1stones["text"])
        value2 = int(team2stones["text"])
        stonesBefore = stones

        ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser1.flush()
        while stonesBefore == stones:
            ser1.write(b"0\n")
            line = 0
            line = int(ser1.readline().decode('utf-8').rstrip())
            if line == 1:
                stones += 1
            print(line)
            time.sleep(1)
            

        if winner == "blue":
            if (stones % 2 == 0):
                stones2 -= 1
                team2stones["text"] = str(value2 - 1)
                lag1 = Label(window, text="Team Blue", fg = 'blue', font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
            else:
                stones1 -= 1
                team1stones["text"] = str(value1 - 1)
                lag1 = Label(window, text="Team Blue", font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", fg = 'orange', font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
        else:
            if (stones % 2 == 0):
                stones1 -= 1
                team1stones["text"] = str(value1 - 1)
                lag1 = Label(window, text="Team Blue", font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", fg = 'orange', font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
            else:
                stones2 -= 1
                team2stones["text"] = str(value2 - 1)
                lag1 = Label(window, text="Team Blue", fg = 'blue', font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)

    stones = 0
    takePoints()
    pointsInTable(winnerTeam, points)
    #global rundenr
    rundenr+=1
    clearFrame()
    window3()


    

    #stonesButton=Button(window, text="Stones", command=s) # "Øke antall steiner"-knapp
    #stonesButton.place(relx = 0.5, rely = 0.5)

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
            w2.geometry('400x240')  
            v2 = Label(w2, text="Are you sure you\n want to quit now?", font=("Arial Bold", 10))
            v2.place(relx = 0.35, rely = 0.2)
            def closeW2(): # Lukker det lille vinduet
                w2.destroy()
            def a3(): # Lukker det lille vinduet og åpner vindu 4
                w2.destroy()
                clearFrame()
                window4()
            
            avsluttSpill2 = Button(w2, text="End game",command=a3, font=("Arial Bold", 10)) # Avsluttknapp i det lille vinduet
            avsluttSpill2.place(relx = 0.6, rely = 0.4)
            
            tilbake2 = Button(w2, text="Back to the game", command=closeW2, font=("Arial Bold", 10)) # Fortsettknapp i det lille vinduet
            tilbake2.place(relx = 0.2, rely = 0.4)
        nesteRunde = Button(window, text="Next round", command=n_r) # "Neste runde"-knapp
        nesteRunde.place(relx=0.2, rely=0.8)
        
        avslutt2 = Button(window, text="Quit", command=a2) # Avsluttknapp
        avslutt2.place(relx=0.5, rely=0.8)
    def w3_2(): # vindu 3 versjon 2
        fortsett = Button(window, text="Continue", command=w4) # Fortsettknapp
        fortsett.place(relx=0.4, rely=0.8)

    table[runder + 1][0] = 'Total score'
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
            for i in range(total_rows):
                self.e = Entry(window, width=12, fg='blue', font=('Arial',16,'bold')) 
                self.e.grid(row=i, column=0) 
                self.e.insert(END, table[0][i]) 
                for j in range(1, total_columns): 
                    self.e = Entry(window, width=4, fg='blue', font=('Arial',16,'bold')) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, table[j][i])
                self.e = Entry(window, width=11, fg='blue', font=('Arial',16,'bold')) 
                self.e.grid(row=i, column=runder + 1) 
                self.e.insert(END, table[runder + 1][i])

    # Number of rows and colums in the list
    total_columns = runder + 2
    total_rows = 3
    t = Table(window)
    # Tabell slutt
    
    if avsluttBool or (runder < rundenr): #Bestemmer hvilken versjon av vindu 3
        w3_2()
    else:
        w3_1()
    
def window4():
    def nyttSpill(): # Starter spillet på nytt (åpner vindu 1)
        global runder
        runder = 5
        clearFrame()
        window1()
        for i in range(1,len(table)):
            table[i][1] = ''
            table[i][2] = ''
    
    global rundenr
    rundenr = 1
    ns = Button(window, text="New game", command=nyttSpill, font=("Arial Bold", 30)) # "Nytt spill"-knapp
    ns.place(relx=0.35, rely=0.8)
    score1 = 0
    score2 = 0
    for i in range(1, runder + 1):
        score1 += int(table[i][1])
        score2 += int(table[i][2])
    if score1 > score2:
         vinnerText = Label(window, text="The winner is Team Blue", fg = 'blue', font=("Arial Bold", 40))
    elif score1 < score2:
         vinnerText = Label(window, text="The winner is Team Orange", fg = 'orange', font=("Arial Bold", 40))
    else: 
         vinnerText = Label(window, text="It's a tie", font=("Arial Bold", 50))
    vinnerText.place(relx=0.1, rely=0.3)
        
window1()
    
window.mainloop()