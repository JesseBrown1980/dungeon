#!/usr/bin/env python3
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from generator import DungeonGenerator
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.logger import Logger
from enum import Enum

class State(Enum):
    PAUSED=0
    ANIMATING=1
    DONE=5
    

class DungeonApp(App):
    '''
    '''
    generator = ObjectProperty(None)

    def reset(self, arg):
        self.state = State.ANIMATING
        n_rooms = 0
        minSize = 0
        maxSize = 0
        try:
            n_rooms = int(self.field1.text)
            minSize=int(self.field2.text)
            maxSize=int(self.field3.text)
        except Exception as e:
            print(e)
        self.generator.generate_rooms(n_rooms = n_rooms, minSize=minSize, maxSize=maxSize)
        

    def identify(self, arg):
        if self.state != State.ANIMATING:
            self.generator.identify_rooms()
            self.generator.center_rooms()
            
    def cull_rooms(self, arg):
        if self.state != State.ANIMATING:
            self.generator.identify_rooms(clear=True)
            self.generator.center_rooms()
        
    def hallways(self, arg):
        if self.state != State.ANIMATING:
            self.generator.build_hallways()
        
    def build(self):
        Window.size = (1024, 1024)
        
        self.state = State.PAUSED
        self.generator = DungeonGenerator(size=Window.size,
                                          size_hint=(.9,1))
        self.buttons = BoxLayout(orientation='horizontal', size_hint=(1,.1))

        self.btn0 = Button(text='Start', on_press=self.reset)
        self.btn1 = Button(text='Identify', on_press=self.identify)
        self.btn2 = Button(text='Cull', on_press=self.cull_rooms)
        self.btn3 = Button(text='Build Hallways', on_press=self.hallways)

        for btn in [self.btn0, self.btn1, self.btn2, self.btn3]:
            self.buttons.add_widget(btn)
        #input number of rooms
        self.input_box1 = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        self.label1 = Label(text='Number of rooms:',  size_hint_y=None, height=30, width=100)
        self.field1 = TextInput(multiline=False, size_hint_y=None, height=50,  text="40",size_hint_x=None,width=200)
        self.input_box1.add_widget(self.label1)
        self.input_box1.add_widget(self.field1)
        #min/max size of room
        self.label2 = Label(text='min size of room:',  size_hint_y=None, height=30, width=50)
        self.field2 = TextInput(multiline=False, size_hint_y=None, height=50 ,size_hint_x=None,width=100 ,text="2")
        self.label3 = Label(text='max size of room:',  size_hint_y=None, height=30, width=50)
        self.field3 = TextInput(multiline=False, size_hint_y=None, height=50 ,size_hint_x=None,width=100, text="10")
        self.input_box1.add_widget(self.label2)
        self.input_box1.add_widget(self.field2)
        self.input_box1.add_widget(self.label3)
        self.input_box1.add_widget(self.field3)
        #set widget
        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.generator)
        self.root.add_widget(self.input_box1)
        self.root.add_widget(self.buttons)
            
        Clock.schedule_interval(self.update, 1/60.)
        
        return self.root

    
    def update(self, dt):
        '''
        '''

        for btn in [self.btn1, self.btn2, self.btn3]:
            btn.disabled = self.state is State.ANIMATING

        if self.state is State.PAUSED:
            return

        if self.state is State.ANIMATING:
            result = self.generator.spread_out_rooms(dt)
            if result:
                self.state = State.PAUSED
                self.generator.center_rooms()
            return


if __name__ == "__main__":
    
    DungeonApp().run()
