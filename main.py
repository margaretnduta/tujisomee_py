from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from screens.onboarding import OnboardingScreen
from screens.main_app import MainScreen


class Tujisomee(App):
    def build(self):
        self.current_language = "en"
        self.selected_view_mode = "grid"

        sm = ScreenManager(transition=SlideTransition(duration=0.3))
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(MainScreen(name="main"))

        return sm


if __name__ == "__main__":
    Tujisomee().run()