# import tkinter as tk
# import tktable

# window = tk.Tk()
# window.title("Testvindu")
# window.geometry('800x480')

# table = tktable.Table(window, rows=3, cols=11)
# table.pack(side="top", fill="both", expand=True)
# window.mainloop()

from tkinter import Button, Label, Tk, Entry, END
  
  
runder = 10

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

score1 = 0
score2 = 0
for i in range(1, len(table)):
    score1 += int(table[i][1])
    score2 += int(table[i][2])
print(score1)
print(score2)









   




# |||||||||||\\
#             \\
# //|||||||||||||||||\\
# ||||||||||||||||||||||
# \\|||||||||||||||||//