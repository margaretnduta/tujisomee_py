from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation


class KidButton(Button):
    """ Custom Button with rounded corners, dynamic background color, and tap-bounce animations. """

    def __init__(self, bg_color=(0.3, 0.6, 0.9, 1), radius=25, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Removes default gray Kivy button skin
        self.bg_color = bg_color
        self.radius = radius

        # Draw custom rounded card background
        with self.canvas.before:
            self.color_instruction = Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self.radius]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        """ Keeps the rounded rectangle aligned with button position and size updates. """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_color(self, new_color):
        """ Dynamically updates button background color. """
        self.bg_color = new_color
        self.color_instruction.rgba = new_color

    def animate_bounce(self):
        # Animate physical pixel size instead of size_hint to avoid NoneType errors
        orig_w, orig_h = self.size

        # Shrink by 8% then pop back to original size
        anim = Animation(size=(orig_w * 0.92, orig_h * 0.92), duration=0.06) + \
               Animation(size=(orig_w, orig_h), duration=0.06)
        anim.start(self)