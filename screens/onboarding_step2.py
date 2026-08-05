import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

from ui.kid_button import KidButton


class ModeCardWidget(BoxLayout):
    """Custom selection card featuring visual UI preview mockups."""
    def __init__(self, mode_id, active_bg, **kwargs):
        super().__init__(**kwargs)
        self.mode_id = mode_id
        self.active_bg = active_bg
        self.inactive_bg = (0.88, 0.88, 0.90, 0.6)
        
        self.orientation = 'horizontal'
        self.padding = [15, 12, 15, 12]
        self.spacing = 15
        self.size_hint_y = None
        self.height = 105

        with self.canvas.before:
            self.bg_color = Color(*self.inactive_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[18])

        self.bind(pos=self._update_rect, size=self._update_rect)

        # Left Container: Mini Visual UI Mockup
        mockup_container = BoxLayout(size_hint=(None, None), size=(75, 75))
        with mockup_container.canvas.before:
            Color(1, 1, 1, 0.9)
            self.mockup_bg = RoundedRectangle(pos=mockup_container.pos, size=mockup_container.size, radius=[14])
        mockup_container.bind(pos=self._update_mockup_bg, size=self._update_mockup_bg)

        if mode_id == 'grid':
            # Mini 2x2 Grid Preview
            grid = GridLayout(cols=2, spacing=5, padding=8)
            for char in ['A', 'B', 'C', 'D']:
                lbl = Label(
                    text=f"[b]{char}[/b]", 
                    markup=True, 
                    font_size='12sp', 
                    color=(0.85, 0.35, 0.55, 1)
                )
                with lbl.canvas.before:
                    Color(0.98, 0.93, 0.96, 1)
                    lbl.bg_rect = RoundedRectangle(pos=lbl.pos, size=lbl.size, radius=[4])
                lbl.bind(pos=self._update_label_bg, size=self._update_label_bg)
                grid.add_widget(lbl)
            mockup_container.add_widget(grid)

        else:
            # Mini Stacked Card Preview
            card_box = BoxLayout(padding=10)
            mini_card = Label(
                text="[b]A a[/b]", 
                markup=True, 
                font_size='16sp', 
                color=(0.2, 0.6, 0.55, 1)
            )
            with mini_card.canvas.before:
                Color(0.85, 0.96, 0.93, 1)
                mini_card.bg_rect = RoundedRectangle(pos=mini_card.pos, size=mini_card.size, radius=[8])
            mini_card.bind(pos=self._update_label_bg, size=self._update_label_bg)
            card_box.add_widget(mini_card)
            mockup_container.add_widget(card_box)

        self.add_widget(mockup_container)

        # Right Container: Text Description
        text_layout = BoxLayout(orientation='vertical', spacing=4)
        self.title_label = Label(
            text="",
            markup=True,
            font_size='16sp',
            bold=True,
            color=(0.2, 0.2, 0.3, 1),
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))

        self.desc_label = Label(
            text="",
            font_size='12sp',
            color=(0.4, 0.4, 0.45, 1),
            halign='left',
            valign='middle'
        )
        self.desc_label.bind(size=self.desc_label.setter('text_size'))

        text_layout.add_widget(self.title_label)
        text_layout.add_widget(self.desc_label)
        self.add_widget(text_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_mockup_bg(self, instance, value):
        self.mockup_bg.pos = instance.pos
        self.mockup_bg.size = instance.size

    def _update_label_bg(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    def set_active(self, active):
        if active:
            self.bg_color.rgba = self.active_bg
        else:
            self.bg_color.rgba = self.inactive_bg

    def update_text(self, title, desc):
        self.title_label.text = f"[b]{title}[/b]"
        self.desc_label.text = desc


class OnboardingStep2Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_mode = None  # Initially no selection
        self.current_lang = "en"

        # Main background
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=[25, 20, 25, 20], 
            spacing=12
        )
        with main_layout.canvas.before:
            Color(0.98, 0.93, 0.96, 1.0)
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self._update_bg, size=self._update_bg)

        # 1. Mascot Logo
        mascot_box = BoxLayout(size_hint_y=0.22)
        self.mascot = Image(
            source="assets/logo.png",
            fit_mode="contain"
        )
        mascot_box.add_widget(self.mascot)
        main_layout.add_widget(mascot_box)

        # 2. Header
        header_box = BoxLayout(orientation='vertical', size_hint_y=0.14, spacing=2)
        self.title_label = Label(
            text="",
            markup=True,
            font_size='19sp',
            bold=True,
            color=(0.8, 0.3, 0.5, 1),
            halign='center',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))

        self.subtitle_label = Label(
            text="",
            font_size='13sp',
            bold=True,
            color=(0.4, 0.4, 0.5, 1),
            halign='center',
            valign='middle'
        )
        self.subtitle_label.bind(size=self.subtitle_label.setter('text_size'))

        header_box.add_widget(self.title_label)
        header_box.add_widget(self.subtitle_label)
        main_layout.add_widget(header_box)

        # 3. Mode Cards Container
        options_layout = BoxLayout(orientation='vertical', spacing=12, size_hint_y=0.42)

        self.card_grid = ModeCardWidget(
            mode_id='grid',
            active_bg=(1.0, 0.93, 0.73, 1) # Yellow
        )

        self.card_card = ModeCardWidget(
            mode_id='card',
            active_bg=(0.68, 0.91, 0.86, 1) # Mint Teal
        )

        options_layout.add_widget(self.card_grid)
        options_layout.add_widget(self.card_card)
        main_layout.add_widget(options_layout)

        # 4. Action CTA Button ("Start Learning")
        self.start_btn = KidButton(
            bg_color=(0.88, 0.55, 0.72, 1),
            text="",
            font_size="16sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=22,
            size_hint_y=0.14
        )
        self.start_btn.bind(on_release=self.start_learning)
        main_layout.add_widget(self.start_btn)

        # 5. Bottom Navigation Bar with Arrow Buttons
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=15)

        # Previous Arrow Button (<) - Always Visible
        self.prev_arrow = KidButton(
            bg_color=(1.0, 1.0, 1.0, 0.9),
            text="<",
            font_size="20sp",
            bold=True,
            color=(0.5, 0.4, 0.5, 1),
            radius=15,
            size_hint=(None, 1),
            width=50
        )
        self.prev_arrow.bind(on_release=lambda x: self.go_back_to_step1())

        # Middle spacer
        nav_bar.add_widget(self.prev_arrow)
        nav_bar.add_widget(BoxLayout())

        # Next Arrow Button (>) - Hidden until user picks a mode
        self.next_arrow = KidButton(
            bg_color=(0.88, 0.55, 0.72, 1),
            text=">",
            font_size="20sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=15,
            size_hint=(None, 1),
            width=50,
            opacity=0,           # Hidden initially
            disabled=True        # Disabled until triggered
        )
        self.next_arrow.bind(on_release=self.start_learning)
        nav_bar.add_widget(self.next_arrow)

        main_layout.add_widget(nav_bar)
        self.add_widget(main_layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.current_lang = getattr(app, 'current_language', getattr(app, 'user_language', 'en'))

        if self.current_lang == 'sw':
            self.title_label.text = "How would you like to learn today?"
            self.subtitle_label.text = "Unapenda kujifunza vipi?"
            self.card_grid.update_text("Muundo wa Gridi", "Ona vitufe vyote vya sauti A–Z mara moja.")
            self.card_card.update_text("Muundo wa Kadi", "Pitia kadi kubwa za sauti moja baada ya nyingine.")
            self.start_btn.text = "Anza kujifunza"
        else:
            self.title_label.text = "How would you like to learn today?"
            self.subtitle_label.text = "Unapenda kujifunza vipi?"
            self.card_grid.update_text("Grid View", "See all A–Z sound buttons at once.")
            self.card_card.update_text("Card View", "Swipe through giant sound cards one by one.")
            self.start_btn.text = "Start learning"

        # Default: auto-select grid mode or reset state
        self.select_mode(self.selected_mode if self.selected_mode else 'grid')

    def select_mode(self, mode):
        self.selected_mode = mode
        self.card_grid.set_active(mode == 'grid')
        self.card_card.set_active(mode == 'card')

        # Reveal the Next Arrow (>) once a selection event happens!
        self.next_arrow.opacity = 1
        self.next_arrow.disabled = False

    def on_touch_down(self, touch):
        if self.card_grid.collide_point(*touch.pos):
            self.select_mode('grid')
        elif self.card_card.collide_point(*touch.pos):
            self.select_mode('card')

        return super().on_touch_down(touch)

    def go_back_to_step1(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding'

    def start_learning(self, instance):
        if not self.selected_mode:
            return  # Safety guard

        # Check if instance has the bounce animation method before calling
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()

        app = App.get_running_app()
        app.user_mode = self.selected_mode
        
        # Transition directly to Step 3 (Summary Screen)
        self.manager.transition.direction = 'left'
        self.manager.current = 'onboarding_step3'