import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window

class SelectableCard(BoxLayout):
    """Custom card with active visual feedback for mode selection."""
    def __init__(self, mode_id, **kwargs):
        super().__init__(**kwargs)
        self.mode_id = mode_id
        self.orientation = 'horizontal'
        self.padding = 15
        self.spacing = 15
        self.size_hint_y = None
        self.height = 100
        self.is_selected = False

        # Colors
        self.normal_bg = (0.98, 0.93, 0.75, 1) if mode_id == 'grid' else (0.68, 0.91, 0.86, 1)
        self.selected_border = (0.85, 0.35, 0.55, 1)
        
        with self.canvas.before:
            self.bg_color_instruction = Color(*self.normal_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[18])
            self.border_color_instruction = Color(0, 0, 0, 0)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 18), width=3)

        self.bind(pos=self._update_rect, size=self._update_rect)

        # Icon container
        icon_box = BoxLayout(size_hint_x=None, width=60)
        with icon_box.canvas.before:
            Color(1, 1, 1, 0.8)
            self.icon_bg = RoundedRectangle(pos=icon_box.pos, size=icon_box.size, radius=[12])
        icon_box.bind(pos=self._update_icon_bg, size=self._update_icon_bg)
        self.add_widget(icon_box)

        # Labels
        text_layout = BoxLayout(orientation='vertical', spacing=4)
        self.title_label = Label(
            text="",
            markup=True,
            font_size='18sp',
            color=(0.2, 0.1, 0.2, 1),
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))

        self.desc_label = Label(
            text="",
            font_size='13sp',
            color=(0.4, 0.4, 0.4, 1),
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
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, 18)

    def _update_icon_bg(self, instance, value):
        self.icon_bg.pos = instance.pos
        self.icon_bg.size = instance.size

    def set_selected(self, selected):
        self.is_selected = selected
        if selected:
            self.border_color_instruction.rgba = self.selected_border
        else:
            self.border_color_instruction.rgba = (0, 0, 0, 0)

    def update_texts(self, title, desc):
        self.title_label.text = f"[b]{title}[/b]"
        self.desc_label.text = desc


class OnboardingStep2Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_mode = "grid"
        self.current_lang = "en"
        self.touch_start_x = 0

        # Background Layout
        main_layout = BoxLayout(orientation='vertical', padding=[24, 20, 24, 20], spacing=15)
        with main_layout.canvas.before:
            Color(0.98, 0.92, 0.95, 1)
            self.bg_rect = RoundedRectangle(pos=main_layout.pos, size=main_layout.size)
        main_layout.bind(pos=self._update_bg, size=self._update_bg)

        # Header Section
        header_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80, spacing=5)
        self.title_label = Label(
            text="",
            markup=True,
            font_size='22sp',
            color=(0.3, 0.1, 0.25, 1),
            halign='center'
        )
        self.subtitle_label = Label(
            text="",
            font_size='15sp',
            color=(0.5, 0.45, 0.5, 1),
            halign='center'
        )
        header_box.add_widget(self.title_label)
        header_box.add_widget(self.subtitle_label)
        main_layout.add_widget(header_box)

        # Option Cards
        options_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, height=220)
        self.grid_card = SelectableCard(mode_id='grid')
        self.card_card = SelectableCard(mode_id='card')

        options_layout.add_widget(self.grid_card)
        options_layout.add_widget(self.card_card)
        main_layout.add_widget(options_layout)

        main_layout.add_widget(BoxLayout()) # Spacer

        # Action CTA Button
        self.start_btn = Button(
            text="",
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=55,
            background_normal='',
            background_color=(0.93, 0.55, 0.68, 1),
            color=(1, 1, 1, 1)
        )
        self.start_btn.bind(on_release=self.start_learning)
        main_layout.add_widget(self.start_btn)

        # Bottom Slider / Pagination Bar
        indicator_box = BoxLayout(size_hint_y=None, height=30, spacing=12)
        indicator_box.add_widget(BoxLayout())
        
        self.dot1 = Label(text="•", font_size='28sp', color=(0.8, 0.7, 0.75, 1), size_hint=(None, None), size=(15, 15))
        self.bar2 = Label(text="▬", font_size='20sp', color=(0.85, 0.35, 0.55, 1), size_hint=(None, None), size=(30, 15))
        
        indicator_box.add_widget(self.dot1)
        indicator_box.add_widget(self.bar2)
        indicator_box.add_widget(BoxLayout())
        
        main_layout.add_widget(indicator_box)
        self.add_widget(main_layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_pre_enter(self, *args):
        """Strictly syncs all screen labels to the active language."""
        app = App.get_running_app()
        self.current_lang = getattr(app, 'current_language', getattr(app, 'user_language', 'en'))

        if self.current_lang == 'sw':
            self.title_label.text = "[b]Unapenda kujifunza vipi leo?[/b]"
            self.subtitle_label.text = "Chagua muundo wa kuona masomo"
            self.grid_card.update_texts("Muundo wa Gridi", "Ona vitufe vyote vya sauti A–Z mara moja.")
            self.card_card.update_texts("Muundo wa Kadi", "Pitia kadi kubwa za sauti moja baada ya nyingine.")
            self.start_btn.text = "Anza kujifunza"
        else:
            self.title_label.text = "[b]How would you like to learn today?[/b]"
            self.subtitle_label.text = "Choose your preferred view"
            self.grid_card.update_texts("Grid View", "See all A–Z sound buttons at once.")
            self.card_card.update_texts("Card View", "Swipe through giant sound cards one by one.")
            self.start_btn.text = "Start learning"

        self.apply_mode_selection(self.selected_mode)

    def apply_mode_selection(self, mode):
        self.selected_mode = mode
        self.grid_card.set_selected(mode == 'grid')
        self.card_card.set_selected(mode == 'card')

    def on_touch_down(self, touch):
        """Handles card clicks and starts horizontal swipe gesture detection."""
        self.touch_start_x = touch.x

        if self.grid_card.collide_point(*touch.pos):
            self.apply_mode_selection('grid')
            return True
        elif self.card_card.collide_point(*touch.pos):
            self.apply_mode_selection('card')
            return True

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Detects right swipe gesture to slide back to Step 1 smoothly."""
        if touch.x - self.touch_start_x > 100: # Swiped Right
            self.go_back_to_step1()
            return True
        return super().on_touch_up(touch)

    def go_back_to_step1(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'onboarding'

    def start_learning(self, instance):
        app = App.get_running_app()
        app.user_mode = self.selected_mode
        if self.manager.has_screen("main"):
            self.manager.transition.direction = 'left'
            self.manager.current = 'main'
        else:
            print(f"Mode chosen: {self.selected_mode}. Screen 'main' target coming next!")