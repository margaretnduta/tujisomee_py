#load the screen manager, and launch the app
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition

# Import screens from the screens/ package
from screens.onboarding import OnboardingScreen


class Tujisomee(App):
    def build(self):
        # Global state accessible across screens via App.get_running_app()
        self.current_language = "en"
        self.selected_view_mode = "grid"

        # ScreenManager manages screen navigation
        sm = ScreenManager(transition=SlideTransition(duration=0.3))
        sm.add_widget(OnboardingScreen(name="onboarding"))
        
        return sm


if __name__ == "__main__":
    Tujisomee().run()