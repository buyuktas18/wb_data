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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label

from data_tool import run_program
from show_position import create_plot

import threading

sm = ScreenManager()



class Screen1(Screen):
    
    #add file button 
    btn1 = Button(text='add a file')
    def __init__(self, **kwargs):
        
        super(Screen1, self).__init__(**kwargs)
        self.add_widget(self.btn1)

class Screen2(Screen):
    #second screen which ask the path to save
    btn2 = Button(text='start')
    def __init__(self, **kwargs):

        super(Screen2, self).__init__(**kwargs)
        self.add_widget(self.btn2)

class Loading_screen(Screen):

    btn3 = Button(text='Run')

    def __init__(self, **kwargs):
        super(Loading_screen, self).__init__(**kwargs)
        self.add_widget(self.btn3)

      
class Screen3(Screen):
    #second screen which ask the path to save
    label = Label(text='loading...')
    def __init__(self, **kwargs):

        super(Screen3, self).__init__(**kwargs)
        self.add_widget(self.label)




class MyApp(App):

    

    filelist = []
    path = ''
    file_names = []

    thread1 = ThreadWithReturnValue()

    
    def build(self):
     
        Screen1.btn1.bind(on_release=self.ask_files)
        Screen2.btn2.bind(on_release=self.ask_path)
        
        Loading_screen.btn3.bind(on_release=self.begin)
        #Screen3.btn2.bind(on_release=self.pr)

        sm.add_widget(Screen1( name = 's1'))
        sm.add_widget(Screen2( name = 's2'))
        sm.add_widget(Loading_screen(name='loading'))
        sm.add_widget(Screen3(name='foo'))
        #sm.add_widget(Loading(name='l'))
        
        return sm

    def ask_files(self, obj):


        root = tk.Tk()
        root.withdraw()
        self.filelist = filedialog.askopenfilenames(
            title='Add files',
            initialdir='/sample_folder'
        )
        
       
        sm.current = 's2'
        print(self.filelist)
        

    def ask_path(self, obj):

   

        root = tk.Tk()
        root.withdraw()
        self.path = filedialog.askdirectory(
            title='Select path',
            initialdir='/test'
        )
        print(self.path)
        
        

        #file_names = thr1.join()

       
        sm.current = 'loading'

    def begin(self, obj):
        sm.current = 'foo'
        print(self.path)
        self.thread1 = ThreadWithReturnValue(target=run_program, args=(self.filelist, self.path))
        self.thread1.start()
        thread2= threading.Thread(target=self.pr, args=(obj,))
        thread2.start()




    def show_pos(self, p, *largs):
        create_plot(p)

    def pr(self, obj):
        while self.thread1.is_alive():
            Screen3.label.text="Loading"
            time.sleep(1)
        Screen3.label.text="Completed"

    
if __name__ == '__main__':
    MyApp().run()