import string
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# Import custom sound loader from mp3.py
from mp3 import play_sounds

# Warm sky-blue background color for the main app window
Window.clearcolor = (0.85, 0.95, 1.0, 1.0)


class KidButton(Button):
    """ Custom Button class with rounded corners and custom background colors """

    def __init__(self, bg_color, radius=20, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Make default Kivy button background invisible
        self.bg_color = bg_color
        self.radius = radius

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self.radius]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class Tujisomee(App):

    def build(self):
        self.letters = list(string.ascii_uppercase)

        # Child-friendly bright pastel palette (RGBA format)
        self.colors = [
            (0.35, 0.75, 0.98, 1),  # Sky Blue
            (1.00, 0.82, 0.30, 1),  # Warm Yellow
            (1.00, 0.50, 0.40, 1),  # Soft Coral
            (0.55, 0.85, 0.45, 1),  # Meadow Green
            (1.00, 0.65, 0.75, 1),  # Bubblegum Pink
            (1.00, 0.60, 0.25, 1),  # Sunny Orange
        ]

        # Main Layout (Vertical Container)
        self.main_layout = BoxLayout(
            orientation="vertical", spacing=10, padding=[20, 15, 20, 15]
        )

        # --- HEADER ---
        header_box = BoxLayout(
            orientation="vertical", size_hint_y=0.14, spacing=2
        )
        self.title_label = Label(
            text="Tujisomee Phonics 🎈",
            font_size=28,
            bold=True,
            color=(0.1, 0.3, 0.5, 1),
        )
        self.subtitle_label = Label(
            text="Tap any letter sound below to listen! 🔊",
            font_size=16,
            color=(0.3, 0.4, 0.6, 1),
        )
        header_box.add_widget(self.title_label)
        header_box.add_widget(self.subtitle_label)
        self.main_layout.add_widget(header_box)

        # --- VIEW MODE TOGGLE ---
        toggle_box = BoxLayout(
            orientation="horizontal", size_hint_y=0.08, spacing=15, padding=[40, 0]
        )
        self.grid_mode_btn = KidButton(
            bg_color=(0.2, 0.6, 0.85, 1),
            text="⣿ Grid View",
            font_size=16,
            bold=True,
            color=(1, 1, 1, 1),
            radius=12,
        )
        self.grid_mode_btn.bind(on_release=lambda x: self.switch_view("grid"))

        self.card_mode_btn = KidButton(
            bg_color=(0.7, 0.7, 0.8, 1),
            text="🎴 Card View",
            font_size=16,
            bold=True,
            color=(1, 1, 1, 1),
            radius=12,
        )
        self.card_mode_btn.bind(on_release=lambda x: self.switch_view("card"))

        toggle_box.add_widget(self.grid_mode_btn)
        toggle_box.add_widget(self.card_mode_btn)
        self.main_layout.add_widget(toggle_box)

        # --- MAIN CONTENT AREA ---
        self.content_area = BoxLayout(orientation="vertical", size_hint_y=0.78)
        self.main_layout.add_widget(self.content_area)

        # Set default view to Grid View before creating views
        self.current_view = "grid"

        # Pre-create Grid and Card views
        self.grid_view = self.create_grid_view()
        self.card_view = self.create_card_view()

        self.content_area.add_widget(self.grid_view)

        return self.main_layout

    def create_grid_view(self):
        """ Creates a responsive Grid View containing all A-Z sound buttons """
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        grid = GridLayout(
            cols=5, spacing=12, padding=[10, 10, 10, 10], size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter("height"))

        for i, letter in enumerate(self.letters):
            color_choice = self.colors[i % len(self.colors)]
            btn = KidButton(
                bg_color=color_choice,
                text=letter,
                font_size=36,
                bold=True,
                color=(1, 1, 1, 1),
                radius=18,
                size_hint_y=None,
                height=95,
            )
            btn.bind(on_release=lambda instance, l=letter: self.play_letter_sound(l))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        return scroll

    def create_card_view(self):
        """ Creates the Slideshow Carousel card view """
        card_layout = BoxLayout(orientation="vertical", spacing=10)

        self.carousel = Carousel(
            direction="right", loop=True, size_hint_y=0.85
        )
        self.carousel.bind(index=self.on_slide_change)

        for i, letter in enumerate(self.letters):
            color_choice = self.colors[i % len(self.colors)]
            card_box = BoxLayout(padding=[30, 10, 30, 10])

            btn = KidButton(
                bg_color=color_choice,
                text=letter,
                font_size=140,
                bold=True,
                color=(1, 1, 1, 1),
                radius=25,
            )
            btn.bind(on_release=lambda instance, l=letter: self.play_letter_sound(l))

            card_box.add_widget(btn)
            self.carousel.add_widget(card_box)

        card_layout.add_widget(self.carousel)

        nav_layout = BoxLayout(
            orientation="horizontal", spacing=20, size_hint_y=0.15
        )
        prev_btn = KidButton(
            bg_color=(0.3, 0.6, 0.9, 1),
            text="◀ Previous",
            font_size=18,
            bold=True,
            color=(1, 1, 1, 1),
            radius=15,
        )
        prev_btn.bind(on_release=lambda x: self.carousel.load_previous())

        next_btn = KidButton(
            bg_color=(0.3, 0.6, 0.9, 1),
            text="Next ▶",
            font_size=18,
            bold=True,
            color=(1, 1, 1, 1),
            radius=15,
        )
        next_btn.bind(on_release=lambda x: self.carousel.load_next())

        nav_layout.add_widget(prev_btn)
        nav_layout.add_widget(next_btn)
        card_layout.add_widget(nav_layout)

        return card_layout

    def switch_view(self, mode):
        """ Switches between Grid View and Card View """
        if mode == self.current_view:
            return

        self.content_area.clear_widgets()
        self.current_view = mode

        if mode == "grid":
            self.content_area.add_widget(self.grid_view)
            self.grid_mode_btn.bg_color = (0.2, 0.6, 0.85, 1)
            self.grid_mode_btn.update_rect(self.grid_mode_btn, None)
            self.card_mode_btn.bg_color = (0.7, 0.7, 0.8, 1)
            self.card_mode_btn.update_rect(self.card_mode_btn, None)
            self.subtitle_label.text = "Tap any letter sound below to listen! 🔊"
        else:
            self.content_area.add_widget(self.card_view)
            self.card_mode_btn.bg_color = (0.2, 0.6, 0.85, 1)
            self.card_mode_btn.update_rect(self.card_mode_btn, None)
            self.grid_mode_btn.bg_color = (0.7, 0.7, 0.8, 1)
            self.grid_mode_btn.update_rect(self.grid_mode_btn, None)
            self.subtitle_label.text = "Swipe or tap to hear the letter sound! 🔊"
            self.play_current_card_sound()

    def play_letter_sound(self, letter):
        """ Plays audio file corresponding to the selected letter """
        audio_path = f"./mp3/{letter.lower()}.mp3"
        play_sounds(audio_path)

    def play_current_card_sound(self, *args):
        """ Triggers audio for the currently active carousel card """
        current_slide_box = self.carousel.current_slide
        if current_slide_box:
            btn = current_slide_box.children[0]
            self.play_letter_sound(btn.text)

    def on_slide_change(self, carousel, index):
        """ Automatically plays sound when swiping slides in Card View """
        if getattr(self, "current_view", None) == "card":
            self.play_current_card_sound()


if __name__ == "__main__":
    Tujisomee().run()