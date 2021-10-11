import tkinter as tk
from tkinter import filedialog

import time

from kivy.app import App
from kivy.base import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from thread_with_return import ThreadWithReturnValue

from data_tool import run_program
from show_position import create_plot

import threading



class MyApp(App):

    filelist = []
    path = ''
    file_names = []

    def build(self):
        wid = BoxLayout()
        #add file button 
        btn1 = Button(text='add a file')
        btn1.bind(on_release=self.ask_files)

        btn2 = Button(text='Run the program')
        btn2.bind(on_release=self.ask_path)

        btn3 = Button(text='show position')
        btn3.bind(on_release=partial(self.show_pos, '/test/057D40-SW4-NG'))

        wid.add_widget(btn1)
        wid.add_widget(btn2)
        wid.add_widget(btn3)
        return wid

    def ask_files(self, obj):
        root = tk.Tk()
        root.withdraw()
        global filelist
        filelist = filedialog.askopenfilenames(
            title='Add files',
            initialdir='/sample_folder'
        )
        print(filelist)


    def ask_path(self, obj):
        root = tk.Tk()
        root.withdraw()
        global path
        global filelist
        path = filedialog.askdirectory(
            title='Select path',
            initialdir='/test'
        )
        print(path)
        thr1 = ThreadWithReturnValue(target=run_program, args=(filelist, path))
        thr1.start()
        global file_names 
        file_names = thr1.join()
        

    def show_pos(self, p, *largs):
        create_plot(p)

    
    


if __name__ == '__main__':
    MyApp().run()