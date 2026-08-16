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
from utils.sound_fx import play_sfx


class QuizScreen(Screen):
    PINK_ACCENT = (0.88, 0.55, 0.72, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.letters = list(string.ascii_uppercase)
        self.target_letter = "A"
        self.options = []
        
        self.colors = [
            (0.38, 0.72, 0.96, 1),
            (0.98, 0.76, 0.30, 1),
            (0.96, 0.48, 0.44, 1),
            (0.48, 0.82, 0.48, 1)
        ]

    def on_enter(self):
        self.next_question()

    def generate_options(self):
        self.target_letter = random.choice(self.letters)
        wrong_letters = [l for l in self.letters if l != self.target_letter]
        self.options = random.sample(wrong_letters, 3) + [self.target_letter]
        random.shuffle(self.options)

    def next_question(self, *args):
        self.generate_options()
        self.clear_widgets()
        self.build_ui()
        
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

        # Header Bar
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

        # Mascot Speech Bubble Card
        mascot_card = BoxLayout(orientation="horizontal", size_hint_y=0.32, spacing=10, padding=[12, 8])
        with mascot_card.canvas.before:
            Color(1, 1, 1, 0.9)
            mascot_card.bg_rect = RoundedRectangle(pos=mascot_card.pos, size=mascot_card.size, radius=[20])
        mascot_card.bind(pos=self._update_widget_bg, size=self._update_widget_bg)

        mascot_img = Image(source="assets/logo.png", fit_mode="contain", size_hint=(0.3, 1))
        mascot_card.add_widget(mascot_img)

        speech_box = BoxLayout(orientation="vertical", size_hint=(0.7, 1), spacing=4)
        
        self.speech_msg = getattr(self, 'speech_msg_text', None)
        default_speech = "Unaijua herufi hii? Tega sikio" if current_lang == "sw" else "Can you find this sound? Listen carefully"
        
        self.speech_label = Label(
            text=f"[i]\"{self.speech_msg or default_speech}\"[/i]",
            markup=True,
            font_size="13sp",
            color=(0.3, 0.3, 0.4, 1),
            halign="left",
            valign="middle"
        )
        self.speech_label.bind(size=self.speech_label.setter('text_size'))
        speech_box.add_widget(self.speech_label)

        replay_btn = KidButton(
            bg_color=self.PINK_ACCENT,
            text="Replay" if current_lang == "en" else "Sikiliza",
            font_size="13sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=12,
            size_hint=(1, 0.45)
        )
        replay_btn.bind(on_release=self.replay_target_sound)
        speech_box.add_widget(replay_btn)

        mascot_card.add_widget(speech_box)
        main_layout.add_widget(mascot_card)

        # 2x2 Choice Grid
        grid = GridLayout(cols=2, spacing=12, size_hint_y=0.53)
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

        # Navigation Footer
        footer_nav = BoxLayout(orientation="horizontal", size_hint_y=None, height=52, spacing=10, padding=[8, 4])
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

    def check_answer(self, instance, picked_letter):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()

        app = App.get_running_app()
        lang = getattr(app, 'current_language', 'en')

        if picked_letter == self.target_letter:
            play_sfx("correct")
            play_sfx("star")
            app.add_star()
            
            praise = "Safiri sana Umepatia" if lang == "sw" else "Awesome job  You got a star"
            self.speech_msg_text = praise
            instance.bg_color = (0.3, 0.8, 0.4, 1)
            Clock.schedule_once(self.next_question, 0.8)
        else:
            play_sfx("wrong")
            retry_msg = "Jaribu tena  Unaweza" if lang == "sw" else "Oops Try another one"
            self.speech_label.text = f"[i]\"{retry_msg}\"[/i]"
            instance.bg_color = (0.9, 0.3, 0.3, 1)

    def replay_target_sound(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
        play_sfx("click")
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
        play_sfx("click")
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

    def go_to_onboarding(self, instance):
        play_sfx("click")
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding'