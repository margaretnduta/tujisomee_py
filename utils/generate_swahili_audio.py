import asyncio
import os
import string
import edge_tts

# Target Kenyan Swahili neural voice
VOICE = "sw-KE-ZuriNeural"
OUTPUT_DIR = "assets/mp3"

# Letter sounds/pronunciations mapped for Kenyan phonics
SWAHILI_PRONUNCIATION = {
    'A': 'A',
    'B': 'Ba',
    'C': 'Cha',
    'D': 'Da',
    'E': 'E',
    'F': 'Fa',
    'G': 'Ga',
    'H': 'Ha',
    'I': 'I',
    'J': 'Ja',
    'K': 'Ka',
    'L': 'La',
    'M': 'Ma',
    'N': 'Na',
    'O': 'O',
    'P': 'Pa',
    'Q': 'Kwa',
    'R': 'Ra',
    'S': 'Sa',
    'T': 'Ta',
    'U': 'U',
    'V': 'Va',
    'W': 'Wa',
    'X': 'Ksa',
    'Y': 'Ya',
    'Z': 'Za'
}


async def generate_audio():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating Kenyan Swahili audio files...")

    for letter, spoken_text in SWAHILI_PRONUNCIATION.items():
        filename = f"{OUTPUT_DIR}/{letter.lower()}.mp3"
        communicate = edge_tts.Communicate(spoken_text, VOICE)
        await communicate.save(filename)
        print(f"Saved: {filename} (Text: '{spoken_text}')")

    print("All Kenyan Swahili audio assets generated successfully.")


if __name__ == "__main__":
    asyncio.run(generate_audio())