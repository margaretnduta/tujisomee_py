from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window

# Import KidButton from ui package
from ui.kid_button import KidButton

# Set default soft pink background
Window.clearcolor = (0.98, 0.93, 0.96, 1.0)


class OnboardingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_language = "en"

        # Main responsive container using fractional size_hints
        main_layout = BoxLayout(
            orientation="vertical",
            padding=[30, 20, 30, 30],
            spacing=15
        )

        # 1. Mascot Image (Scales cleanly on mobile using fit_mode)
        mascot_box = BoxLayout(size_hint_y=0.35)
        self.mascot = Image(
            source="assets/logo.png",
            fit_mode="contain"
        )
        mascot_box.add_widget(self.mascot)

        # 2. App Title Header
        title_box = BoxLayout(orientation="vertical", size_hint_y=0.18, spacing=2)
        title_label = Label(
            text="Tujisomee\nPhonics ",
            font_size="26sp",
            bold=True,
            color=(0.8, 0.3, 0.5, 1),
            halign="center",
            valign="middle"
        )
        title_label.bind(size=title_label.setter('text_size'))
        title_box.add_widget(title_label)

        # 3. Instruction Subtitle
        sub_label = Label(
            text="Pick a language to start",
            font_size="14sp",
            bold=True,
            color=(0.3, 0.3, 0.4, 1),
            size_hint_y=0.07,
            halign="center"
        )

        # 4. Language Choice Container
        lang_container = BoxLayout(
            orientation="horizontal",
            spacing=15,
            size_hint_y=0.22,
            padding=[5, 0]
        )

        # English Card
        self.btn_en = KidButton(
            bg_color=(1.0, 0.93, 0.73, 1),  # Active canary yellow
            text="English",
            font_size="16sp",
            bold=True,
            color=(0.2, 0.2, 0.3, 1),
            radius=18
        )
        self.btn_en.bind(on_release=lambda x: self.select_lang("en"))

        # Swahili Card
        self.btn_sw = KidButton(
            bg_color=(0.85, 0.85, 0.85, 0.5),  # Muted inactive gray
            text="Kiswahili",
            font_size="16sp",
            bold=True,
            color=(0.2, 0.2, 0.3, 1),
            radius=18
        )
        self.btn_sw.bind(on_release=lambda x: self.select_lang("sw"))

        lang_container.add_widget(self.btn_en)
        lang_container.add_widget(self.btn_sw)

        # 5. Bottom "Let's Learn!" Primary Button
        cta_btn = KidButton(
            bg_color=(0.88, 0.55, 0.72, 1),
            text="Let's Learn!",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=22,
            size_hint_y=0.15
        )
        cta_btn.bind(on_release=self.start_learning)

        # Assemble layout
        main_layout.add_widget(mascot_box)
        main_layout.add_widget(title_box)
        main_layout.add_widget(sub_label)
        main_layout.add_widget(lang_container)
        main_layout.add_widget(cta_btn)

        self.add_widget(main_layout)

    def select_lang(self, lang):
        self.selected_language = lang
        if lang == "en":
            self.btn_en.set_color((1.0, 0.93, 0.73, 1))
            self.btn_sw.set_color((0.85, 0.85, 0.85, 0.5))
        else:
            self.btn_sw.set_color((0.5, 0.8, 0.8, 1))  # Soft turquoise active
            self.btn_en.set_color((0.85, 0.85, 0.85, 0.5))

    def start_learning(self, instance):
        instance.animate_bounce()
        app = App.get_running_app()
        app.current_language = self.selected_language
        
        # When main_app.py screen is added, we navigate using:
        if self.manager.has_screen("main"):
            self.manager.current = "main"
        else:
            print(f"Selected language: {app.current_language}. Main screen coming next!")