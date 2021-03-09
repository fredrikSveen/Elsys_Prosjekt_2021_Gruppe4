import tkinter as tk

window = tk.Tk()
window.title("Curlingspill")
window.geometry('800x480')


#Globale variabler:
runder = 5
    

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
    
    avsluttSpill = tk.Button(w, text="Avslutt spill", font=("Arial Bold", 10))
    avsluttSpill.place(relx = 0.6, rely = 0.4)
    
    tilbake = tk.Button(w, text="Tilbake til spillet", commannd=quit, font=("Arial Bold", 10))
    tilbake.place(relx = 0.2, rely = 0.4)       

def window1():
    runder = 5
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
    rundenr = 1
    l = tk.Label(window, text=f"Runde {str(rundenr)}", font=("Arial Bold", 40))
    l.place(relx = 0.4)
    
    avslutt = tk.Button(window, text="Avslutt nå", command=Avslutt, font=("Arial Bold", 30))
    avslutt.place(relx = 0.72, rely = 0.83)
    
    lag1 = tk.Label(window, text="Team 1", font=("Arial bold", 40))  
    lag1.place(relx = 0, rely = 0.2)
    lag2 = tk.Label(window, text="Team 2", font=("Arial bold", 40)) 
    lag2.place(relx = 0.5, rely = 0.2)
    
def window3():
    fortsett = tk.Button(window, text="Fortsett", command=Avslutt, font=("Arial Bold", 30))
    fortsett.place(relx = 0.72, rely = 0.83)
    
    avslutt = tk.Button(window, text="Avslutt", command=Avslutt, font=("Arial Bold", 30))
    avslutt.place(relx = 0.72, rely = 0.83)   


window1()
    

window.mainloop()
