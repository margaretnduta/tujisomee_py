import string
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# Import our custom sound player from mp3.py
from mp3 import play_sounds

class Tujisomee(App):

    def build(self):
        # Tracking application state
        self.count = 0
        self.current_language = "en"  # Ready to scale to 'es', 'sw', etc.

        # --- MAIN CONTAINER ---
        # Stacks header and grid vertically
        main_layout = BoxLayout(
            orientation="vertical", 
            spacing=10, 
            padding=20
        )

        # --- HEADER SECTION ---
        self.title_label = Label(
            text="Tujisomee Phonics!", 
            font_size=24, 
            size_hint_y=0.15
        )
        self.count_label = Label(
            text="Clicks: 0", 
            font_size=18, 
            size_hint_y=0.1
        )
        
        main_layout.add_widget(self.title_label)
        main_layout.add_widget(self.count_label)

        # --- ALPHABET GRID SECTION ---
        # 5-column grid layout for A-Z buttons
        grid_layout = GridLayout(
            cols=5, 
            spacing=10, 
            size_hint_y=0.75
        )

        # Loop dynamically through all uppercase letters (A-Z)
        for letter in string.ascii_uppercase:
            btn = Button(
                text=letter,
                font_size=28,
                bold=True
            )
            # Bind the release event of each button to our central click handler
            btn.bind(on_release=self.on_letter_click)
            grid_layout.add_widget(btn)

        main_layout.add_widget(grid_layout)
        return main_layout

    def on_letter_click(self, instance):
        """
        Triggered whenever any letter button in the grid is clicked.
        'instance' refers to the specific Button object that was pressed.
        """
        # 1. Increment total click count and update UI label
        self.count += 1
        self.count_label.text = f"Clicks: {self.count}"

        # 2. Extract letter from button text and convert to lowercase ('A' -> 'a')
        letter = instance.text.lower()
        
        # 3. Construct file path dynamically based on language and letter
        audio_path = f"./mp3/{letter}.mp3"
        
        # 4. Trigger audio playback using our custom play_sounds function
        play_sounds(audio_path)


if __name__ == "__main__":
    # Launch the Kivy Application
    Tujisomee().run()