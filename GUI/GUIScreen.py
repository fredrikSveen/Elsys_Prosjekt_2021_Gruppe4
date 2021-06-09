from tkinter import Button, Label, Tk, Entry, END, PhotoImage, NW, Canvas
#from PIL import ImageTk,Image
from math import floor
window = Tk()
window.config(bg = "palegreen")
window.title("Curling game")
window.geometry('800x480')

#Globale variabler:
runder = 5
rundenr = 1
avsluttBool = False
stones = 0
winner = "blue"
winnerTeam = 1 # input fra openCV (Team Blue = 1, Team Orange = 2, uavgjort = 0)
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
    v = Label(w, text="By exiting now the\n current round won't count", font=("Arial Bold", 10), bg = bakgrunn)
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

    avsluttSpill = Button(w, text="End game", command=A, font=("Arial Bold", 16),bg = knapp, activebackground = aktivknapp)
    avsluttSpill.place(relx = 0.35, rely = 0.65)
    
    tilbake = Button(w, text="Back to the game", command=closeW, font=("Arial Bold", 16),bg = knapp, activebackground = aktivknapp)
    tilbake.place(relx = 0.25, rely = 0.4)

def window1(): # Åpner første vindu
    x = Label(window, text="Choose number of rounds and stones per team", font=("Arial Bold", 20), bg = bakgrunn)
    x.place(relx = 0.1, rely = 0.1)
    chooseRounds = Label(window, text="Rounds:", font=("Arial Bold", 20), bg = bakgrunn)
    chooseRounds.place(relx = 0.27, rely = 0.25)
    chooseStones = Label(window, text="Stones:", font=("Arial Bold", 20), bg = bakgrunn)
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

    opp = Button(window, text="\u2B99", command=pilOpp, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp) # Oppknapp
    opp.place(relx = 0.3, rely = 0.35)
    
    ned = Button(window, text="\u2B9b", command=pilNed, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Nedknapp
    ned.place(relx = 0.3, rely = 0.53)

    opp2 = Button(window, text="\u2B99", command=pilOpp2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Oppknapp steiner
    opp2.place(relx = 0.6, rely = 0.35)
    
    ned2 = Button(window, text="\u2B9b", command=pilNed2, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp) # Nedknapp steiner
    ned2.place(relx = 0.6, rely = 0.53)
    
    start = Button(window, text="Start", command=Start, font=("Arial Bold", 40),bg = knapp, activebackground = aktivknapp) # Startknapp
    start.place(relx = 0.39, rely = 0.77)

def window2(): # Vinduet under spill
    global stones1
    global stones2

    l = Label(window, text=f"Round {str(rundenr)}", font=("Arial", 55, 'bold italic'),bg = bakgrunn)
    l.place(relx = 0.3)

    avslutt = Button(window, text="Quit", command=Avslutt, font=("Arial Bold", 30),bg = knapp, activebackground = aktivknapp)
    avslutt.place(relx = 0.856, rely = 0.83)
    
    # Forstørre Team Blue og Team oransje og midtstille. Dette må også gjøres i s- og regret-funksjonen
    if winner == 'blue':
        lag1 = Label(window, text="Team Blue", fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
        lag1.place(relx = 0.05, rely = 0.2)
        lag2 = Label(window, text="Team Orange", font=("Arial bold", 40),bg = bakgrunn) 
        lag2.place(relx = 0.45, rely = 0.2) 
    else: 
        lag1 = Label(window, text="Team Blue", font=("Arial bold", 40),bg = bakgrunn)  
        lag1.place(relx = 0.05, rely = 0.2)
        lag2 = Label(window, text="Team Orange", fg = oransjefarge, bg = bakgrunn, font=("Arial bold", 40)) 
        lag2.place(relx = 0.45, rely = 0.2)         

    
    stones1 = stonesPer # Startverdi antall steiner igjen team 1
    stones2 = stonesPer # Startverdi antall steiner igjen team 2
    
    team1stones = Label(window, text=str(stones1), font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 1 (tall)
    team1stones.place(relx = 0, rely = 0.4)
    team1stonesText = Label(window, text="Stone(s) left", font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 1 (tekst)
    team1stonesText.place(relx = 0.05, rely = 0.4)
    
    team2stones = Label(window, text=str(stones2), font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 2 (tall)
    team2stones.place(relx = 0.5, rely = 0.4)
    team2stonesText = Label(window, text="Stone(s) left", font=("Arial bold", 30),bg = bakgrunn) # Label antall steiner igjen team 2 (text)
    team2stonesText.place(relx = 0.55, rely = 0.4)

    #simulasjon av steinkast
    def s(): # Funksjon til knapp som øker antall steiner kastet ved trykk på knapp, samt reduserer antall steiner igjen på hvert lag
        global stones
        global stones2
        global stones1
        stones+=1
        value1 = int(team1stones["text"])
        value2 = int(team2stones["text"])
        if winner == "blue":
            if (stones % 2 == 0):
                stones2 -= 1
                team2stones["text"] = str(value2 - 1)
                lag1 = Label(window, text="Team Blue", fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", bg = bakgrunn, font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
            else:
                stones1 -= 1
                team1stones["text"] = str(value1 - 1)
                lag1 = Label(window, text="Team Blue", bg = bakgrunn, font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", fg = "darkorange3", bg = bakgrunn, font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
        else:
            if (stones % 2 == 0):
                stones1 -= 1
                team1stones["text"] = str(value1 - 1)
                lag1 = Label(window, text="Team Blue", bg = bakgrunn, font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", fg = oransjefarge, font=("Arial bold", 40),bg = bakgrunn) 
                lag2.place(relx = 0.45, rely = 0.2)
            else:
                stones2 -= 1
                team2stones["text"] = str(value2 - 1)
                lag1 = Label(window, text="Team Blue", fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                lag1.place(relx = 0.05, rely = 0.2)
                lag2 = Label(window, text="Team Orange", bg = bakgrunn, font=("Arial bold", 40)) 
                lag2.place(relx = 0.45, rely = 0.2)
        
        if (stones == stonesPer*2):
            stones = 0
            pointsInTable(winnerTeam, points)
            global rundenr
            rundenr+=1
            clearFrame()
            window3()

    stonesButton=Button(window, text="Stones", command=s, bg = knapp, activebackground = aktivknapp) # "Øke antall steiner"-knapp
    stonesButton.place(relx = 0.5, rely = 0.5)

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
                    team2stones["text"] = str(value2 + 1)
                    
                    lag1 = Label(window, text="Team Blue", font=("Arial bold", 40), bg = bakgrunn)  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", fg = oransjefarge, bg = bakgrunn, font=("Arial bold", 40)) 
                    lag2.place(relx = 0.45, rely = 0.2)


                else:
                    stones1 += 1
                    team1stones["text"] = str(value1 + 1)

                    lag1 = Label(window, text="Team Blue", fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", font=("Arial bold", 40), bg = bakgrunn) 
                    lag2.place(relx = 0.45, rely = 0.2)

            if (winner == "blue"):
                if (stones % 2 == 0):
                    stones1 += 1
                    team1stones["text"] = str(value1 + 1)

                    lag1 = Label(window, text="Team Blue", fg = 'blue', bg = bakgrunn, font=("Arial bold", 40))  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", font=("Arial bold", 40), bg = bakgrunn) 
                    lag2.place(relx = 0.45, rely = 0.2)
                    
                else:
                    stones2 += 1
                    team2stones["text"] = str(value2 + 1)

                    lag1 = Label(window, text="Team Blue", font=("Arial bold", 40), bg = bakgrunn)  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", fg = oransjefarge, bg = bakgrunn, font=("Arial bold", 40)) 
                    lag2.place(relx = 0.45, rely = 0.2)
    
    # Justere plasseringen(midtstilt?) og teksstørrelsen(større) til denne knappen
    regretStone = Button(window, text="Regret stone", font=("Arial bold", 25), command=regret, bg = knapp, activebackground = aktivknapp)
    regretStone.place(relx = 0, rely = 0.858)

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

    img = ImageTk.PhotoImage(pinkL.resize((100, 100))) 
    label = Label(window, image=img, bg = bakgrunn)
    label.image = img
    label.place(relx = 0.3, rely = 0.25)




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
            v2 = Label(w2, text="Are you sure you\n want to quit now?", font=("Arial Bold", 10), bg = bakgrunn)
            v2.place(relx = 0.35, rely = 0.2)
            def closeW2(): # Lukker det lille vinduet
                w2.destroy()
            def a3(): # Lukker det lille vinduet og åpner vindu 4
                w2.destroy()
                clearFrame()
                window4()
            
            avsluttSpill2 = Button(w2, text="End game",command=a3, font=("Arial Bold", 16),bg = knapp, activebackground = aktivknapp) # Avsluttknapp i det lille vinduet
            avsluttSpill2.place(relx = 0.35, rely = 0.65)
            
            tilbake2 = Button(w2, text="Back to the game", command=closeW2, font=("Arial Bold", 16), bg = knapp, activebackground = aktivknapp) # Fortsettknapp i det lille vinduet
            tilbake2.place(relx = 0.25, rely = 0.4)
        nesteRunde = Button(window, text="Next round", font = ("Arial Bold", 30), command=n_r, bg = knapp, activebackground = aktivknapp) # "Neste runde"-knapp
        nesteRunde.place(relx=0.35, rely=0.6)
        
        avslutt2 = Button(window, text="Quit", command=a2, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp) # Avsluttknapp
        avslutt2.place(relx = 0.856, rely = 0.83)
    def w3_2(): # vindu 3 versjon 2
        fortsett = Button(window, text="Continue", font =("Arial Bold", 30), command=w4, bg = knapp, activebackground = aktivknapp) # Fortsettknapp
        fortsett.place(relx=0.36, rely=0.6)

    table[runder + 1][0] = 'Total score'
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

            self.e = Entry(window, width=12, font=('Arial',skrift,'bold'), bd = kant)
            self.e.grid(row=0, column=0) 
            self.e.insert(END, table[0][0]) 

            self.e = Entry(window, width=12, font=('Arial',skrift,'bold'), fg = 'blue', bd = kant) 
            self.e.grid(row=1, column=0) 
            self.e.insert(END, table[0][1]) 

            self.e = Entry(window, width=12, font=('Arial',skrift,'bold'), fg = 'orange', bd = kant) 
            self.e.grid(row=2, column=0) 
            self.e.insert(END, table[0][2])
            for i in range(total_rows):
                for j in range(1, runder+1): 
                    self.e = Entry(window, width=floor(20/runder), font=('Arial',skrift,'bold'), justify = 'center', bd = kant) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, table[j][i])
               
            self.e = Entry(window, width=32-floor(20/runder)*runder, font=('Arial',skrift,'bold'), justify = 'left', bd = kant)
            self.e.grid(row=0, column=runder + 1) 
            self.e.insert(END, table[runder + 1][0])
            self.e = Entry(window, width=32-floor(20/runder)*runder, font=('Arial',skrift,'bold'), justify = 'center', bd = kant) 
            self.e.grid(row=1, column=runder + 1) 
            self.e.insert(END, table[runder + 1][1])

            self.e = Entry(window, width=32-floor(20/runder)*runder, font=('Arial',skrift,'bold'), justify = 'center', bd = kant) 
            self.e.grid(row=2, column=runder + 1) 
            self.e.insert(END, table[runder + 1][2])
 

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
    ns = Button(window, text="New game", command=nyttSpill, font=("Arial Bold", 30), bg = knapp, activebackground = aktivknapp) # "Nytt spill"-knapp
    ns.place(relx=0.35, rely=0.6)

    # Forstørr og midtstill
    if sc1 > sc2:
         vinnerText = Label(window, text="The winner is Team Blue", fg = 'blue', bg = bakgrunn, font=("Arial Bold", 40))
         vinnerText.place(relx=0.1, rely=0.3)
    elif sc1 < sc2:
         vinnerText = Label(window, text="The winner is Team Orange", fg = oransjefarge, bg = bakgrunn, font=("Arial Bold", 40))
         vinnerText.place(relx=0.07, rely=0.3)
    else: 
         vinnerText = Label(window, text="It's a tie", bg = bakgrunn, font=("Arial Bold", 50))
         vinnerText.place(relx=0.35, rely=0.3)
        
window1()

    
window.mainloop()