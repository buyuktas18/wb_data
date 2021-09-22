import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from data_analyser import print_time
from data_tool import run_program
import threading
import time

window = tk.Tk()
window.title('White Balance Data Analyse Tool')
window.geometry('600x400')
files = ''
filename = []

var1 = tk.IntVar()
var2 = tk.IntVar()
c1 = tk.Checkbutton(window, text="deviation", variable=var1, onvalue=1, offvalue=0)


c2 = tk.Checkbutton(window, text="change", variable=var2, onvalue=1, offvalue=0)

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

def count_time(thr):
    while(thr.is_alive()):
        t = int(time_label['text'])
        time.sleep(1)
        t = t+1
        time_label['text'] = t

def start_program():
    global filename
    path = fd.askdirectory()
    print(path)
    #multithreading for not responding problem
    thread1 = threading.Thread(target=run_program, args=(filename, path,)) 
    thread2 = threading.Thread(target=count_time, args=[thread1])
    thread1.start()
    thread2.start()

time_label = tk.Label(
    window,
    text="0"
)

run_button = tk.Button(
    window,
    text="RUN",
    command = start_program
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
run_button.pack()
c1.pack()
c2.pack()


time_label.pack()

window.mainloop()