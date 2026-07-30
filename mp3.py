import os
from kivy.core.audio import SoundLoader

def play_sounds(path):
    """
    Safely loads and plays an MP3 audio file.
    
    Args:
        path (str): The relative path to the audio file (e.g., './mp3/en/a.mp3')
    
    Returns:
        Sound object or None: Returns the playing sound object if successful, else None.
    """
    # 1. Convert relative path to absolute path to avoid OS pathing issues
    full_path = os.path.abspath(path)
    
    # 2. Check if the audio file exists on disk
    if not os.path.exists(full_path):
        print(f"Warning: Audio file not found at path: {full_path}")
        return None

    # 3. Load the sound file using Kivy's core audio engine
    sound = SoundLoader.load(full_path)
    
    # 4. If loaded successfully, play it asynchronously and return the object
    if sound:
        sound.play()
        return sound

    print(f"Error: Kivy failed to load sound at: {full_path}")
    return None