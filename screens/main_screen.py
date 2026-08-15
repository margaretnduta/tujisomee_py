import string
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle

from ui.kid_button import KidButton
from utils.mp3 import play_sounds


class MainScreen(Screen):
    # App Primary Pink Palette Accent
    PINK_ACCENT = (0.88, 0.55, 0.72, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_card_index = 0
        self.letters = list(string.ascii_uppercase)
        
        # Kid-friendly soft pastel color palette
        self.colors = [
            (0.38, 0.72, 0.96, 1),  # Sky Blue
            (0.98, 0.76, 0.30, 1),  # Warm Sun Yellow
            (0.96, 0.48, 0.44, 1),  # Soft Coral Red
            (0.48, 0.82, 0.48, 1),  # Fresh Green
            (0.78, 0.52, 0.88, 1)   # Lavender Purple
        ]

    def on_enter(self):
        """Rebuilds UI dynamically whenever user enters or changes modes/languages."""
        self.clear_widgets()
        self.build_ui()

    def build_ui(self):
        app = App.get_running_app()
        mode = getattr(app, 'user_mode', 'grid')
        current_lang = getattr(app, 'current_language', 'en')
        
        # Base Screen Layout
        main_layout = BoxLayout(
            orientation="vertical", 
            spacing=12, 
            padding=[16, 12, 16, 12]
        )
        with main_layout.canvas.before:
            Color(0.98, 0.93, 0.96, 1.0)
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self._update_bg, size=self._update_bg)

        # 1. Top Header Bar
        header = BoxLayout(
            orientation="horizontal", 
            size_hint_y=None, 
            height=60, 
            spacing=10, 
            padding=[12, 6, 12, 6]
        )
        with header.canvas.before:
            Color(1, 1, 1, 0.95)
            header.bg_rect = RoundedRectangle(pos=header.pos, size=header.size, radius=[16])
        header.bind(pos=self._update_widget_bg, size=self._update_widget_bg)

        # Mascot Logo
        mascot = Image(source="assets/logo.png", fit_mode="contain", size_hint=(None, 1), width=40)
        header.add_widget(mascot)

        # App Title & Language Badge
        lang_code = "English" if current_lang == "en" else "Kiswahili"
        title = Label(
            text=f"[b]Tujisomee[/b]  •  [size=13sp][color=D85888]{lang_code}[/color][/size]",
            markup=True,
            font_size="17sp",
            color=(0.2, 0.2, 0.3, 1),
            halign="left",
            valign="middle"
        )
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)

        # Dynamic Language / Settings Button styled with Primary Theme Pink
        settings_text = "Lang" if current_lang == "en" else "Lugha"
        settings_btn = KidButton(
            bg_color=self.PINK_ACCENT,
            text=f" {settings_text}",
            font_size="12sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=12,
            size_hint=(None, 1),
            width=75
        )
        settings_btn.bind(on_release=self.go_to_settings)
        header.add_widget(settings_btn)

        main_layout.add_widget(header)

        # 2. Body View Container (Grid vs Card)
        body_container = BoxLayout(size_hint_y=1)
        if mode == 'grid':
            body_container.add_widget(self.build_grid_view())
        else:
            body_container.add_widget(self.build_card_view())

        main_layout.add_widget(body_container)
        self.add_widget(main_layout)

    # --- GRID VIEW BUILDER ---
    def build_grid_view(self):
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=4)
        grid = GridLayout(cols=4, spacing=10, padding=[2, 8, 2, 8], size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for i, letter in enumerate(self.letters):
            tile_btn = KidButton(
                bg_color=self.colors[i % len(self.colors)],
                text=f"{letter} {letter.lower()}",
                font_size="22sp",
                bold=True,
                radius=16,
                size_hint_y=None,
                height=90
            )
            tile_btn.bind(on_release=lambda inst, l=letter: self.play_letter_sound(inst, l))
            grid.add_widget(tile_btn)

        scroll.add_widget(grid)
        return scroll

    # --- CARD VIEW BUILDER ---
    def build_card_view(self):
        card_layout = BoxLayout(orientation="vertical", spacing=12, padding=[4, 4])

        current_letter = self.letters[self.current_card_index]
        card_color = self.colors[self.current_card_index % len(self.colors)]

        # Counter Badge
        counter_label = Label(
            text=f"[b]{self.current_card_index + 1}[/b] / {len(self.letters)}",
            markup=True,
            font_size="14sp",
            color=(0.5, 0.4, 0.5, 1),
            size_hint_y=None,
            height=20
        )
        card_layout.add_widget(counter_label)

        # Giant Flashcard
        self.card_btn = KidButton(
            bg_color=card_color,
            text=f"{current_letter}\n[size=48sp]{current_letter.lower()}[/size]",
            markup=True,
            font_size="72sp",
            bold=True,
            radius=28,
            size_hint=(1, 0.8)
        )
        self.card_btn.bind(on_release=lambda inst: self.play_letter_sound(inst, self.letters[self.current_card_index]))
        card_layout.add_widget(self.card_btn)

        # Navigation Controls (< Previous | Next >)
        nav_controls = BoxLayout(size_hint=(1, 0.16), spacing=15)
        
        prev_btn = KidButton(
            bg_color=(1, 1, 1, 0.95),
            text="<",
            font_size="26sp",
            bold=True,
            color=(0.4, 0.4, 0.5, 1),
            radius=18
        )
        prev_btn.bind(on_release=self.prev_card)

        next_btn = KidButton(
            bg_color=self.PINK_ACCENT,
            text=">",
            font_size="26sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=18
        )
        next_btn.bind(on_release=self.next_card)

        nav_controls.add_widget(prev_btn)
        nav_controls.add_widget(next_btn)
        card_layout.add_widget(nav_controls)

        return card_layout

    # --- CANVAS & ACTION HANDLERS ---
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

    def go_to_settings(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding'