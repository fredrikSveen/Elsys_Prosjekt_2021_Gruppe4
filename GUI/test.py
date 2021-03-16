# import tkinter as tk
# import tktable

# window = tk.Tk()
# window.title("Testvindu")
# window.geometry('800x480')

# table = tktable.Table(window, rows=3, cols=11)
# table.pack(side="top", fill="both", expand=True)
# window.mainloop()

from tkinter import *
  
  
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
   
# find total number of rows and 
# columns in list 
total_columns = len(table) 
total_rows = len(table[0]) 
   
# create window 
window = Tk() 
t = Table(window) 
window.mainloop()
  
# take the data 
#antall runder velges av bruker
# runder = 6
# table = list(range(runder + 1))
# for i in range(0,7):
#     cols = list(range(3))
#     cols[0] = str(i)
#     cols[1] = str(3)
#     cols[2] = str(3)
#     table[i] = cols
# table[0][0] = "Team/Round"
# table[0][1] = "Team 1"
# table[0][2] = "Team 2"
# print(table)








   




# |||||||||||\\
#             \\
# //|||||||||||||||||\\
# ||||||||||||||||||||||
# \\|||||||||||||||||//