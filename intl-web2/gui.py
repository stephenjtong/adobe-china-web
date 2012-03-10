from tkinter import filedialog
from tkinter import *
from tkinter import ttk
root = Tk()


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
filename=StringVar()

filename = filedialog.askopenfilename()

ttk.Label(mainframe, textvariable=type(filename)).grid()

root.mainloop()