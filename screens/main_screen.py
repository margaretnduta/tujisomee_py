import string
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle

from ui.kid_button import KidButton
from utils.mp3 import play_sounds


class MainScreen(Screen):
    PINK_ACCENT = (0.88, 0.55, 0.72, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_card_index = 0
        self.letters = list(string.ascii_uppercase)
        
        self.colors = [
            (0.38, 0.72, 0.96, 1),
            (0.98, 0.76, 0.30, 1),
            (0.96, 0.48, 0.44, 1),
            (0.48, 0.82, 0.48, 1),
            (0.78, 0.52, 0.88, 1)
        ]

    def on_enter(self):
        self.clear_widgets()
        self.build_ui()

    def build_ui(self):
        app = App.get_running_app()
        mode = getattr(app, 'user_mode', 'grid')
        current_lang = getattr(app, 'current_language', 'en')
        stars = getattr(app, 'stars', 0)
        
        main_layout = BoxLayout(
            orientation="vertical", 
            spacing=10, 
            padding=[16, 10, 16, 10]
        )
        with main_layout.canvas.before:
            Color(0.98, 0.93, 0.96, 1.0)
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self._update_bg, size=self._update_bg)

        # 1. Header Bar with Star Badge
        header = BoxLayout(
            orientation="horizontal", 
            size_hint_y=None, 
            height=56, 
            spacing=6, 
            padding=[10, 6, 10, 6]
        )
        with header.canvas.before:
            Color(1, 1, 1, 0.95)
            header.bg_rect = RoundedRectangle(pos=header.pos, size=header.size, radius=[16])
        header.bind(pos=self._update_widget_bg, size=self._update_widget_bg)

        mascot = Image(source="assets/logo.png", fit_mode="contain", size_hint=(None, 1), width=32)
        header.add_widget(mascot)

        # Star Counter
        star_badge = Label(
            text=f"[b]{stars}[/b]",
            markup=True,
            font_size="14sp",
            color=(0.9, 0.6, 0.1, 1),
            size_hint=(None, 1),
            width=50
        )
        header.add_widget(star_badge)

        # Language Selector Dropdown
        lang_spinner = Spinner(
            text="English " if current_lang == "en" else "Kiswahili ",
            values=("English ", "Kiswahili "),
            size_hint=(None, 1),
            width=105,
            background_normal='',
            background_color=self.PINK_ACCENT,
            color=(1, 1, 1, 1),
            font_size="11sp",
            bold=True
        )
        lang_spinner.bind(text=self.on_language_change)
        header.add_widget(lang_spinner)

        main_layout.add_widget(header)

        # 2. Body View Container
        body_container = BoxLayout(size_hint_y=0.82)
        if mode == 'grid':
            body_container.add_widget(self.build_grid_view())
        else:
            body_container.add_widget(self.build_card_view())
        main_layout.add_widget(body_container)

        # 3. Footer Navigation Bar (Quiz + Home Actions)
        footer_nav = BoxLayout(
            orientation="horizontal", 
            size_hint_y=None, 
            height=54, 
            spacing=10,
            padding=[8, 4, 8, 4]
        )
        with footer_nav.canvas.before:
            Color(1, 1, 1, 0.95)
            footer_nav.bg_rect = RoundedRectangle(pos=footer_nav.pos, size=footer_nav.size, radius=[18])
        footer_nav.bind(pos=self._update_widget_bg, size=self._update_widget_bg)

        quiz_btn = KidButton(
            bg_color=(0.48, 0.82, 0.48, 1),
            text=" Quiz" if current_lang == "en" else " Mchezo",
            font_size="13sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=14,
            size_hint=(0.5, 1)
        )
        quiz_btn.bind(on_release=self.go_to_quiz)

        home_btn = KidButton(
            bg_color=self.PINK_ACCENT,
            text="Home" if current_lang == "en" else "Mwanzo",
            font_size="13sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=14,
            size_hint=(0.5, 1)
        )
        home_btn.bind(on_release=self.go_to_onboarding)

        footer_nav.add_widget(quiz_btn)
        footer_nav.add_widget(home_btn)

        main_layout.add_widget(footer_nav)
        self.add_widget(main_layout)

    def on_language_change(self, spinner, text):
        new_lang = "en" if "English" in text else "sw"
        app = App.get_running_app()
        if app.current_language != new_lang:
            app.update_language(new_lang)
            self.on_enter()

    def build_grid_view(self):
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=4)
        grid = GridLayout(cols=4, spacing=10, padding=[2, 6, 2, 6], size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for i, letter in enumerate(self.letters):
            tile_btn = KidButton(
                bg_color=self.colors[i % len(self.colors)],
                text=f"{letter} {letter.lower()}",
                font_size="22sp",
                bold=True,
                radius=16,
                size_hint_y=None,
                height=85
            )
            tile_btn.bind(on_release=lambda inst, l=letter: self.play_letter_sound(inst, l))
            grid.add_widget(tile_btn)

        scroll.add_widget(grid)
        return scroll

    def build_card_view(self):
        card_layout = BoxLayout(orientation="vertical", spacing=10, padding=[2, 2])

        current_letter = self.letters[self.current_card_index]
        card_color = self.colors[self.current_card_index % len(self.colors)]

        counter_label = Label(
            text=f"[b]{self.current_card_index + 1}[/b] / {len(self.letters)}",
            markup=True,
            font_size="13sp",
            color=(0.5, 0.4, 0.5, 1),
            size_hint_y=None,
            height=18
        )
        card_layout.add_widget(counter_label)

        self.card_btn = KidButton(
            bg_color=card_color,
            text=f"{current_letter}\n[size=44sp]{current_letter.lower()}[/size]",
            markup=True,
            font_size="68sp",
            bold=True,
            radius=26,
            size_hint=(1, 0.78)
        )
        self.card_btn.bind(on_release=lambda inst: self.play_letter_sound(inst, self.letters[self.current_card_index]))
        card_layout.add_widget(self.card_btn)

        nav_controls = BoxLayout(size_hint=(1, 0.18), spacing=15)
        
        prev_btn = KidButton(
            bg_color=(1, 1, 1, 0.95),
            text="<",
            font_size="24sp",
            bold=True,
            color=(0.4, 0.4, 0.5, 1),
            radius=16
        )
        prev_btn.bind(on_release=self.prev_card)

        next_btn = KidButton(
            bg_color=self.PINK_ACCENT,
            text=">",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=16
        )
        next_btn.bind(on_release=self.next_card)

        nav_controls.add_widget(prev_btn)
        nav_controls.add_widget(next_btn)
        card_layout.add_widget(nav_controls)

        return card_layout

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _update_widget_bg(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    def play_letter_sound(self, instance, letter):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        app = App.get_running_app()
        play_sounds(letter, lang=getattr(app, 'current_language', 'en'))

    def next_card(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        self.current_card_index = (self.current_card_index + 1) % len(self.letters)
        self.on_enter()
        app = App.get_running_app()
        play_sounds(self.letters[self.current_card_index], lang=getattr(app, 'current_language', 'en'))

    def prev_card(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        self.current_card_index = (self.current_card_index - 1) % len(self.letters)
        self.on_enter()
        app = App.get_running_app()
        play_sounds(self.letters[self.current_card_index], lang=getattr(app, 'current_language', 'en'))

    def go_to_quiz(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        self.manager.transition.direction = 'left'
        self.manager.current = 'quiz'

    def go_to_onboarding(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding'