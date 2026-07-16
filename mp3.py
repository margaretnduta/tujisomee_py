import os
from kivy.core.audio import SoundLoader


def play_sounds(path):
    full_path = os.path.abspath(path)
    if not os.path.exists(full_path):
        print(f"Audio file not found: {full_path}")
        return None

    sound = SoundLoader.load(full_path)
    if sound:
        sound.play()
        return sound

    return None