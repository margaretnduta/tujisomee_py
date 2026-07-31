import string
import os
from gtts import gTTS

# Target directory for Swahili audio
sw_folder = os.path.join("mp3", "sw")
os.makedirs(sw_folder, exist_ok=True)

print("Generating Swahili (Kiswahili) audio files for A through Z...")

for letter in string.ascii_lowercase:
    file_path = os.path.join(sw_folder, f"{letter}.mp3")
    
    if os.path.exists(file_path):
        print(f"Skipping {file_path} (Already exists)")
        continue
        
    # Generate Swahili pronunciation
    tts = gTTS(text=letter, lang='sw')
    tts.save(file_path)
    print(f"Created: {file_path}")

print("\nSuccess! All Kiswahili audio files are ready in mp3/sw/")