# import tkinter as tk
# import tktable

# window = tk.Tk()
# window.title("Testvindu")
# window.geometry('800x480')

# table = tktable.Table(window, rows=3, cols=11)
# table.pack(side="top", fill="both", expand=True)
# window.mainloop()

#from tkinter import *
  
  
# class Table: 
      
#     def __init__(self,window): 
          
#         # code for creating table 
#         for i in range(rows): 
#             for j in range(columns): 
                  
#                 self.e = Entry(window, width=20, fg='blue', 
#                                font=('Arial',16,'bold')) 
                  
#                 self.e.grid(row=i, column=j) 
#                 self.e.insert(END, data[i][j]) 
  
# take the data 
#antall runder velges av bruker
runder = 6
table = list(range(runder + 1))
cols = list(range(3))
for i in range(0,7):
    print(i)
    cols[0] = str(i)
    cols[1] = str(3)
    cols[2] = str(3)
    table[i] = cols
print(table)








   
# # find total number of rows and 
# # columns in list 
# rows = len(lst) 
# columns = len(lst[0]) 
   
# # create root window 
# window = Tk() 
# t = Table(window) 
# window.mainloop() 



# |||||||||||\\
#             \\
# //|||||||||||||||||\\
# ||||||||||||||||||||||
# \\|||||||||||||||||//