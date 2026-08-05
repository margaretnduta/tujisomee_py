import string
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window

from ui.kid_button import KidButton
from utils.mp3 import play_sounds


class MainScreen(Screen):
    def on_enter(self):
        """ Runs every time this screen opens to dynamically build the grid based on selected language. """
        self.clear_widgets()
        self.build_ui()

    def build_ui(self):
        app = App.get_running_app()
        self.letters = list(string.ascii_uppercase)
        
        # Color scheme palette for the letter buttons
        self.colors = [
            (0.35, 0.75, 0.98, 1),  # Soft Blue
            (1.00, 0.82, 0.30, 1),  # Warm Yellow
            (1.00, 0.50, 0.40, 1),  # Coral Red
            (0.55, 0.85, 0.45, 1)   # Apple Green
        ]

        main_layout = BoxLayout(
            orientation="vertical", 
            spacing=10, 
            padding=[15, 15, 15, 15]
        )

        # 1. Top Bar / Header
        header = BoxLayout(orientation="horizontal", size_hint_y=0.12)
        
        lang_title = "English" if app.current_language == "en" else "Kiswahili"
        title = Label(
            text=f"Tujisomee Phonics ({lang_title}) 🎈",
            font_size="20sp",
            bold=True,
            color=(0.1, 0.3, 0.5, 1)
        )

        back_btn = KidButton(
            bg_color=(0.7, 0.7, 0.8, 1),
            text="⚙️ Lang",
            font_size="12sp",
            radius=12,
            size_hint=(0.25, 0.8)
        )
        back_btn.bind(on_release=self.go_back)

        header.add_widget(title)
        header.add_widget(back_btn)
        main_layout.add_widget(header)

        # 2. Phonics Letter Grid View
        scroll = ScrollView(size_hint=(1, 0.88), do_scroll_x=False)
        grid = GridLayout(cols=4, spacing=12, padding=[5, 5], size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for i, letter in enumerate(self.letters):
            btn = KidButton(
                bg_color=self.colors[i % len(self.colors)],
                text=letter,
                font_size="28sp",
                bold=True,
                radius=18,
                size_hint_y=None,
                height=80
            )
            # Bind audio playback passing letter and language state
            btn.bind(on_release=lambda inst, l=letter: self.play_letter_sound(inst, l))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def play_letter_sound(self, instance, letter):
        instance.animate_bounce()
        app = App.get_running_app()
        play_sounds(letter, lang=app.current_language)

    def go_back(self, instance):
        instance.animate_bounce()
        self.manager.current = "onboarding"