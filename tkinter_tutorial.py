import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from data_tool import run_program
import time
import re
from show_position import create_plot
from thread_with_return import ThreadWithReturnValue
import threading


flag = 0
window = tk.Tk()
window.title('White Balance Data Analyse Tool')
window.geometry('600x400')
files = ''
filename = []
my_files = []
path = ''

variables = [0, 0]
var1 = tk.IntVar()
var2 = tk.IntVar()

def log_c1():
    global var1
    global variables
    variables[0] = var1

def log_c2():
    global var2
    global variables
    variables[1] = var2

c1 = tk.Checkbutton(window, text="deviation", variable=var1, onvalue=1, offvalue=0, command=log_c1)
c2 = tk.Checkbutton(window, text="change", variable=var2, onvalue=1, offvalue=0, command=log_c2)

variables.append(var1)
variables.append(var2)



def select_files():
    global filename
    global files
    filename = fd.askopenfilenames(
        title='Add a file',
        initialdir='/'
        
    )

    for f in filename:
        files += f + '\n'

    showinfo(
        title='Selected file',
        message="You have selected these files: \n" + files
    )

def update_label():
    global files
    label['text'] = files

def start_program():
    global filename
    global variables
    global path
    global flag
    global my_files

    path = fd.askdirectory()
    print(path)
    #multithreading for not responding problem
    
    my_files = ['057D40-SW4-NG', '057D43-SW5-NG', '057E32-SW4-NF']
    openNewWindow(filename)    
    

def openNewWindow(options_arr):


    global path
    global my_files
    print("deneme")
    
    for f in my_files:
        p = path+"/"+f
        tk.Button(text=f, command = lambda: create_plot(p)).pack()
    
  
time_label = tk.Label(
    window,
    text="0"
)


path_button = tk.Button(
    window,
    text="Select a path",
    command = start_program
)


run_button = tk.Button(
    window,
    text="RUN",
    #command = lambda: threading.Thread(target=run_program, args=(filename, path, variables)).start()
    command = lambda: run_program(filename, path, variables, window, label)
)

add_button = tk.Button(
    window,
    text='Add files',
    command=update_label
)

open_button = tk.Button(
    window,
    text='Add a file',
    command=select_files
)

label = tk.Label(
    window,
    text = "You have not selected any files yet"
)

open_button.pack()
add_button.pack()
label.pack()
path_button.pack()
run_button.pack()
c1.pack()
c2.pack()


time_label.pack()
window.mainloop()