import tkinter
from tkinter import messagebox

CONTROL_LIMIT = 0.8
ROUND_NUM = 4

class EntryData(tkinter.Entry):
    def __init__(self, master=None, start=None, end=None, bg=None, **kwargs):
        self.start = start
        self.end = end
        self.nominal = round((self.start + self.end)/2, 4)
        self.tol_control_limit = round((self.nominal - self.start) * CONTROL_LIMIT, ROUND_NUM)
        self.data_dict = {} # To store the data base entry box location
        self.data_entry_list = [] # To store the value max and min of the entry box 
        
        super().__init__(master, **kwargs)
        self.var = tkinter.StringVar()
        self.config(textvariable=self.var, justify='center')
        # self.bind('<Tab>', self.check_value)
        self.var.trace('w', self.my_callback)

    def check_value(self, event=None):
        if len(self.data_entry_list) > 0:
            self.data_entry_list.clear() # delete list to ensure just one set of data is sent 
        value = float(self.var.get())
        if self.end is not None and value > self.end:
            self.config(bg='red')
        
        elif self.start is not None and value < self.start:
            self.config(bg='red')
        
        else:
            if self.end is not None and (self.nominal + self.tol_control_limit) <= value <= self.end:
                self.config(bg='yellow')
            elif self.start is not None and self.start <= value <= (self.nominal - self.tol_control_limit):
                self.config(bg='yellow')
            else:
                self.config(bg='green')
        #The dict has entry box location is a key. Value, min, max and nominal values
        loc = str(self.var)
        # self.data_entry_list.append(float(self.var.get()))
        self.data_entry_list.append(value)
        self.data_entry_list.append(self.start)
        self.data_entry_list.append(self.end)
        self.data_entry_list.append(self.nominal)
        self.data_entry_list.append(self.tol_control_limit)
        self.data_dict[loc] = self.data_entry_list
    

    def my_callback(self, *args):
        num_list = '0123456789.'
        for num in self.var.get():
            if num not in num_list:
                messagebox.showerror("Value Entered", "Value entered is invalid")
        if len(self.var.get()) > 0:
            self.check_value()     
        return len(self.var.get())

    def send_data(self):
        return self.data_dict

    def clear_data(self):
        self.delete(0, tkinter.END)
        self.config(bg='white')

    def focus_entry(self):
        self.focus()

    def delete_data(self):
        self.clear_data()
        self.data_dict.clear()

   




        
