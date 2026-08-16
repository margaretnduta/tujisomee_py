import random
import string
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle

from ui.kid_button import KidButton
from utils.mp3 import play_sounds


class QuizScreen(Screen):
    PINK_ACCENT = (0.88, 0.55, 0.72, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.letters = list(string.ascii_uppercase)
        self.target_letter = "A"
        self.options = []
        
        self.colors = [
            (0.38, 0.72, 0.96, 1),  # Blue
            (0.98, 0.76, 0.30, 1),  # Yellow
            (0.96, 0.48, 0.44, 1),  # Coral Red
            (0.48, 0.82, 0.48, 1)   # Green
        ]

    def on_enter(self):
        self.next_question()

    def generate_options(self):
        """Pick 1 target letter and 3 random distractors."""
        self.target_letter = random.choice(self.letters)
        wrong_letters = [l for l in self.letters if l != self.target_letter]
        self.options = random.sample(wrong_letters, 3) + [self.target_letter]
        random.shuffle(self.options)

    def next_question(self, *args):
        self.generate_options()
        self.clear_widgets()
        self.build_ui()
        
        # Play target letter audio automatically on question start
        app = App.get_running_app()
        play_sounds(self.target_letter, lang=getattr(app, 'current_language', 'en'))

    def build_ui(self):
        app = App.get_running_app()
        current_lang = getattr(app, 'current_language', 'en')
        stars = getattr(app, 'stars', 0)

        main_layout = BoxLayout(
            orientation="vertical", 
            spacing=12, 
            padding=[16, 10, 16, 10]
        )
        with main_layout.canvas.before:
            Color(0.98, 0.93, 0.96, 1.0)
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self._update_bg, size=self._update_bg)

        # 1. Header Bar with Star Counter
        header = BoxLayout(
            orientation="horizontal", 
            size_hint_y=None, 
            height=56, 
            spacing=8, 
            padding=[10, 6, 10, 6]
        )
        with header.canvas.before:
            Color(1, 1, 1, 0.95)
            header.bg_rect = RoundedRectangle(pos=header.pos, size=header.size, radius=[16])
        header.bind(pos=self._update_widget_bg, size=self._update_widget_bg)

        mascot = Image(source="assets/logo.png", fit_mode="contain", size_hint=(None, 1), width=36)
        header.add_widget(mascot)

        title_text = "Mchezo wa Herufi" if current_lang == "sw" else "Find the Letter"
        title = Label(
            text=f"[b]{title_text}[/b]",
            markup=True,
            font_size="16sp",
            color=(0.2, 0.2, 0.3, 1),
            halign="left",
            valign="middle"
        )
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)

        # Star Counter Badge
        star_badge = Label(
            text=f"[b]{stars}[/b]",
            markup=True,
            font_size="16sp",
            color=(0.9, 0.6, 0.1, 1),
            size_hint=(None, 1),
            width=65
        )
        header.add_widget(star_badge)

        main_layout.add_widget(header)

        # 2. Audio Replay Prompt
        prompt_card = BoxLayout(orientation="vertical", size_hint_y=0.35, spacing=6, padding=[10, 10])
        with prompt_card.canvas.before:
            Color(1, 1, 1, 0.8)
            prompt_card.bg_rect = RoundedRectangle(pos=prompt_card.pos, size=prompt_card.size, radius=[20])
        prompt_card.bind(pos=self._update_widget_bg, size=self._update_widget_bg)

        instruction = "Tafuta herufi hii:" if current_lang == "sw" else "Which letter makes this sound?"
        instr_label = Label(
            text=instruction,
            font_size="14sp",
            color=(0.4, 0.4, 0.5, 1),
            size_hint_y=None,
            height=24
        )
        prompt_card.add_widget(instr_label)

        replay_btn = KidButton(
            bg_color=self.PINK_ACCENT,
            text="Replay Sound",
            font_size="16sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=16,
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5}
        )
        replay_btn.bind(on_release=lambda inst: self.replay_target_sound(inst))
        prompt_card.add_widget(replay_btn)

        main_layout.add_widget(prompt_card)

        # 3. 2x2 Option Choices Grid
        grid = GridLayout(cols=2, spacing=12, size_hint_y=0.5)
        for i, option_letter in enumerate(self.options):
            card_btn = KidButton(
                bg_color=self.colors[i % len(self.colors)],
                text=f"{option_letter} {option_letter.lower()}",
                font_size="32sp",
                bold=True,
                radius=20,
                size_hint=(1, 1)
            )
            card_btn.bind(on_release=lambda inst, l=option_letter: self.check_answer(inst, l))
            grid.add_widget(card_btn)

        main_layout.add_widget(grid)

        # 4. Bottom Navigation Controls
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

        learn_btn = KidButton(
            bg_color=(0.38, 0.72, 0.96, 1),
            text="Learn" if current_lang == "en" else "Jifunze",
            font_size="13sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=14,
            size_hint=(0.5, 1)
        )
        learn_btn.bind(on_release=self.go_to_learn)

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

        footer_nav.add_widget(learn_btn)
        footer_nav.add_widget(home_btn)
        main_layout.add_widget(footer_nav)

        self.add_widget(main_layout)

    # --- GAME LOGIC ---
    def check_answer(self, instance, picked_letter):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()

        if picked_letter == self.target_letter:
            # Correct answer: award star and load next question
            app = App.get_running_app()
            app.add_star()
            instance.bg_color = (0.3, 0.8, 0.4, 1)  # Flash green
            Clock.schedule_once(self.next_question, 0.6)
        else:
            # Wrong answer: flash red briefly
            instance.bg_color = (0.9, 0.3, 0.3, 1)

    def replay_target_sound(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        app = App.get_running_app()
        play_sounds(self.target_letter, lang=getattr(app, 'current_language', 'en'))

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _update_widget_bg(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    def go_to_learn(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

    def go_to_onboarding(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding'