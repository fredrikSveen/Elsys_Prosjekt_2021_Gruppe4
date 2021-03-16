import tkinter as tk
from tkinter import *

window = tk.Tk()
window.title("Curlingspill")
window.geometry('800x480')


#Globale variabler:
runder = 5
rundenr = 1
avsluttBool = False
    

#Funksjoner
#roundKeeper(tar inn data fra pi-en):
#Øker rundenr med 1 hver gang en stein registreres

def clearFrame(): # destroys all widgets from frame
    for widget in window.winfo_children():
       widget.destroy()
       
def Avslutt():
    w = tk.Tk()
    w.geometry('400x240')  
    v = tk.Label(w, text="Ved å avslutte nå vil ikke \n gjeldende runde være tellende", font=("Arial Bold", 10))
    v.place(relx = 0.2, rely = 0.2)
    def closeW():
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

def window1():
    l = tk.Label(window, text=str(runder), font=("Arial Bold", 60))
    l.place(relx = 0.4, rely = 0.42)
    
    def pilOpp():
        value = int(l["text"])
        if value < 10:
            l["text"] = f"{value + 1}"
            global runder
            runder += 1
    
    def pilNed():
        value = int(l["text"])
        if value > 1:
            l["text"] = f"{value - 1}"
            global runder
            runder -= 1
    
    def Start():
        clearFrame()
        window2()
        
    
    opp = tk.Button(window, text="Pil opp", command=pilOpp, font=("Arial Bold", 30))
    opp.place(relx = 0.5, rely = 0.4)
    
    ned = tk.Button(window, text="Pil ned", command=pilNed, font=("Arial Bold", 30))
    ned.place(relx = 0.5, rely = 0.5)
    
    start = tk.Button(window, text="Start", command=Start, font=("Arial Bold", 25))
    start.place(relx = 0.45, rely = 0.7)

def window2():
    l = tk.Label(window, text=f"Runde {str(rundenr)}", font=("Arial Bold", 40))
    l.place(relx = 0.4)
    
    avslutt = tk.Button(window, text="Avslutt nå", command=Avslutt, font=("Arial Bold", 30))
    avslutt.place(relx = 0.72, rely = 0.83)
    
    lag1 = tk.Label(window, text="Team 1", font=("Arial bold", 40))  
    lag1.place(relx = 0, rely = 0.2)
    lag2 = tk.Label(window, text="Team 2", font=("Arial bold", 40)) 
    lag2.place(relx = 0.5, rely = 0.2)

    

    #simulasjon av steinkast
    totalStones = 4

    stones = 0
    stones1 = int(totalStones/2)
    stones2 = int(totalStones/2)

    team1stones = tk.Label(window, text=f"{stones1} steiner igjen", font=("Arial bold", 30))
    team1stones.place(relx = 0, rely = 0.4)

    team2stones = tk.Label(window, text=f"{stones2} steiner igjen", font=("Arial bold", 30))
    team2stones.place(relx = 0.5, rely = 0.4)

    def s():
        global stones
        stones+=1
        if (stones == totalStones):
            stones = 0
            global rundenr
            rundenr+=1
            clearFrame()
            window3()
            if (stones % 2 == 0):
                global stones2
                stones2 -= 1
                team2stones["text"] = f"{stones2} steiner igjen"
            else:
                global stones1
                stones1 -= 1
                team1stones["text"] = f"{stones1} steiner igjen"

            
    stonesButton=tk.Button(window, text="Steiner", command=s)
    stonesButton.place(relx = 0.5, rely = 0.5)

    
    
def window3():
    def w4():
        clearFrame()
        window4()

    def w3_1(): # vindu 3 layout 1
        def n_r():
            clearFrame()
            window2()
        nesteRunde = tk.Button(window, text="Neste runde", command=n_r)
        nesteRunde.place(relx=0.2, rely=0.8)
        
        avslutt2 = tk.Button(window, text="Avslutt", command=w4)
        avslutt2.place(relx=0.5, rely=0.8)

    def w3_2(): # vindu 3 layout 2
        fortsett = tk.Button(window, text="Fortsett", command=w4)
        fortsett.place(relx=0.4, rely=0.8)

    class Table: 
        def __init__(self,window):  
            # code for creating table 
            for i in range(total_rows):
                self.e = Entry(window, width=12, fg='blue', 
                                    font=('Arial',16,'bold')) 
                self.e.grid(row=i, column=0) 
                self.e.insert(END, table[0][i]) 
                for j in range(1, total_columns): 
                    self.e = Entry(window, width=5, fg='blue', 
                                    font=('Arial',16,'bold')) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, table[j][i])
        
    # take the data 
    table = list(range(runder + 1))
    for i in range(0,runder + 1):
        cols = list(range(3))
        cols[0] = str(i)
        cols[1] = str(3)
        cols[2] = str(3)
        table[i] = cols
    table[0][0] = "Team/Round"
    table[0][1] = "Team 1"
    table[0][2] = "Team 2"
   
    # find total number of rows and 
    # columns in list 
    total_columns = len(table) 
    total_rows = len(table[0]) 

    t = Table(window)

    if avsluttBool or (runder < rundenr):
        w3_2()
        # avsluttBool = False
    else:
        w3_1()


    

def window4():
    def nyttSpill():
        clearFrame()
        window1()
    
    global rundenr
    rundenr = 1

    ns = tk.Button(window, text="Nytt spill", command=nyttSpill, font=("Arial Bold", 30))
    ns.place(relx=0.4, rely=0.8)

    vinner = "Team 1" # legge inn den faktiske vinneren

    vinnerText = tk.Label(window, text="Vinneren er "+vinner, font=("Arial Bold", 30))
    vinnerText.place(relx=0.3, rely=0.3)


window1()
    
window.mainloop()