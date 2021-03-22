import tkinter as tk
from tkinter import Button, Label, Tk, Entry, END
window = tk.Tk()
window.title("Curlingspill")
window.geometry('800x480')
#Globale variabler:
runder = 5
rundenr = 1
avsluttBool = False
stones = 0
#table = [[]]

# Lager liste med resultater
table = list(range(12))
for i in range(0,12):
    cols = list(range(3))
    cols[0] = str(i)        
    cols[1] = ''
    cols[2] = ''
    table[i] = cols
table[0][0] = "Team/Round"
table[0][1] = "Team 1"
table[0][2] = "Team 2"



winnerTeam = 1 # input fra openCV (Team 1 = 1, Team 2 = 2)
points = 2 # Input fra openCV (antall poeng til winnerTeam)


# vinnerlag = 1 # input fra openCV (Team 1 = 1, Team 2 = 2)
# poeng = 2 # Input fra openCV (antall poeng til winnerTeam)

totalStones = 2
stones1 = int(totalStones/2)
stones2 = int(totalStones/2)




def pointsInTable(winnerTeam, points):
    global table
    if winnerTeam == 1:
        table[rundenr][1] = str(points)
        table[rundenr][2] = str(0)
    else:
        table[rundenr][2] = str(points)
        table[rundenr][1] = str(0)


#Funksjoner
#roundKeeper(tar inn data fra pi-en):
#Øker rundenr med 1 hver gang en stein registreres
def clearFrame(): # Destroys all widgets from frame
    for widget in window.winfo_children():
       widget.destroy()
       
def Avslutt(): # Åpner varslingsvindu
    w = tk.Tk()
    w.geometry('400x240')  
    v = tk.Label(w, text="Ved å avslutte nå vil ikke \n gjeldende runde være tellende", font=("Arial Bold", 10))
    v.place(relx = 0.2, rely = 0.2)
    def closeW(): # Lukker vinduet
        w.destroy()
    def A(): #Avsluttknapp i det lille vinduet
        global avsluttBool
        avsluttBool = True
        w.destroy()
        clearFrame()
        window3()
    avsluttSpill = tk.Button(w, text="Avslutt spill",command=A, font=("Arial Bold", 10))
    avsluttSpill.place(relx = 0.6, rely = 0.4)
    
    tilbake = tk.Button(w, text="Tilbake til spillet", command=closeW, font=("Arial Bold", 10))
    tilbake.place(relx = 0.2, rely = 0.4)
def window1(): # Åpner første vindu
    x = tk.Label(window, text="Hvor mange runder vil dere spille?", font=("Arial Bold", 20))
    x.place(relx = 0.25, rely = 0.2)
    l = tk.Label(window, text=str(runder), font=("Arial Bold", 60))
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


    opp = tk.Button(window, text="\u2191", command=pilOpp, font=("Arial Bold", 30)) # Oppknapp
    opp.place(relx = 0.55, rely = 0.35)
    
    ned = tk.Button(window, text="\u2193", command=pilNed, font=("Arial Bold", 30)) # Nedknapp
    ned.place(relx = 0.55, rely = 0.53)
    
    start = tk.Button(window, text="Start", command=Start, font=("Arial Bold", 25)) # Startknapp
    start.place(relx = 0.45, rely = 0.8)

def window2(): # Vinduet under spill


    l = tk.Label(window, text=f"Runde {str(rundenr)}", font=("Arial Bold", 40))
    l.place(relx = 0.4)

    avslutt = tk.Button(window, text="Avslutt nå", command=Avslutt, font=("Arial Bold", 30))
    avslutt.place(relx = 0.72, rely = 0.83)
    
    lag1 = tk.Label(window, text="Team 1", font=("Arial bold", 40))  
    lag1.place(relx = 0.2, rely = 0.2)
    lag2 = tk.Label(window, text="Team 2", font=("Arial bold", 40)) 
    lag2.place(relx = 0.65, rely = 0.2)
    
    stones1 = int(totalStones/2) # Startverdi antall steiner igjen team 1
    stones2 = int(totalStones/2) # Startverdi antall steiner igjen team 1
    
    team1stones = tk.Label(window, text=str(stones1), font=("Arial bold", 30)) # Label antall steiner igjen team 1 (tall)
    team1stones.place(relx = 0, rely = 0.4)
    team1stonesText = tk.Label(window, text="steiner igjen", font=("Arial bold", 30)) # Label antall steiner igjen team 1 (tekst)
    team1stonesText.place(relx = 0.05, rely = 0.4)
    
    team2stones = tk.Label(window, text=str(stones2), font=("Arial bold", 30)) # Label antall steiner igjen team 2 (tall)
    team2stones.place(relx = 0.5, rely = 0.4)
    team2stonesText = tk.Label(window, text="steiner igjen", font=("Arial bold", 30)) # Label antall steiner igjen team 2 (text)
    team2stonesText.place(relx = 0.55, rely = 0.4)

    # Forsøk på å endre "steiner" til "stein" dersom én stein igjen (funker ikke)
    if (stones1 == 1):
        #team1stonesText["text"] = "stein igjen"
        team1stonesText.config(text = "stein igjen")
    
    if (stones2 == 1):
        #team2stonesText["text"] = "stein igjen"
        team2stonesText.config(text = "stein igjen")
    #simulasjon av steinkast
    def s(): # Funksjon til knapp som øker antall steiner kastet ved trykk på knapp, samt reduserer antall steiner igjen på hvert lag
        global stones
        stones+=1
        value1 = int(team1stones["text"])
        value2 = int(team2stones["text"])
        if (stones % 2 == 0):
            global stones2
            stones2 -= 1
            team2stones["text"] = str(value2 - 1)
        else:
            global stones1
            stones1 -= 1
            team1stones["text"] = str(value1 - 1)

        if (stones == totalStones):
            stones = 0
            #pointsInTable(vinnerlag, poeng) # Legger poeng i tabellen
            global rundenr
            rundenr+=1
            clearFrame()
            window3()

    stonesButton=tk.Button(window, text="Steiner", command=s) # "Øke antall steiner"-knapp
    stonesButton.place(relx = 0.5, rely = 0.5)

def window3():
    def w4(): # Åpner vindu 4
        clearFrame()
        window4()
    def w3_1(): # vindu 3 versjon 1
        def n_r(): # Åpner vindu 2
            clearFrame()
            window2()
        def a2(): # Åpner et "sikker på at du vil avslutte"-vindu
            w2 = tk.Tk()
            w2.geometry('400x240')  
            v2 = tk.Label(w2, text="Er du sikker på at du \n vil avslutte nå?", font=("Arial Bold", 10))
            v2.place(relx = 0.2, rely = 0.2)
            def closeW2(): # Lukker det lille vinduet
                w2.destroy()
            def a3(): # Lukker det lille vinduet og åpner vindu 4
                w2.destroy()
                clearFrame()
                window4()
            
            avsluttSpill2 = tk.Button(w2, text="Avslutt spill",command=a3, font=("Arial Bold", 10)) # Avsluttknapp i det lille vinduet
            avsluttSpill2.place(relx = 0.6, rely = 0.4)
            
            tilbake2 = tk.Button(w2, text="Tilbake til spillet", command=closeW2, font=("Arial Bold", 10)) # Fortsettknapp i det lille vinduet
            tilbake2.place(relx = 0.2, rely = 0.4)
        nesteRunde = tk.Button(window, text="Neste runde", command=n_r) # "Neste runde"-knapp
        nesteRunde.place(relx=0.2, rely=0.8)
        
        avslutt2 = tk.Button(window, text="Avslutt", command=a2) # Avsluttknapp
        avslutt2.place(relx=0.5, rely=0.8)
    def w3_2(): # vindu 3 versjon 2
        fortsett = tk.Button(window, text="Fortsett", command=w4) # Fortsettknapp
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
                    self.e = Entry(window, width=5, fg='blue', font=('Arial',16,'bold')) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, table[j][i])
                self.e = Entry(window, width=12, fg='blue', font=('Arial',16,'bold')) 
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
    #global table
    def nyttSpill(): # Starter spillet på nytt (åpner vindu 1)
        global runder
        runder = 5
        clearFrame()
        window1()
        for i in range(1,len(table)):
            table[i][1] = '0'
            table[i][2] = '0'
    
    global rundenr
    rundenr = 1
    ns = tk.Button(window, text="Nytt spill", command=nyttSpill, font=("Arial Bold", 30)) # "Nytt spill"-knapp
    ns.place(relx=0.4, rely=0.8)
    score1 = 0
    score2 = 0
    for i in range(1, runder + 1):
        score1 += int(table[i][1])
        score2 += int(table[i][2])
    if score1 > score2:
         vinnerText = tk.Label(window, text="Vinneren er Team 1", font=("Arial Bold", 50))
    elif score1 < score2:
         vinnerText = tk.Label(window, text="Vinneren er Team 2", font=("Arial Bold", 50))
    else: 
         vinnerText = tk.Label(window, text="Det ble uavgjort", font=("Arial Bold", 50))
    vinnerText.place(relx=0.2, rely=0.3)
        
window1()
    
window.mainloop()