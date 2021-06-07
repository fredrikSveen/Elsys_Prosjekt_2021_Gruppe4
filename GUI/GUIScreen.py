from tkinter import Button, Label, Tk, Entry, END
window = Tk()
window.title("Curling game")
window.geometry('800x480')

#Globale variabler:
runder = 5
rundenr = 1
avsluttBool = False
stones = 0
winner = "blue"
winnerTeam = 2 # input fra openCV (Team Blue = 1, Team Orange = 2, uavgjort = 0)
points = 2 # Input fra openCV (antall poeng til winnerTeam, dersom uavgjort har ikke denne verdien noe å si)
stonesPer = int(1)
stones1 = int(stonesPer)
stones2 = int(stonesPer)
sc1=0
sc2=0

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
        global stones
        avsluttBool = True
        stones = 0
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
    global stones1
    global stones2

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
            pointsInTable(winnerTeam, points)
            global rundenr
            rundenr+=1
            clearFrame()
            window3()

    stonesButton=Button(window, text="Stones", command=s) # "Øke antall steiner"-knapp
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
                    
                    lag1 = Label(window, text="Team Blue", font=("Arial bold", 40))  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", fg = 'orange', font=("Arial bold", 40)) 
                    lag2.place(relx = 0.45, rely = 0.2)


                else:
                    stones1 += 1
                    team1stones["text"] = str(value1 + 1)

                    lag1 = Label(window, text="Team Blue", fg = 'blue', font=("Arial bold", 40))  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", font=("Arial bold", 40)) 
                    lag2.place(relx = 0.45, rely = 0.2)

            if (winner == "blue"):
                if (stones % 2 == 0):
                    stones1 += 1
                    team1stones["text"] = str(value1 + 1)

                    lag1 = Label(window, text="Team Blue", fg = 'blue', font=("Arial bold", 40))  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", font=("Arial bold", 40)) 
                    lag2.place(relx = 0.45, rely = 0.2)
                    
                else:
                    stones2 += 1
                    team2stones["text"] = str(value2 + 1)

                    lag1 = Label(window, text="Team Blue", font=("Arial bold", 40))  
                    lag1.place(relx = 0.05, rely = 0.2)
                    lag2 = Label(window, text="Team Orange", fg = 'orange', font=("Arial bold", 40)) 
                    lag2.place(relx = 0.45, rely = 0.2)
    

    regretStone = Button(window, text="Regret stone", command=regret)
    regretStone.place(relx = 0.6, rely = 0.5)


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
            for i in range(total_rows):
                self.e = Entry(window, width=12, fg='blue', font=('Arial',20,'bold')) 
                self.e.grid(row=i, column=0) 
                self.e.insert(END, table[0][i]) 
                for j in range(1, total_columns): 
                    self.e = Entry(window, width=(4),  fg='blue', font=('Arial',20,'bold')) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, table[j][i])
                self.e = Entry(window, width=11, fg='blue', font=('Arial',20,'bold')) 
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
        global avsluttBool
        global runder
        avsluttBool=False
        runder = 5
        for i in range(1,len(table)):
            table[i][1] = ''
            table[i][2] = ''
        clearFrame()
        window1()
    
    global rundenr
    rundenr = 1
    ns = Button(window, text="New game", command=nyttSpill, font=("Arial Bold", 30)) # "Nytt spill"-knapp
    ns.place(relx=0.35, rely=0.8)
    if sc1 > sc2:
         vinnerText = Label(window, text="The winner is Team Blue", fg = 'blue', font=("Arial Bold", 40))
         vinnerText.place(relx=0.1, rely=0.3)
    elif sc1 < sc2:
         vinnerText = Label(window, text="The winner is Team Orange", fg = 'orange', font=("Arial Bold", 40))
         vinnerText.place(relx=0.1, rely=0.3)
    else: 
         vinnerText = Label(window, text="It's a tie", font=("Arial Bold", 50))
         vinnerText.place(relx=0.3, rely=0.3)
        
window1()
    
window.mainloop()