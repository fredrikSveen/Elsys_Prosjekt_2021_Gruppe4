import tkinter as tk

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
    w.geometry('401x240')  
    v = tk.Label(w, text="Ved å avslutte nå vil ikke \n gjeldende runde være tellende", font=("Arial Bold", 10))
    v.place(relx = 0.2, rely = 0.2)
    def closeW():
        w.destroy()

    def A(): #Avsluttknapp i det lille vinduet
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

    if avsluttBool:
        w3_2()
        #avsluttBool = False
    else:
        w3_1()

def window4():
    def nyttSpill():
        clearFrame()
        window1()
        
    ns = tk.Button(window, text="Nytt spill", command=nyttSpill, font=("Arial Bold", 30))
    ns.place(relx=0.4, rely=0.8)

    vinner = "Team 1" # legge inn den faktiske vinneren

    vinnerText = tk.Label(window, text="Vinneren er "+vinner, font=("Arial Bold", 30))
    vinnerText.place(relx=0.3, rely=0.3)


window1()
    
window.mainloop()