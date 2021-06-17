from tkinter import Button, Label, Tk, Entry, END, PhotoImage, NW, Canvas, BOTH
from PIL import ImageTk,Image
from math import floor
from itertools import count
window = Tk()
window.title("Curling game")
window.geometry('800x480')
window.config(bg='white')
window.iconphoto(False, PhotoImage(file='GUI\Images\yellowStone.png'))

#Globale variabler:
runder = 2
rundenr = 1
avsluttBool = False
stones = 0
winner = "blue"
winnerTeam = 2 # input fra openCV (Team Blue = 1, Team Orange = 2, uavgjort = 0)
points = 2 # Input fra openCV (antall poeng til winnerTeam, dersom uavgjort har ikke denne verdien noe å si)
stonesPer = 1
stones1 = stonesPer
stones2 = stonesPer
sc1=0
sc2=0
aktivknapp = "forest green"
oransjefarge = "darkorange3"
knapp = "limegreen"
bakgrunn = "palegreen"
pinkL = Image.open("GUI\Images\persusPink2.png")
blueStone = Image.open("GUI\Images\plueStone.png")
orangeStone = Image.open("GUI\Images\orangeStone.png")
logo = Image.open('GUI\Images\logoTrans.png')
#gif = Image.open("/Users/Lillemina/Elsys_Prosjekt_2021_Gruppe4/GUI/curlingGif.gif", format="gif -index 2")
filGif = 'GUI\Images\curlingGifTheOneAndOnly.gif'
filConfetti = 'GUI\Images\confetti.gif' 
bluePoints = 0
orangePoints = 0
name1 = "Blått Lag"
name2 = "Oransje Lag"
stoneLeft = "Stein igjen"
stonesLeft = "Steiner igjen"


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


def pointsInTable(winnerTeam, points):
    global winner
    if winnerTeam == 1:
        table[rundenr][1] = points
        table[rundenr][2] = 0
        winner = "blue"
    elif winnerTeam == 2:
        table[rundenr][2] = points
        table[rundenr][1] = 0
        winner = "orange"
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
    img4 = ImageTk.PhotoImage(logo.rotate(0, expand = 1).resize((600, 480))) 
    label4 = Label(window, image=img4, bg = 'white')
    label4.image = img4
    label4.pack()
    window.after(500,clearFrame)
    window.after(500, window1)


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

    unicode_char = '\u2B99'

    opp = Button(window, text=u'\u2B9D', command=pilOpp, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp) # Oppknapp
    opp.place(relx = 0.3, rely = 0.35)
    
    ned = Button(window, text="\u2B9b", command=pilNed, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Nedknapp
    ned.place(relx = 0.3, rely = 0.53)

    opp2 = Button(window, text="\u2B99", command=pilOpp2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Oppknapp steiner
    opp2.place(relx = 0.6, rely = 0.35)
    
    ned2 = Button(window, text="\u2B9b", command=pilNed2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Nedknapp steiner
    ned2.place(relx = 0.6, rely = 0.53)
    
    start = Button(window, text="Start", command=Start, font=("Arial Bold", 40),bg = knapp, activebackground = aktivknapp) # Startknapp
    start.place(relx = 0.389, rely = 0.73)

def window2(): # Vinduet under spill
    global stones1
    global stones2

    l = Label(window, text=f"Runde {str(rundenr)}", font=("Arial", 55, 'bold italic'),bg = bakgrunn)
    l.place(relx = 0.3)

    avslutt = Button(window, text="Avslutt", command=Avslutt, font=("Arial Bold", 22),bg = knapp, activebackground = aktivknapp)
    avslutt.place(relx = 0.843, rely = 0.872)
    
    # Forstørre Team Blue og Team oransje og midtstille. Dette må også gjøres i s- og regret-funksjonen
    if winner == 'blue':
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

    #simulasjon av steinkast
    def s(): # Funksjon til knapp som øker antall steiner kastet ved trykk på knapp, samt reduserer antall steiner igjen på hvert lag
        global stones
        global stones1
        global stones2
        global value1
        global value2
        stones+=1
        value1 = int(team1stones["text"])
        value2 = int(team2stones["text"])
        if winner == "blue":
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




        
        if (stones == stonesPer*2):
            stones = 0
            pointsInTable(winnerTeam, points)
            global rundenr
            rundenr+=1
            clearFrame()
            window3()

    stonesButton=Button(window, text="Steiner", command=s, font=("Arial bold", 20), bg = knapp, activebackground = aktivknapp) # "Øke antall steiner"-knapp
    stonesButton.place(relx = 0.4, rely = 0.7)

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
    regretStone = Button(window, text="Angre stein", font=("Arial bold", 22), command=regret, bg = knapp, activebackground = aktivknapp)
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
        nesteRunde = Button(window, text="Neste runde", font = ("Arial Bold", 22), command=n_r, bg = knapp, activebackground = aktivknapp) # "Neste runde"-knapp
        nesteRunde.place(relx=0.37, rely=0.7)
        
        avslutt2 = Button(window, text="Avslutt", command=a2, font=("Arial Bold", 22), bg = knapp, activebackground = aktivknapp) # Avsluttknapp
        avslutt2.place(relx = 0.843, rely = 0.872)
    def w3_2(): # vindu 3 versjon 2
        fortsett = Button(window, text="Fortsett", font =("Arial Bold", 22), command=w4, bg = knapp, activebackground = aktivknapp) # Fortsettknapp
        fortsett.place(relx=0.41, rely=0.7)

    lbl = ImageLabel(window)
    lbl.place(relx = 0, rely = 0.25)
    lbl.load(filGif)
    # lbl.next_frame.config(heigh = 200)
    # lbl.next_frame.config(width = 800)

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
                    self.e = Entry(window, width=floor(25/runder), font=('Arial',skrift,'bold'), justify = 'center', bd = kant) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, table[j][i])
               
                self.e = Entry(window, width=33-floor(25/runder)*runder, font=('Arial',skrift,'bold'), justify = 'center', bd = kant)
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
 

        opp = Button(window, text="\u2B99", command=pilOpp, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp)
        opp.place(relx = 0.3, rely = 0.35)
        
        ned = Button(window, text="\u2B9b", command=pilNed, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp)
        ned.place(relx = 0.3, rely = 0.53)

        opp2 = Button(window, text="\u2B99", command=pilOpp2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp)
        opp2.place(relx = 0.6, rely = 0.35)
        
        ned2 = Button(window, text="\u2B9b", command=pilNed2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp)
        ned2.place(relx = 0.6, rely = 0.53)
        
        cont = Button(window, text="Fortsett", command=Cont, font=("Arial Bold", 35),bg = knapp, activebackground = aktivknapp)
        cont.place(relx = 0.355, rely = 0.77)
    
    def Recalc():
        global rundenr
        rundenr -= 1
        pointsInTable(winnerTeam, points)
        rundenr += 1


    manually = Button(window, text="Legg til poeng manuelt", font=("Arial bold", 22), command=Manually, bg = knapp, activebackground = aktivknapp)
    manually.place(relx = 0.0005, rely = 0.872)

    recalc = Button(window, text="Sjekk poeng på nytt", font=("Arial bold", 22), command=Recalc, bg = knapp, activebackground = aktivknapp)
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
    elif sc1 < sc2:
         vinnerText = Label(window, text="Vinneren er " + name2, fg = oransjefarge, bg = bakgrunn, font=("Arial Bold", 40))
         vinnerText.place(relx=0.1, rely=0.3)
    else: 
         vinnerText = Label(window, text="Det ble uavgjort", bg = bakgrunn, font=("Arial Bold", 50))
         vinnerText.place(relx=0.17, rely=0.3)
        


logoWindow()


    
window.mainloop()