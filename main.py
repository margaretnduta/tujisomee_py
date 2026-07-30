import string
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# Import our custom sound player from mp3.py
from mp3 import play_sounds

# Set a warm, sky-blue background color for the app window
Window.clearcolor = (0.85, 0.95, 1.0, 1.0)


class KidButton(Button):
    """ Custom Button class with rounded corners and custom background colors """

    def __init__(self, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Make default Kivy button background invisible
        self.bg_color = bg_color

        with self.canvas.before:
            # Set the color for this specific button card
            Color(*self.bg_color)
            # Draw a rounded rectangle (radius=25 gives soft, kid-friendly corners)
            self.rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[25]
            )

        # Ensure the canvas shape resizes and moves dynamically when layout updates
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class Tujisomee(App):

    def build(self):
        self.letters = list(string.ascii_uppercase)
        self.current_language = "en"

        # Child-friendly bright pastel palette (RGBA format)
        self.colors = [
            (0.35, 0.75, 0.98, 1),  # Sky Blue
            (1.00, 0.82, 0.30, 1),  # Warm Yellow
            (1.00, 0.50, 0.40, 1),  # Soft Red / Coral
            (0.55, 0.85, 0.45, 1),  # Meadow Green
            (1.00, 0.65, 0.75, 1),  # Bubblegum Pink
            (1.00, 0.60, 0.25, 1),  # Sunny Orange
        ]

        # Main Layout (Vertical Container)
        main_layout = BoxLayout(
            orientation="vertical", spacing=15, padding=[25, 15, 25, 25]
        )

        # Header Title (Dark blue text for contrast against sky background)
        self.title_label = Label(
            text="Tujisomee Phonics",
            font_size=32,
            bold=True,
            color=(0.1, 0.3, 0.5, 1),
            size_hint_y=0.12,
        )
        main_layout.add_widget(self.title_label)

        # --- CAROUSEL (SLIDESHOW) ---
        self.carousel = Carousel(
            direction="right", loop=True, size_hint_y=0.73
        )
        self.carousel.bind(index=self.on_slide_change)

        # Build each big colorful card for A to Z
        for i, letter in enumerate(self.letters):
            color_choice = self.colors[i % len(self.colors)]

            # Card container with padding around the giant button
            card_box = BoxLayout(padding=[30, 10, 30, 10])

            btn = KidButton(
                bg_color=color_choice,
                text=letter,
                font_size=150,  # Extra large text for young readers
                bold=True,
                color=(1, 1, 1, 1),  # Crisp white letter text
            )

            # Re-play sound on tap
            btn.bind(on_release=self.play_current_sound)

            card_box.add_widget(btn)
            self.carousel.add_widget(card_box)

        main_layout.add_widget(self.carousel)

        # --- NAVIGATION BUTTONS ---
        nav_layout = BoxLayout(
            orientation="horizontal", spacing=20, size_hint_y=0.15
        )

        self.prev_btn = KidButton(
            bg_color=(0.3, 0.6, 0.9, 1),
            text="◀ Previous",
            font_size=22,
            bold=True,
            color=(1, 1, 1, 1),
        )
        self.prev_btn.bind(on_release=lambda x: self.carousel.load_previous())

        self.next_btn = KidButton(
            bg_color=(0.3, 0.6, 0.9, 1),
            text="Next ▶",
            font_size=22,
            bold=True,
            color=(1, 1, 1, 1),
        )
        self.next_btn.bind(on_release=lambda x: self.carousel.load_next())

        nav_layout.add_widget(self.prev_btn)
        nav_layout.add_widget(self.next_btn)

        main_layout.add_widget(nav_layout)

        # Play 'A' sound on app launch
        self.play_current_sound()

        return main_layout

    def play_current_sound(self, *args):
        """Finds the active slide and triggers audio playback"""
        current_slide_box = self.carousel.current_slide
        if current_slide_box:
            # Extract the inner KidButton from the padding container
            btn = current_slide_box.children[0]
            letter = btn.text.lower()
            audio_path = f"./mp3/{letter}.mp3"
            play_sounds(audio_path)

    def on_slide_change(self, carousel, index):
        """Automatically plays sound when swiped or navigated"""
        self.play_current_sound()


if __name__ == "__main__":
    Tujisomee().run()