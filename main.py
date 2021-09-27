import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
import matplotlib.animation as animation
import pandas
import tkinter
from tkinter import messagebox
from tkinter import *
from entrydata import EntryData
from pathlib import Path
import winsound
import os
import sys
import win32com.client as wincl
from datetime import date
from button_class import My_Button, MyLabel, MyEntry


BACKGROUND_COLOR = "#B1DDC6"

CONTROL_LIMIT = 0.8
ROUND_NUM = 5
DECIMALS = 6 # length of the data in entry box

def alert(word):
    # Generate voice
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(word)

def validate_name():
    # this function to verify name or serial number is filled required
    global serial_num
    
    if serial_num == 1:
        if serial_entry.get() == '' or name_entry.get() == '':
            return False
        else:
            operator = name_entry.get()
            ser = serial_entry.get()
            return operator, ser
    else:
        if name_entry.get() == "":
            return False
        else:
            operator = name_entry.get()
            ser = 'None'
            return operator, ser
    

def write_to_file():
    # This function is to create setup files and result files in the system
    global num_feature
    global part_counter
    
    if validate_name():
        feature_name = 0 # index in feature_list
        part_counter += 1
        operator, ser = validate_name()
        try: # Check if file with material - order exist 
            with open(f_path, 'r') as rf: # open setup file
                rf.readline()    
                
        except FileNotFoundError:
            with open (wo_path, 'a') as wo_f: # open work file
                with open (f_path, 'a') as ff: # open setup file
                    print("feature", "value", "min", "max", "nominal", "control_limit",
                        "num_feature", "parts", "serial#", "name", "date", sep=',', file=wo_f)
                    print("feature", "value", "min", "max", "nominal", "control_limit",
                        "num_feature", "parts", "serial#", sep=',', file=ff)
                
                    for item in my_entry:
                        the_data = item.send_data()
                        list_data = list(the_data)
                        print(feature_list[feature_name], the_data[list_data[0]][0], the_data[list_data[0]][1], 
                            the_data[list_data[0]][2], the_data[list_data[0]][3], the_data[list_data[0]][4], 
                            num_feature, part_counter, ser.upper(), operator.title(), today, sep=',', file=wo_f)
                        # copy the first set of data to setup file under material number only
                        print(feature_list[feature_name], the_data[list_data[0]][0], the_data[list_data[0]][1], 
                        the_data[list_data[0]][2], the_data[list_data[0]][3], the_data[list_data[0]][4], 
                        num_feature, 0, ser.upper(), sep=',', file=ff)
                        feature_name += 1
                        item.clear_data()
        else:
            try:
                with open(wo_path, 'r') as wo_f:
                    wo_f.readline()
            except FileNotFoundError:
                with open (wo_path, 'a') as wo_f:
                    print("feature", "value", "min", "max", "nominal", "control_limit",
                            "num_feature", "parts", "serial#", "name", "date", sep=',', file=wo_f)
                    for item in my_entry:
                        the_data = item.send_data()
                        list_data = list(the_data)
                        print(feature_list[feature_name], the_data[list_data[0]][0], the_data[list_data[0]][1], 
                            the_data[list_data[0]][2], the_data[list_data[0]][3], the_data[list_data[0]][4], 
                            num_feature, part_counter, ser.upper(), operator.title(), today, sep=',', file=wo_f)
                        feature_name += 1
                        item.clear_data()
            else:
                with open (wo_path, 'a') as wo_f:
                    for item in my_entry:
                        the_data = item.send_data()
                        list_data = list(the_data)
                        print(feature_list[feature_name], the_data[list_data[0]][0], the_data[list_data[0]][1], 
                            the_data[list_data[0]][2], the_data[list_data[0]][3], the_data[list_data[0]][4], 
                            num_feature, part_counter, ser.upper(), operator.title(), today, sep=',', file=wo_f)
                        feature_name += 1
                        item.clear_data()
        serial_entry.delete(0, tkinter.END)
        if serial_num == 1:
            serial_entry.focus()
        else:
            my_entry[0].focus_entry()
        calling = main_wd.after(1000, set_focus)
    else:
        if serial_num == 1:
            alert('Please enter name and serial number')
            messagebox.showinfo('Name-Serial Number Entry Error',  'Please enter name and serial number')
        else:
            alert("Please enter your name in name box")
            messagebox.showinfo('Name Entry Error',  'Please enter your name')
        
        
def cancel():
    # This function to delete all data in entry boxes by using function in EntryBox class
    for item in my_entry:
        item.delete_data()
    if serial_num == 1:
        serial_entry.focus()
    else:
        my_entry[0].focus_entry()
    calling = main_wd.after(1000, set_focus)

def detect_exist_file(a_file):
    # This function to check the file exist or not
    entries = os.scandir(the_path)
    for entry in entries:
        if entry.name == a_file:
            return True
       

def retrieve_data(path):
    # This function toretrieve the data from file which is saved before
    the_data = pandas.read_csv(path)
    total_feature = the_data.at[0, 'num_feature']
    total_parts = the_data.at[len(the_data.parts) - 1, 'parts']
    serial_part = the_data.at[len(the_data.parts) - 1, 'serial#']
    nominal_dim_list = [the_data.at[num, 'nominal'] for num in range(total_feature)]
    control_limit_list = [the_data.at[num, 'control_limit'] for num in range(total_feature)]
    features_list = [the_data.at[num, 'feature'] for num in range(total_feature)]
    min_list =  [the_data.at[num, 'min'] for num in range(total_feature)]
    max_list =  [the_data.at[num, 'max'] for num in range(total_feature)]
    tol_list = [(min_list[i], max_list[i]) for i in range(total_feature)]
    
    return total_feature, total_parts, nominal_dim_list, control_limit_list, tol_list, features_list, serial_part

def confirmation(number):
    # this function to ask user to set up a new job or exit
    my_num = ""
    for i in str(number):
        my_num += i + ', '
    alert(f"The program for material number {my_num} does not exist. Enter Yes to continue. Enter No to exit")
    answer = input("The program does not exist. Enter Y to continue, N to exit Y/N: ")
    if answer.upper() == "Y" or answer.upper() == 'YES':
        return True
    else:
        return False

def turn_on_off(num):
    # This function to allow the serial number entry is editable or nor
    # global serial_num
    if num == 0:
        serial_entry.config(state='disabled', bg=BACKGROUND_COLOR)
    else:
        serial_entry.config(justify='center', state='normal')

def set_focus():
    """This function to set focus automatically when the data length >= DECIMALS constant in the value entries
        inorther to use electronic gages"""
    global calling
    for i in range(len(my_entry) - 1):
        if my_entry[i].my_callback() >= DECIMALS:
            my_entry[i + 1].focus_entry()
    calling = main_wd.after(1000, set_focus) 
    if my_entry[len(my_entry) - 1].my_callback() >= DECIMALS:
        main_wd.focus_set()
        main_wd.after_cancel(calling)
    

# ------------------------------------ REQUEST JOB INFOMATION -------------------------------- #

# Get date
today = date.today()
# Getting infomation of part
feature_list = [] # list of feature name
num_feature = 0 # number of features
alert("Enter material number")
material_num = input('Enter material number: ').strip()
# Create path for file
the_path = 'C:\\Users\\1\\Documents\\Python\\BG_dataTrial'
material_file = material_num + '.csv'
f_path = the_path + '\\' + material_file # path of setup file
# Detect file if it exists in the system then by pass getting info
if not detect_exist_file(material_file):
    if confirmation(material_num):
        data_tol = [] # list of feature tolerances 
        alert("Enter Work Order")
        work_order = input("Enter Work Order: ").strip()
        # create the path for the job with work order and material number
        wo_path =  the_path + '\\' + material_num + '_' + work_order + '.csv'
# ------------------------- window widgets to get data -------------------------------------- #
        _list = [ 'AOL', 'OD', 'ID', 'BODY DIA', 'WASHER DIA', 'CHAMFER LEN', 'CHAMFER ANG',
            'JOURNAL DIA', 'RADIUS', 'ANGLE', 'UNDERCUT DIA', 'DEPTH', 'CHAMFER DIA' ]

        def on_change(*args):
            # This function to monitor the data typed in and searches match feature name
            value = feature_var.get().upper()
            if value == "":
                data = _list
            else:
                data = []
                for item in _list:
                    if value in item:
                        data.append(item)
            update_list_box(data)

        def update_list_box(data):
            listbox.delete(0, END)
            if len(data) > 0 :
                listbox.grid(row=2, column=2)
                for item in data:
                    listbox.insert(END, item)
            else: 
                listbox.grid_remove()

        def on_select(event):
            try:
                selection = event.widget.get(event.widget.curselection())
                feature_var.set(selection)
                listbox.grid_remove()
            except tkinter.TclError:
                pass

        def next():
            # This function to store part infomation such as bubble, feature name, dimension and tolerances
            global var1, check_box_result, validation
            bubble_num = bubble_entry.get()
            feature_name = feature_name_entry.get()
            if bubble_num == '' or feature_name == '':
                messagebox.showerror('Missing data', 'Please fill bubble number and feature name')
            else:
                if '#' in bubble_num:
                    feature_name = bubble_num + ' ' + feature_name
                else:
                    feature_name = '#' + bubble_num + ' ' + feature_name
                max_dim = max_ent.get()
                min_dim = min_ent.get()
                if max_dim == '' or min_dim == '':
                    nominal_dim = nom_ent.get()
                    plus_tol = plus_ent.get()
                    minus_tol = minus_ent.get()
                    if nominal_dim == '' or plus_tol == '' or minus_tol == '':
                        messagebox.showerror("Missing data", "Please fill up nominal and tolerances or max, min dimension")
                    else:
                        max_dim = round(float(nominal_dim ) + float(plus_tol), ROUND_NUM)
                        min_dim = round(float(nominal_dim) - float(minus_tol), ROUND_NUM)
                else:
                    max_dim = round(float(max_dim), ROUND_NUM)
                    min_dim = round(float(min_dim), ROUND_NUM)
                val = var1.get()
            if check_box_result == 0:
                check_box_result = 1
                validation = val
                feature_list.append(feature_name)
                data_tol.append((min_dim, max_dim))
                bubble_entry.focus()
                delete_all()
            else:
                if val != validation:
                    if validation == 0:
                        messagebox.showerror('Serial number error', 'Please check the Serial number requirement\n'  +
                                                'The previous part not requires serial number')
                    else:
                        messagebox.showerror('Serial number error', 'Please check off the Serial number requirement')
                else:
                    feature_list.append(feature_name)
                    data_tol.append((min_dim, max_dim))
                    bubble_entry.focus()
                    delete_all()
            feature_name_entry.delete(0, tkinter.END)
            listbox.grid_remove()
           
        def create_setup_file():
            global num_feature, serial_num
            num_feature = len(feature_list)
            serial_num = validation
            with open (f_path, 'a') as ff: # open to write data to setup file
                print("feature", "value", "min", "max", "nominal", "control_limit",
                        "num_feature", "parts", "serial#", sep=',', file=ff)
                for i in range(len(feature_list)):
                    minn, maxx = data_tol[i]
                    print(f"minn: {minn}, maxx: {maxx}")
                    nominal = round((maxx + minn)/2, ROUND_NUM)
                    print(f"nominal: {nominal}")
                    control_lim = round((nominal - minn) * CONTROL_LIMIT, ROUND_NUM)
                    print(f"control limit: {control_lim}")
                    print(feature_list[i], 0, minn, maxx, nominal, control_lim, 
                          len(feature_list), 0, serial_num, sep=',', file=ff)
            result = messagebox.askyesno("Program is ready", "Click Yes to run the program.\nClick No to Exit")
            if  result == False:
                alert("The setup is completed")
                messagebox.showinfo("Notice", "The setup is completed")
                sys.exit()
            window.destroy()

        def close():
            bubble_num = bubble_entry.get()
            if bubble_num != "":
                next()
                create_setup_file()
            else:
                create_setup_file()

        def delete_all():
            nom_ent.clear_data()
            plus_ent.clear_data()
            minus_ent.clear_data()
            max_ent.clear_data()
            min_ent.clear_data()
            bubble_entry.delete(0, END)
            feature_name_entry.delete(0, END)

        # -----------------------GLOBAL VARIABLES FOR WINDOW WIDGET----------------- #
        check_box_result = 0
        validation =  0
        # --------------------------------------------------------------------------- #
        window = Tk()
        window.title('SET UP FEATURES')
        w = 900 # width for the Tk root
        h = 500 # height for the Tk root

        # get screen width and height
        ws = window.winfo_screenwidth() # width of the screen
        hs = window.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        temp = ""
        # ------------------------------FRAME-1------------------------------------- #
        frame1_color = '#5eaaa8'
        frame1_font = ('Arial', 12, 'bold')
        frame1 = Frame(window, width=800, height=100, bg=frame1_color)
        frame1.pack(fill=BOTH, expand=True)
        frame1.columnconfigure([0, 2], weight=1)
        frame1.rowconfigure([0, 2], weight=1)
        # Don't use button_class cause it does not need trace data
        bubble_lbe = Label(frame1, text="Bubble#", bg=frame1_color, font=frame1_font)
        bubble_lbe.grid(row=0, column=0, pady=5)
        bubble_entry = Entry(frame1, justify='center',font=frame1_font)
        bubble_entry.grid(row=1, column=0, padx=00, pady=5, ipady=5)


        feature_name_lbe = Label(frame1, text="FEATURE NAME", bg=frame1_color, font=frame1_font)
        feature_name_lbe.grid(row=0, column=1, columnspan=2, pady=5)
        feature_var = StringVar()
        feature_var.trace('w', on_change)
        feature_name_entry = Entry(frame1, justify='center', textvariable=feature_var, font=frame1_font)
        feature_name_entry.grid(row=1, column=1, columnspan=2, padx=50, pady=5, sticky='news', ipady=5)

        listbox = Listbox(frame1)
        listbox.bind('<<ListboxSelect>>', on_select)

        var1 = IntVar()
        my_check_box = Checkbutton(frame1, text="Serial number is required", bg=frame1_color,
                                    variable=var1, onvalue=1, offvalue=0)
        my_check_box.grid(row=2, column=1, columnspan=2, padx=20, pady=5, sticky='w')

        # ------------------------------FRAME-2------------------------------------- #
        frame2_color = '#a3d2ca'
        frame2 = Frame(window, width=800, height=300, bg=frame2_color)
        frame2.pack(fill=BOTH, expand=True)
        frame2.columnconfigure([0, 2], weight=1)
        frame2.rowconfigure([0, 2], weight=1)

        dim_lbe = MyLabel(frame2, "Dimension - Tolerance", 0, 1, frame1_font,'black', frame2_color)
        dim_lbe.grid(padx=5, pady=5)
        max_lbe = MyLabel(frame2, "Max-Dim", 1, 0, frame1_font,'black', frame2_color)
        max_lbe.grid(padx=5, pady=5)
        max_ent = MyEntry(frame2, 2, 0)
        min_lbe = MyLabel(frame2, "Min-Dim", 3, 0, frame1_font,'black', frame2_color)
        min_lbe.grid(padx=5, pady=5)
        min_ent = MyEntry(frame2, 4, 0)
        nom_lbe = MyLabel(frame2, "Nominal", 2, 1, frame1_font,'black', frame2_color)
        nom_lbe.grid(padx=5, pady=5)
        nom_ent = MyEntry(frame2, 3, 1)
        plus_lbe = MyLabel(frame2, "PlusTol", 1, 2, frame1_font,'black', frame2_color)
        plus_lbe.grid(padx=5, pady=5)
        plus_ent = MyEntry(frame2, 2, 2)
        plus_ent.grid(padx=5, pady=10)
        minus_lbe = MyLabel(frame2, "MinusTol", 3, 2, frame1_font,'black', frame2_color)
        minus_lbe.grid(padx=5, pady=10)

        minus_ent = MyEntry(frame2, 4, 2)
        minus_ent.grid(padx=5, pady=10)
        # ------------------------------FRAME-3------------------------------------- #
        frame3_color = '#4e8d7c'
        frame3 = Frame(window, width=800, height=100, bg=frame3_color)
        frame3.pack(fill=BOTH, expand=True)
        frame3.columnconfigure([0, 2], weight=1)

        next_btn = My_Button(frame3, "NEXT", 0, 0, next, 30)
        save_btn = My_Button(frame3, 'CLOSE', 0, 1, close, 30)
        cancel_btn = My_Button(frame3, 'CANCEL', 0, 2, cancel, 30)
        part_counter = 0 # count number of parts
        serial_num = validation # equal 1 if serial# is required
       
        window.mainloop()
    else:
        alert("You cancelled the program. Good Bye!")
        sys.exit()
else:
    # retrieve data from setup file
    alert("Enter Work Order")
    work_order = input("Enter Work Order: ")
    the_file = material_num + '_' + work_order + '.csv' # path of work order file
    wo_path =  the_path + '\\' + material_num + '_' + work_order + '.csv'
    if detect_exist_file(the_file):
        num_feature, part_counter, _, _, data_tol, feature_list, serial_exist = retrieve_data(wo_path)
    else:
        num_feature, part_counter, _, _, data_tol, feature_list, serial_exist = retrieve_data(f_path)
    if serial_exist == 0 or serial_exist == 'NONE':
        serial_num = 0
    else:
        serial_num = 1
# -------------------------------Main GUI of inspecting parts-------------------------------- #
main_wd = tkinter.Tk()
main_wd.title(f"{material_num} - {work_order} Data entry")
main_wd.configure(bg=BACKGROUND_COLOR, border=0)
main_wd.rowconfigure([0, 4], weight=1)
my_entry = []
my_entry_var = [] # Stringvar of entry in tkinter - location of entry box

# -------------------------------Create name entry and serial entry ---------------------------- #
name_label = tkinter.Label(main_wd, text='Name', font=('Arial', 8, 'italic'), bg=BACKGROUND_COLOR)
name_label.grid(row=0, column=0)
name_entry = tkinter.Entry(main_wd, width=15)
name_entry.grid(row=1, column=0, padx=5, pady=5, ipady=5)
name_entry.config(justify='center')
serial_label = tkinter.Label(main_wd, text='Serial#', font=('Arial', 8, 'italic'), bg=BACKGROUND_COLOR)
serial_label.grid(row=2, column=0)
serial_entry = tkinter.Entry(main_wd, width=15)
serial_entry.grid(row=3, column=0, padx=5, pady=5, ipady=7)
turn_on_off(serial_num)
# ------------------------------- Create entry value boxes ----------------------------- #
for i in range(1, num_feature + 1):
    minus, plus = data_tol[i - 1]
    main_wd.columnconfigure(i, weight=1)
    label = tkinter.Label(main_wd, text=feature_list[i - 1], font=('Arial', 9, 'bold'), fg='blue', bg=BACKGROUND_COLOR)
    label.grid(row=0, column=i)
    max_label = tkinter.Label(main_wd, text=f"max: {plus}", font=('Arial', 8, 'italic'), bg=BACKGROUND_COLOR)
    max_label.grid(row=1, column=i)
    min_label = tkinter.Label(main_wd, text=f"min: {minus}", font=('Arial', 8, 'italic'), bg=BACKGROUND_COLOR)
    min_label.grid(row=2, column=i)
    entry = EntryData(main_wd, start=minus, end=plus, font="Helvetica 14 bold")
    entry.grid(row=3, column=i, padx=5, pady=5, ipady=5)  # ipady to increase the height of entry box
    my_entry.append(entry)
calling = main_wd.after(1000, set_focus)
send_btn = tkinter.Button(main_wd, text="SEND", command=write_to_file)
send_btn.grid(row=4, column=num_feature - 1, padx=5, pady=5, sticky='news')
cancel_btn = tkinter.Button(main_wd, text="CANCEL", command=cancel)
cancel_btn.grid(row=4, column=num_feature, padx=5, pady=5, sticky='news')

# -------------------------------- ANIMATE GRAPH---------------------------------- #
def animate(k):
    """This function to animate the graph"""
    try:
        _, _ , nominal_dim_list, control_limit_list, _, _, _ = retrieve_data(f_path)
        data = pandas.read_csv(wo_path)
        x = []
        y = []
        last_value = [] # to store the last value in each entry box in orther to set color 
        for var in feature_list:
            data_var = data[data.feature == var]
            data_point = data_var['value'].to_list() # list of data in each entry box (feature)
            last_point = data_point[-1] # the last value in each entry box (feature)
            part_x = [] # determind number of parts by counting number of data in entry data
            for i in range(len(data_point)):
                part_x.append(int(i) + 1) 
            
            x.append(part_x) # list of number of parts
            y.append(data_point) # list of value of features
            last_value.append(last_point) # list of last value of each feature

        for i in range(len(feature_list)):
            ax = plt.subplot(1, len(feature_list), i + 1)
            ax.clear()
            ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # Set x axis at integer only
            ax.plot(x[i], y[i], marker='o',markerfacecolor='cyan')
            ax.set_title(feature_list[i])
            ymin, ymax = data_tol[i]
            y_lower = ymin - (control_limit_list[i] / 10) # Set limit for figure (graph)
            y_upper = ymax + (control_limit_list[i] / 10)
            ymin_cl = nominal_dim_list[i] - control_limit_list[i]
            ymax_cl = nominal_dim_list[i] + control_limit_list[i]
            # Set color for graph base on last value of feature
            if last_value[i] <= ymin or last_value[i] >= ymax:
                ax.set_facecolor('#ff577f')
            elif ymin < last_value[i] <= ymin_cl or ymax_cl <= last_value[i] < ymax:
                ax.set_facecolor('#ffd56b')
            elif ymin_cl < last_value[i] < ymax_cl:
                ax.set_facecolor('#dff3e3')

            ax.axhline(y=ymin, color='red', linestyle="--")
            ax.axhline(y=ymax, color='red', linestyle="--")
            ax.axhline(y=ymin_cl, color='#fc8621', linestyle="--")
            ax.axhline(y=ymax_cl, color='#fc8621', linestyle="--")
            ax.set_ylim((y_lower, y_upper), auto=True) # set limit for y axis
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f')) # Set decimal places to 4 on y axis

    except FileNotFoundError:
        pass

fig = plt.figure(figsize=(13, 4))
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
main_wd.mainloop()