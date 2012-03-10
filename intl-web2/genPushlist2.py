from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import re
import codecs

#提取filenames,返回list
def genPushList(filename): 
	f=codecs.open(filename,"r","utf-8")
	content=str(f.read())
	content=content.replace('\\','/')
	#print(content)
	p=re.compile('mm_filename=".*/(../.*?)"')
	pushlist=list(set(p.findall(content)))
	temp=pushlist[:]
	for file in temp:
		if '_bak' in file.lower(): pushlist.remove(file) #忽略_BAK的大小写
	#print(str(pushlist))
	return pushlist

root = Tk()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

text = Text(mainframe, width=1000, height=800)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()

