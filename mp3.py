import os
from kivy.core.audio import SoundLoader

def play_sounds(letter, lang="en"):
    """
    Safely loads and plays an MP3 audio file based on letter and language.
    
    Args:
        letter (str): The letter to play (e.g., 'a')
        lang (str): 'en' for English, 'sw' for Kiswahili
    """
    clean_letter = letter.lower()
    path = os.path.join(".", "mp3", lang, f"{clean_letter}.mp3")
    full_path = os.path.abspath(path)
    
    if not os.path.exists(full_path):
        print(f"Warning: Audio file not found at: {full_path}")
        return None

    sound = SoundLoader.load(full_path)
    if sound:
        sound.play()
        return sound

    print(f"Error: Could not load sound at: {full_path}")
    return None