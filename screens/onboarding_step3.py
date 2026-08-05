import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle

from ui.kid_button import KidButton


class MiniMockupWidget(BoxLayout):
    """Generates the visual card/grid mockup or language badge icon."""
    def __init__(self, item_type, mode_val="grid", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (60, 60)

        with self.canvas.before:
            Color(1, 1, 1, 0.95)
            self.mockup_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self._update_bg, size=self._update_bg)

        if item_type == 'lang':
            # Language Badge Icon (EN / SW)
            self.lang_label = Label(
                text="[b]EN[/b]",
                markup=True,
                font_size='16sp',
                color=(0.85, 0.35, 0.55, 1)
            )
            self.add_widget(self.lang_label)
        else:
            # Mode Preview Mockup (Matches Step 2 exactly)
            self.mode_container = BoxLayout()
            self.add_widget(self.mode_container)
            self.set_mode_view(mode_val)

    def _update_bg(self, instance, value):
        self.mockup_bg.pos = instance.pos
        self.mockup_bg.size = instance.size

    def update_lang_text(self, text):
        if hasattr(self, 'lang_label'):
            self.lang_label.text = f"[b]{text}[/b]"

    def set_mode_view(self, mode_val):
        if not hasattr(self, 'mode_container'):
            return

        self.mode_container.clear_widgets()

        if mode_val == 'grid':
            # Mini 2x2 Grid Preview Layout
            grid = GridLayout(cols=2, spacing=4, padding=6)
            for char in ['A', 'B', 'C', 'D']:
                lbl = Label(
                    text=f"[b]{char}[/b]", 
                    markup=True, 
                    font_size='10sp', 
                    color=(0.85, 0.35, 0.55, 1)
                )
                with lbl.canvas.before:
                    Color(0.98, 0.93, 0.96, 1)
                    lbl.bg_rect = RoundedRectangle(pos=lbl.pos, size=lbl.size, radius=[4])
                lbl.bind(pos=self._update_label_bg, size=self._update_label_bg)
                grid.add_widget(lbl)
            self.mode_container.add_widget(grid)
        else:
            # Mini Stacked Card Preview Layout
            card_box = BoxLayout(padding=8)
            mini_card = Label(
                text="[b]A a[/b]", 
                markup=True, 
                font_size='14sp', 
                color=(0.2, 0.6, 0.55, 1)
            )
            with mini_card.canvas.before:
                Color(0.85, 0.96, 0.93, 1)
                mini_card.bg_rect = RoundedRectangle(pos=mini_card.pos, size=mini_card.size, radius=[6])
            mini_card.bind(pos=self._update_label_bg, size=self._update_label_bg)
            card_box.add_widget(mini_card)
            self.mode_container.add_widget(card_box)

    def _update_label_bg(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size


class SummaryRowWidget(BoxLayout):
    """Summary row showing chosen options along with live mini mockups."""
    def __init__(self, row_type, **kwargs):
        super().__init__(**kwargs)
        self.row_type = row_type
        self.orientation = 'horizontal'
        self.padding = [12, 10, 12, 10]
        self.spacing = 15
        self.size_hint_y = None
        self.height = 80

        with self.canvas.before:
            Color(1, 1, 1, 0.7)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
        self.bind(pos=self._update_rect, size=self._update_rect)

        # Left Visual Icon / Mockup Widget
        self.mockup = MiniMockupWidget(item_type=row_type)
        self.add_widget(self.mockup)

        # Right Text Details
        text_layout = BoxLayout(orientation='vertical', spacing=2)
        self.title_label = Label(
            text="",
            markup=True,
            font_size='15sp',
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

    def update_data(self, badge_code, title, desc, mode_val=None):
        if self.row_type == 'lang':
            self.mockup.update_lang_text(badge_code)
        else:
            self.mockup.set_mode_view(mode_val if mode_val else 'grid')

        self.title_label.text = f"[b]{title}[/b]"
        self.desc_label.text = desc


class OnboardingStep3Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_lang = "en"
        self.user_mode = "grid"

        # Main Layout
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

        # 2. Header Title
        header_box = BoxLayout(orientation='vertical', size_hint_y=0.12, spacing=2)
        self.title_label = Label(
            text="",
            markup=True,
            font_size='20sp',
            bold=True,
            color=(0.8, 0.3, 0.5, 1),
            halign='center',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        header_box.add_widget(self.title_label)
        main_layout.add_widget(header_box)

        # 3. Summary Rows Layout
        summary_container = BoxLayout(orientation='vertical', spacing=12, size_hint_y=0.34)
        self.lang_row = SummaryRowWidget(row_type='lang')
        self.mode_row = SummaryRowWidget(row_type='mode')

        summary_container.add_widget(self.lang_row)
        summary_container.add_widget(self.mode_row)
        main_layout.add_widget(summary_container)

        # 4. Action Buttons
        actions_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.24)
        
        # Primary "Start" CTA Button
        self.start_btn = KidButton(
            bg_color=(0.88, 0.55, 0.72, 1),
            text="",
            font_size="16sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=20,
            size_hint_y=0.5
        )
        self.start_btn.bind(on_release=self.launch_app)

        # Secondary "Change my choices" Button
        self.change_btn = KidButton(
            bg_color=(1, 1, 1, 0.9),
            text="",
            font_size="14sp",
            bold=True,
            color=(0.8, 0.3, 0.5, 1),
            radius=20,
            size_hint_y=0.5
        )
        self.change_btn.bind(on_release=self.go_to_step1)

        actions_box.add_widget(self.start_btn)
        actions_box.add_widget(self.change_btn)
        main_layout.add_widget(actions_box)

        # 5. Bottom Navigation Bar with Arrow Buttons
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=15)

        # Previous Arrow (<)
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
        self.prev_arrow.bind(on_release=lambda x: self.go_to_step2())

        nav_bar.add_widget(self.prev_arrow)
        nav_bar.add_widget(BoxLayout()) # Spacer

        # Next Arrow (>)
        self.next_arrow = KidButton(
            bg_color=(0.88, 0.55, 0.72, 1),
            text=">",
            font_size="20sp",
            bold=True,
            color=(1, 1, 1, 1),
            radius=15,
            size_hint=(None, 1),
            width=50
        )
        self.next_arrow.bind(on_release=self.launch_app)
        nav_bar.add_widget(self.next_arrow)

        main_layout.add_widget(nav_bar)
        self.add_widget(main_layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.current_lang = getattr(app, 'current_language', getattr(app, 'user_language', 'en'))
        self.user_mode = getattr(app, 'user_mode', 'grid')

        is_sw = (self.current_lang == 'sw')

        # Strictly enforce English or Swahili text
        if is_sw:
            self.title_label.text = "Tuanze"
            self.start_btn.text = "Anza"
            self.change_btn.text = "Badilisha chaguo langu"
            
            # Language Summary Row
            self.lang_row.update_data("SW", "Kiswahili", "Sauti zitacheza kwa Kiswahili")
            
            # View Mode Summary Row with Visual Mockup
            if self.user_mode == 'grid':
                self.mode_row.update_data("", "Muundo wa Gridi", "Ona vitufe vyote vya sauti mara moja", mode_val='grid')
            else:
                self.mode_row.update_data("", "Muundo wa Kadi", "Pitia kadi moja baada ya nyingine", mode_val='card')
        else:
            self.title_label.text = "Let's go "
            self.start_btn.text = "Start"
            self.change_btn.text = "Change my choices"
            
            # Language Summary Row
            self.lang_row.update_data("EN", "English", "Sounds will play in English")
            
            # View Mode Summary Row with Visual Mockup
            if self.user_mode == 'grid':
                self.mode_row.update_data("", "Grid View", "See all sound buttons at once", mode_val='grid')
            else:
                self.mode_row.update_data("", "Card View", "Swipe through one letter at a time", mode_val='card')

    def go_to_step1(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding'

    def go_to_step2(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding_step2'

    def launch_app(self, instance):
        if hasattr(instance, 'animate_bounce'):
            instance.animate_bounce()
            
        if self.manager.has_screen("main"):
            self.manager.transition.direction = 'left'
            self.manager.current = 'main'
        else:
            print(f"Onboarding Complete! Lang: {self.current_lang}, Mode: {self.user_mode}")