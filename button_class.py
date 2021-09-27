import tkinter
from tkinter import messagebox

class My_Button(tkinter.Button):
    def __init__(self, master, text: str, row: int, col: int, command: str, width: int,  color: str=None, **kwargs):
        self.text = text
        self.width = width
        self.row = row
        self.column = col
        self.command = command
        self.color = color
        self.pady = 40
        super().__init__(master=master, width=self.width)
        self['bg'] = self.color
        self['text'] = self.text
        self['command'] = self.command
        self.grid(row=self.row, column=self.column, pady=self.pady)


class MyLabel(tkinter.Label):
    def __init__(self, master, text: str, row: int, col: int, font: tuple=None, fill: str=None, color: str=None, **kw):
        super().__init__(master=master)
        self.text = text
        self.row = row
        self.color = color
        self.column = col
        self.font=font
        self.fill = fill
        self['fg'] = self.fill
        self['bg'] = self.color
        self['text'] = self.text
        self['font'] = self.font
        self.grid(row=self.row, column=self.column)


class MyEntry(tkinter.Entry):
    def __init__(self, master, row: int, col: int, **kwargs):
        super().__init__(master)
        self.row = row
        self.ipy = 5
        self.column = col
        self.grid(row=self.row, column=self.column, ipady=self.ipy)
        self.var = tkinter.StringVar()
        self.config(textvariable=self.var, justify='center', font=('Arial', 12, 'bold'))
        self.var.trace('w', self.my_callback)

    def my_callback(self, *args):
        num_list = '0123456789.'
        for num in self.var.get():
            if num not in num_list:
                messagebox.showerror("Value Entered", "Value entered is invalid")

    def retrieve_data(self):
        return self.get()

    def clear_data(self):
        self.delete(0, tkinter.END)
        

class MyWindow(tkinter.Tk):
    def __init__(self, wd_title: str, width: int=None, height: int=None, **kw):
        super().__init__()
        self._geom = '200x200+0+0'
        self.width = width
        self.height = height
        self.title(wd_title)
        self.set_screen()
        self.bind('<Escape>',self.toggle_geom)  # Bind with Escape button

    def toggle_geom(self, event):
        # Resize the window by pressing Escape button
        self.geometry(self._geom)

    def set_screen(self):
        # function to set screen at width and height
        try:
            self.geometry(f"{self.width}x{self.height}")
        except tkinter.TclError:
            self.geometry(self._geom)
        
    def minnimize(self):
        self.iconify()

    def restore(self):
        self.deiconify()
        


        

    
