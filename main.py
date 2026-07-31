import string
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
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

        # Main Vertical Layout
        self.main_layout = BoxLayout(
            orientation="vertical", spacing=10, padding=[20, 15, 20, 15]
        )

        # --- 1. HEADER WITH LANGUAGE TOGGLE ---
        header_box = BoxLayout(orientation="horizontal", size_hint_y=0.14, spacing=10)

        self.title_label = Label(
            text="Tujisomee Phonics 🎈",
            font_size=24,
            bold=True,
            color=(0.1, 0.3, 0.5, 1),
            size_hint_x=0.5,
            halign="left"
        )

        lang_box = BoxLayout(spacing=8, size_hint_x=0.5)
        self.btn_en = KidButton(
            bg_color=(0.2, 0.5, 0.8, 1),
            text="English 🇬🇧",
            font_size=12,
            bold=True,
            radius=10
        )
        self.btn_en.bind(on_release=lambda btn: self.switch_language("en", btn))

        self.btn_sw = KidButton(
            bg_color=(0.6, 0.6, 0.6, 0.6),
            text="Swahili 🇰🇪",
            font_size=12,
            bold=True,
            radius=10
        )
        self.btn_sw.bind(on_release=lambda btn: self.switch_language("sw", btn))

        lang_box.add_widget(self.btn_en)
        lang_box.add_widget(self.btn_sw)

        header_box.add_widget(self.title_label)
        header_box.add_widget(lang_box)
        self.main_layout.add_widget(header_box)

        # Subtitle
        self.subtitle_label = Label(
            text="Tap any letter sound below to listen! 🔊",
            font_size=14,
            color=(0.3, 0.4, 0.6, 1),
            size_hint_y=0.05
        )
        self.main_layout.add_widget(self.subtitle_label)

        # --- 2. VIEW MODE TOGGLE (GRID / CARD) ---
        toggle_box = BoxLayout(
            orientation="horizontal", size_hint_y=0.08, spacing=15, padding=[40, 0]
        )
        self.grid_mode_btn = KidButton(
            bg_color=(0.2, 0.6, 0.85, 1),
            text="⣿ Grid View",
            font_size=14,
            bold=True,
            radius=12,
        )
        self.grid_mode_btn.bind(on_release=lambda x: self.switch_view("grid"))

        self.card_mode_btn = KidButton(
            bg_color=(0.7, 0.7, 0.8, 1),
            text="🎴 Card View",
            font_size=14,
            bold=True,
            radius=12,
        )
        self.card_mode_btn.bind(on_release=lambda x: self.switch_view("card"))

        toggle_box.add_widget(self.grid_mode_btn)
        toggle_box.add_widget(self.card_mode_btn)
        self.main_layout.add_widget(toggle_box)

        # --- 3. MAIN CONTENT AREA ---
        self.content_area = BoxLayout(orientation="vertical", size_hint_y=0.73)
        self.main_layout.add_widget(self.content_area)

        self.current_view = "grid"
        self.grid_view = self.create_grid_view()
        self.card_view = self.create_card_view()
        self.content_area.add_widget(self.grid_view)

        return self.main_layout

    def create_grid_view(self):
        """ Creates Grid View containing all A-Z sound buttons """
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        grid = GridLayout(cols=5, spacing=12, padding=[10, 10, 10, 10], size_hint_y=None)
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
            btn.bind(on_release=lambda instance, l=letter: self.play_letter_sound(l, instance))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        return scroll

    def create_card_view(self):
        """ Creates Slideshow Carousel view """
        card_layout = BoxLayout(orientation="vertical", spacing=10)

        self.carousel = Carousel(direction="right", loop=True, size_hint_y=0.85)
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
            btn.bind(on_release=lambda instance, l=letter: self.play_letter_sound(l, instance))

            card_box.add_widget(btn)
            self.carousel.add_widget(card_box)

        card_layout.add_widget(self.carousel)

        nav_layout = BoxLayout(orientation="horizontal", spacing=20, size_hint_y=0.15)
        prev_btn = KidButton(
            bg_color=(0.3, 0.6, 0.9, 1),
            text="◀ Previous",
            font_size=16,
            bold=True,
            radius=15,
        )
        prev_btn.bind(on_release=lambda x: self.nav_previous(x))

        next_btn = KidButton(
            bg_color=(0.3, 0.6, 0.9, 1),
            text="Next ▶",
            font_size=16,
            bold=True,
            radius=15,
        )
        next_btn.bind(on_release=lambda x: self.nav_next(x))

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

    def switch_language(self, lang, button_instance):
        """ Margaret's Language Toggle Logic """
        button_instance.animate_bounce()

        if self.current_language == lang:
            return

        self.current_language = lang

        if lang == "en":
            self.btn_en.set_color((0.2, 0.5, 0.8, 1))
            self.btn_sw.set_color((0.6, 0.6, 0.6, 0.6))
        else:
            self.btn_sw.set_color((0.2, 0.5, 0.8, 1))
            self.btn_en.set_color((0.6, 0.6, 0.6, 0.6))

        if self.current_view == "card":
            self.play_current_card_sound()

    def play_letter_sound(self, letter, instance=None):
        """ Plays audio file in active language """
        if instance and hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        play_sounds(letter, lang=self.current_language)

    def nav_previous(self, instance):
        instance.animate_bounce()
        self.carousel.load_previous()

    def nav_next(self, instance):
        instance.animate_bounce()
        self.carousel.load_next()

    def play_current_card_sound(self, *args):
        """ Triggers audio for active carousel card """
        current_slide_box = self.carousel.current_slide
        if current_slide_box:
            btn = current_slide_box.children[0]
            play_sounds(btn.text, lang=self.current_language)

    def on_slide_change(self, carousel, index):
        if getattr(self, "current_view", None) == "card":
            self.play_current_card_sound()


if __name__ == "__main__":
    Tujisomee().run()