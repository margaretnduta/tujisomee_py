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

# Import Margaret's updated multi-language sound function
from mp3 import play_sounds

Window.clearcolor = (0.88, 0.94, 0.98, 1.0)


class KidButton(Button):
    """ Custom Button with rounded corners and tap-bounce animations """

    def __init__(self, bg_color, radius=25, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.radius = radius

        with self.canvas.before:
            self.color_instruction = Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self.radius]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_color(self, new_color):
        """ Dynamically change button background color """
        self.bg_color = new_color
        self.color_instruction.rgba = new_color

    def animate_bounce(self):
        """ Bounce FX animation on tap """
        orig_size = (self.size_hint_x, self.size_hint_y)
        anim = Animation(size_hint=(orig_size[0] * 0.92, orig_size[1] * 0.92), duration=0.06)
        anim += Animation(size_hint=orig_size, duration=0.12, t='out_bounce')
        anim.start(self)


class Tujisomee(App):

    def build(self):
        self.letters = list(string.ascii_uppercase)
        self.current_language = "en"  # Default language is English ('en' or 'sw')

        # Colors for A-Z cards
        self.colors = [
            (0.35, 0.75, 0.98, 1),  # Sky Blue
            (1.00, 0.82, 0.30, 1),  # Warm Yellow
            (1.00, 0.50, 0.40, 1),  # Coral Red
            (0.55, 0.85, 0.45, 1),  # Meadow Green
            (1.00, 0.65, 0.75, 1),  # Pink
            (1.00, 0.60, 0.25, 1),  # Orange
        ]

        # Root layout for overlaying floating controls
        root_layout = FloatLayout()

        # Main Vertical Container
        content_box = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=[60, 15, 60, 20],
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # --- 1. TOP BAR: TITLE + LANGUAGE TOGGLE ---
        top_bar = BoxLayout(orientation="horizontal", size_hint_y=0.15, spacing=10)

        # Title Label
        self.title_label = Label(
            text="Tujisomee Phonics",
            font_size=30,
            bold=True,
            color=(0.12, 0.3, 0.5, 1),
            size_hint_x=0.6,
            halign="left"
        )

        # Language Toggle Container
        lang_box = BoxLayout(spacing=8, size_hint_x=0.4)

        self.btn_en = KidButton(
            bg_color=(0.2, 0.5, 0.8, 1),
            text="English",
            font_size=12,
            bold=True,
            radius=10
        )
        self.btn_en.bind(on_release=lambda btn: self.switch_language("en", btn))

        self.btn_sw = KidButton(
            bg_color=(0.6, 0.6, 0.6, 0.6),  # Muted color when inactive
            text="Swahili",
            font_size=12,
            bold=True,
            radius=10
        )
        self.btn_sw.bind(on_release=lambda btn: self.switch_language("sw", btn))

        lang_box.add_widget(self.btn_en)
        lang_box.add_widget(self.btn_sw)

        top_bar.add_widget(self.title_label)
        top_bar.add_widget(lang_box)
        content_box.add_widget(top_bar)

        # --- 2. CAROUSEL SLIDESHOW ---
        self.carousel = Carousel(direction="right", loop=True, size_hint_y=0.85)
        self.carousel.bind(index=self.on_slide_change)

        for i, letter in enumerate(self.letters):
            color_choice = self.colors[i % len(self.colors)]
            card_box = BoxLayout(padding=[50, 10, 50, 10])

            btn = KidButton(
                bg_color=color_choice,
                text=letter,
                font_size=150,
                bold=True,
                color=(1, 1, 1, 1),
                radius=35
            )
            btn.bind(on_release=self.on_card_tap)

            card_box.add_widget(btn)
            self.carousel.add_widget(card_box)

        content_box.add_widget(self.carousel)
        root_layout.add_widget(content_box)

        # --- 3. SIDE NAVIGATION CONTROLS WITH BOUNCE FX ---
        self.prev_btn = KidButton(
            bg_color=(0.2, 0.4, 0.7, 0.8),
            text="<",
            font_size=32,
            bold=True,
            color=(1, 1, 1, 1),
            radius=20,
            size_hint=(0.08, 0.16),
            pos_hint={"x": 0.02, "center_y": 0.5}
        )
        self.prev_btn.bind(on_release=self.nav_previous)

        self.next_btn = KidButton(
            bg_color=(0.2, 0.4, 0.7, 0.8),
            text=">",
            font_size=32,
            bold=True,
            color=(1, 1, 1, 1),
            radius=20,
            size_hint=(0.08, 0.16),
            pos_hint={"right": 0.98, "center_y": 0.5}
        )
        self.next_btn.bind(on_release=self.nav_next)

        root_layout.add_widget(self.prev_btn)
        root_layout.add_widget(self.next_btn)

        # Play initial sound on startup
        self.play_current_sound()

        return root_layout

    # --- LOGIC & EVENT HANDLERS ---

    def switch_language(self, lang, button_instance):
        """ Margaret's Language Toggle Logic """
        button_instance.animate_bounce()
        
        if self.current_language == lang:
            return  # Already active

        self.current_language = lang

        # Update button highlighting (Active = Blue, Inactive = Muted Grey)
        if lang == "en":
            self.btn_en.set_color((0.2, 0.5, 0.8, 1))
            self.btn_sw.set_color((0.6, 0.6, 0.6, 0.6))
        else:
            self.btn_sw.set_color((0.2, 0.5, 0.8, 1))
            self.btn_en.set_color((0.6, 0.6, 0.6, 0.6))

        # Re-play active letter in the newly selected language!
        self.play_current_sound()

    def on_card_tap(self, instance):
        instance.animate_bounce()
        self.play_current_sound()

    def nav_previous(self, instance):
        instance.animate_bounce()
        self.carousel.load_previous()

    def nav_next(self, instance):
        instance.animate_bounce()
        self.carousel.load_next()

    def play_current_sound(self, *args):
        """ Plays sound using selected language """
        current_slide_box = self.carousel.current_slide
        if current_slide_box:
            btn = current_slide_box.children[0]
            letter = btn.text.lower()
            play_sounds(letter, lang=self.current_language)

    def on_slide_change(self, carousel, index):
        self.play_current_sound()


if __name__ == "__main__":
    Tujisomee().run()