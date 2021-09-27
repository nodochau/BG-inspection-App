from tkinter import *

NAME = ('AOL', 'OD', 'ID', 'BODY DIA', 'WASHER DIA', 'CHAMFER LEN', 'CHAMFER ANG',
        'JOURNAL DIA', 'RADIUS', 'ANGLE', 'UNDERCUT DIA', 'DEPTH', 'CHAMFER DIA', '')


class SearchAndFill:
    def __init__(self, master,  row, col):
        self.row = row
        self.column = col
        self.master = master
        self.var = StringVar()
        self.listbox = Listbox()
        self. my_entry = Entry()
        self.create_entry_box()
        self.create_list_box()

    def create_entry_box(self):
        self.var.trace('w', self.on_change)
        self.my_entry.config(textvariable=self.var, justify='center', font=('Arial', 12, 'bold'))
        self.my_entry.grid(row=self.row, column=self.column, padx=00, pady=5, ipady=5)

    def on_change(self, *args):
        new_data = []
        value = self.var.get().upper()
        for item in NAME:
            if value in item:
                new_data.append(item)
        self.listbox_update(new_data)

    def create_list_box(self):
        self.listbox.grid(row=self.row + 1, column=self.column)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        selection = self.listbox.get(self.listbox.curselection())
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, selection)
        self.listbox.grid_remove()

    def listbox_update(self, data):
        self.listbox.delete(0, END)
        for i in data:
            self.listbox.insert('end', i)