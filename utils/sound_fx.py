import os
from kivy.core.audio import SoundLoader


class SoundFXManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundFXManager, cls).__new__(cls)
            cls._instance.sounds = {}
            cls._instance._load_sounds()
        return cls._instance

    def _load_sounds(self):
        # Place sfx files in assets/sfx/ (or fallback gracefully if missing)
        sfx_files = {
            "star": "assets/sfx/star.mp3",
            "correct": "assets/sfx/correct.mp3",
            "wrong": "assets/sfx/wrong.mp3",
            "click": "assets/sfx/click.mp3"
        }
        for name, path in sfx_files.items():
            if os.path.exists(path):
                sound = SoundLoader.load(path)
                if sound:
                    sound.volume = 0.6
                    self.sounds[name] = sound

    def play(self, name):
        """Play a loaded sound effect asynchronously."""
        sound = self.sounds.get(name)
        if sound:
            sound.stop()
            sound.play()


# Global shortcut
def play_sfx(name):
    SoundFXManager().play(name)