from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from screens.onboarding import OnboardingScreen
from screens.onboarding_step2 import OnboardingStep2Screen
from screens.onboarding_step3 import OnboardingStep3Screen
from kivy.core.window import Window


Window.bind(on_key_down=lambda *args: None)

class Tujisomee(App):
    def build(self):
        self.current_language = "en"
        self.selected_view_mode = "grid"

        sm = ScreenManager(transition=SlideTransition(duration=0.3))
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(OnboardingStep2Screen(name='onboarding_step2'))
        sm.add_widget(OnboardingStep3Screen(name='onboarding_step3'))
        return sm


if __name__ == "__main__":
    Tujisomee().run()