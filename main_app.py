from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window

Config.set('kivy', 'exit_on_escape', '0')

from screens.onboarding import OnboardingScreen
from screens.onboarding_step2 import OnboardingStep2Screen
from screens.onboarding_step3 import OnboardingStep3Screen
from screens.main_screen import MainScreen
from screens.quiz_screen import QuizScreen
from utils.storage import load_settings, save_settings


class TujisomeeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        settings = load_settings()
        self.current_language = settings.get("current_language", "en")
        self.user_mode = settings.get("user_mode", "grid")
        self.stars = settings.get("stars", 0)

    def update_language(self, lang_code):
        self.current_language = lang_code
        save_settings({"current_language": lang_code})

    def update_mode(self, mode):
        self.user_mode = mode
        save_settings({"user_mode": mode})

    def add_star(self):
        """Increments star counter and saves state."""
        self.stars += 1
        save_settings({"stars": self.stars})

    def build(self):
        Window.size = (360, 640)
        Window.bind(on_key_down=lambda *args: None)

        sm = ScreenManager(transition=SlideTransition())

        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(OnboardingStep2Screen(name='onboarding_step2'))
        sm.add_widget(OnboardingStep3Screen(name='onboarding_step3'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(QuizScreen(name='quiz'))

        return sm


if __name__ == '__main__':
    try:
        TujisomeeApp().run()
    except KeyboardInterrupt:
        print("\nApp closed cleanly.")