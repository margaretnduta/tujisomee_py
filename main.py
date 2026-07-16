from kivy.app import App # Tells Kivy to run the main App class
from kivy.uix.label import Label # Kivy Label Class
from kivy.uix.button import Button # Kivy Button Class
from kivy.uix.boxlayout import BoxLayout# Kivy BoxLayout class
# from playsound import playsound # Plays MP3 files
from mp3 import play_sounds 

class Tujisomee(App):

    # add_widget is a native kivy method
    # button_click_audio is user made method from func button_click_audio()
    # self allows to access other things in the app like self.label within the main App class.

    def build(self):
        self.count = 0 # initialize count

        # This are static text that never change when the program is being interpreted 
        self.title_label_1 = Label(text="Hello, User!")
        self.title_label_2 = Label(text="This is a simple Kivy program which is a Python Module")
    
        self.label = Label(text="0") # Dynamic text which changes from button_count()
        self.button_a = Button(text="Play Sound A")
        self.button_b = Button(text="Play Sound B")
        # on_press is a built in event in Kivy
        # bind() native Kivy method

        self.button_a.bind(on_press=self.button_click_audio_a)
        self.button_a.bind(on_press=self.button_count)
        self.button_b.bind(on_press=self.button_click_audio_b)
        self.button_b.bind(on_press=self.button_count)

        # rendering of elements on the screen     
        layout = BoxLayout(orientation = "vertical",
                           spacing = 10,
                           padding = 20
        )

        layout.add_widget(self.title_label_1)
        layout.add_widget(self.title_label_2)
        layout.add_widget(self.label)
        layout.add_widget(self.button_a)
        layout.add_widget(self.button_b)

        return layout

    def button_click_audio_a(self, instance):
        play_sounds("./mp3/a.mp3")

    def button_click_audio_b(self, instance):
        play_sounds("./mp3/b.mp3")

    def button_count(self, instance):
        
        self.count = self.count + 1
        self.label.text = f"Clicks: {self.count}" # This changes value of self count to be displayed by self.label.text object.

if __name__ == "__main__":
    Tujisomee().run()

"""
KIVY BOILERPLATE CODE

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.label = Label(text="Welcome!")
        self.add_widget(self.label)

        self.button = Button(text="Click Me")
        self.button.bind(on_press=self.on_button_click)
        self.add_widget(self.button)

    def on_button_click(self, instance):
        self.label.text = "Button Clicked!"

class MyApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    MyApp().run()
"""
