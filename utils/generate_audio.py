import string
import os
from gtts import gTTS

# Ensure the mp3 folder exists
os.makedirs("mp3", exist_ok=True)

print("Generating audio files for A through Z...")

for letter in string.ascii_lowercase:
    file_path = f"mp3/{letter}.mp3"
    
    # Skip if file already exists so we don't overwrite your existing files
    if os.path.exists(file_path):
        print(f"Skipping {file_path} (already exists)")
        continue
        
    # Generate MP3 using Google Text-to-Speech
    tts = gTTS(text=letter, lang='en')
    tts.save(file_path)
    print(f"Created: {file_path}")

print("Done! All 26 audio files are ready.")
