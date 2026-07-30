import string
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.carousel import Carousel
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.animation import Animation

# Import custom sound module
from mp3 import play_sounds

# Soft pastel background
Window.clearcolor = (0.88, 0.94, 0.98, 1.0)


class KidButton(Button):
    """ Custom Button class with rounded corners, custom color, and click animations """

    def __init__(self, bg_color, radius=25, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Hide default Kivy button background
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

    def animate_bounce(self):
        """ Feature 1: Bouncing visual animation on tap """
        # Shrink slightly then pop back to original size with an elastic bounce
        orig_size = (self.size_hint_x, self.size_hint_y)
        
        # Scale down
        anim = Animation(size_hint=(orig_size[0] * 0.95, orig_size[1] * 0.95), duration=0.08)
        # Bounce back
        anim += Animation(size_hint=orig_size, duration=0.15, t='out_bounce')
        anim.start(self)


class Tujisomee(App):

    def build(self):
        self.letters = list(string.ascii_uppercase)
        self.current_language = "en"

        # Vibrant pastel color collection
        self.colors = [
            (0.35, 0.75, 0.98, 1),  # Sky Blue
            (1.00, 0.82, 0.30, 1),  # Warm Yellow
            (1.00, 0.50, 0.40, 1),  # Soft Coral
            (0.55, 0.85, 0.45, 1),  # Meadow Green
            (1.00, 0.65, 0.75, 1),  # Pink
            (1.00, 0.60, 0.25, 1),  # Orange
        ]

        # Use FloatLayout so side arrows can overlay cleanly on top of the card view
        root_layout = FloatLayout()

        # Vertical layout for Header + Slideshow Carousel
        content_box = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=[40, 20, 40, 20],
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # Header Title
        self.title_label = Label(
            text="Tujisomee Phonics",
            font_size=34,
            bold=True,
            color=(0.12, 0.3, 0.5, 1),
            size_hint_y=0.15
        )
        content_box.add_widget(self.title_label)

        # --- SLIDESHOW CAROUSEL ---
        self.carousel = Carousel(
            direction="right", loop=True, size_hint_y=0.85
        )
        self.carousel.bind(index=self.on_slide_change)

        # Build colorful letter cards
        for i, letter in enumerate(self.letters):
            color_choice = self.colors[i % len(self.colors)]
            
            # Card wrapper
            card_box = BoxLayout(padding=[35, 10, 35, 10])

            btn = KidButton(
                bg_color=color_choice,
                text=letter,
                font_size=160,
                bold=True,
                color=(1, 1, 1, 1),
                radius=35
            )
            btn.bind(on_release=self.on_card_tap)

            card_box.add_widget(btn)
            self.carousel.add_widget(card_box)

        content_box.add_widget(self.carousel)
        root_layout.add_widget(content_box)

        # --- MODERN SIDE NAVIGATION BUTTONS (Floating Controls) ---
        # Previous (Left Side)
        self.prev_btn = KidButton(
            bg_color=(0.2, 0.4, 0.7, 0.75),  # Semi-transparent sleek dark blue
            text="<",
            font_size=32,
            bold=True,
            color=(1, 1, 1, 1),
            radius=20,
            size_hint=(0.08, 0.18),
            pos_hint={"x": 0.02, "center_y": 0.5}
        )
        self.prev_btn.bind(on_release=self.nav_previous)

        # Next (Right Side)
        self.next_btn = KidButton(
            bg_color=(0.2, 0.4, 0.7, 0.75),
            text=">",
            font_size=32,
            bold=True,
            color=(1, 1, 1, 1),
            radius=20,
            size_hint=(0.08, 0.18),
            pos_hint={"right": 0.98, "center_y": 0.5}
        )
        self.next_btn.bind(on_release=self.nav_next)

        root_layout.add_widget(self.prev_btn)
        root_layout.add_widget(self.next_btn)

        # Play 'A' sound on initial app open
        self.play_current_sound()

        return root_layout

    def on_card_tap(self, instance):
        """ Trigger bounce animation and play audio when the giant letter card is clicked """
        instance.animate_bounce()
        self.play_current_sound()

    def nav_previous(self, instance):
        """ Animate left button and load previous slide """
        instance.animate_bounce()
        self.carousel.load_previous()

    def nav_next(self, instance):
        """ Animate right button and load next slide """
        instance.animate_bounce()
        self.carousel.load_next()

    def play_current_sound(self, *args):
        """ Extract current slide letter and play MP3 """
        current_slide_box = self.carousel.current_slide
        if current_slide_box:
            btn = current_slide_box.children[0]
            letter = btn.text.lower()
            audio_path = f"./mp3/{letter}.mp3"
            play_sounds(audio_path)

    def on_slide_change(self, carousel, index):
        """ Auto-play sound when slide changes """
        self.play_current_sound()


if __name__ == "__main__":
    Tujisomee().run()