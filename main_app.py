from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window

Config.set('kivy', 'exit_on_escape', '0')

from screens.onboarding import OnboardingScreen
from screens.onboarding_step2 import OnboardingStep2Screen
from screens.onboarding_step3 import OnboardingStep3Screen
from screens.main_screen import MainScreen  # <-- 1. Import MainScreen


class TujisomeeApp(App):
    current_language = 'en'
    user_mode = 'grid'

    def build(self):
        Window.size = (360, 640)
        Window.bind(on_key_down=lambda *args: None)

        sm = ScreenManager(transition=SlideTransition())

        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(OnboardingStep2Screen(name='onboarding_step2'))
        sm.add_widget(OnboardingStep3Screen(name='onboarding_step3'))
        sm.add_widget(MainScreen(name='main'))  # <-- 2. Register MainScreen

        return sm


if __name__ == '__main__':
    try:
        TujisomeeApp().run()
    except KeyboardInterrupt:
        print("\nApp closed cleanly.")