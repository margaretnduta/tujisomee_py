import os
import sys
from kivy.core.audio import SoundLoader


def get_asset_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def play_sounds(letter, lang="en"):
    """
    Safely loads and plays an MP3 audio file based on letter and language.
    """
    clean_letter = letter.lower()
    
    # Construct relative path: mp3/en/a.mp3 or mp3/sw/a.mp3
    rel_path = os.path.join("mp3", lang, f"{clean_letter}.mp3")
    
    # Get the true absolute path (works both in VS Code and inside .exe)
    full_path = get_asset_path(rel_path)

    if not os.path.exists(full_path):
        print(f"Warning: Audio file not found at: {full_path}")
        return None

    sound = SoundLoader.load(full_path)
    if sound:
        sound.play()
        return sound

    print(f"Error: Could not load sound at: {full_path}")
    return None