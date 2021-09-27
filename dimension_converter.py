from tkinter import *
from tkinter import messagebox
import tkinter as tk


test_list = ('AOL', 'OD', 'ID', 'BODY DIA', 'WASHER DIA', 'CHAMFER LEN', 'CHAMFER ANG',
            'JOURNAL DIA', 'RADIUS', 'ANGLE', 'UNDERCUT DIA', 'DEPTH', 'CHAMFER DIA')

def printting():
    global testing
    print("After function")
    testing = root.after(1000, printting)

def on_change(*args):
    #print(args)
          
    value = var_text.get()
    value = value.strip().lower()

    # get data from test_list
    if value == '':
        data = test_list
    else:
        listbox.grid(row=1, column=0)
        data = []
        for item in test_list:
            if value in item.lower():
                data.append(item)                

    # update data in listbox
    listbox_update(data)


def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data 
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:

        listbox.insert('end', item)


def on_select(event):
   
    # display element selected on list
    print('(event) previous:', event.widget.get('active'))
    print('(event)  current:', event.widget.get(event.widget.curselection()))
    print('---')
    #entry.delete(0, END)
    var_text.set(event.widget.get(event.widget.curselection()))

    # entry.insert(0, event.widget.get(event.widget.curselection()))
    listbox.grid_remove()
    # --- main ---

# #test_list = ('apple', 'banana', 'Cranberry', 'dogwood', 'alpha', 'Acorn', 'Anise', 'Strawberry',
#              'appleef', 'old-banana')
def print_out():
    print(entry.get())
    entry.delete(0, END)

root = tk.Tk()

var_text = tk.StringVar()
var_text.trace('w', on_change)

entry = tk.Entry(root, textvariable=var_text)
entry.grid(row=0, column=0)

listbox = tk.Listbox(root)

listbox.bind('<<ListboxSelect>>', on_select)
listbox_update(test_list)
btn = tk.Button(root, text="Save", command=print_out)
btn.grid(row=2, column=0)
testing = root.after(1000, printting)
root.mainloop()