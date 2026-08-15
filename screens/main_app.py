from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window

# Disable 'Esc' key exiting the app
Config.set('kivy', 'exit_on_escape', '0')

# Phase 1 Onboarding Screens
from screens.onboarding import OnboardingScreen
from screens.onboarding_step2 import OnboardingStep2Screen
from screens.onboarding_step3 import OnboardingStep3Screen


class TujisomeeApp(App):
    current_language = 'en'
    user_mode = 'grid'

    def build(self):
        Window.size = (360, 640)  # Standard mobile aspect ratio preview
        
        # Prevent physical keypresses from crashing event loop
        Window.bind(on_key_down=lambda *args: None)

        sm = ScreenManager(transition=SlideTransition())

        # Register Phase 1 Screens
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(OnboardingStep2Screen(name='onboarding_step2'))
        sm.add_widget(OnboardingStep3Screen(name='onboarding_step3'))

        return sm


if __name__ == '__main__':
    try:
        TujisomeeApp().run()
    except KeyboardInterrupt:
        print("\nApp closed cleanly.")