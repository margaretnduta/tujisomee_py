# 🎈 Tujisomee Phonics

**Tujisomee Phonics** is a vibrant, interactive, and child-friendly educational application built with Python and Kivy. Designed specifically for early childhood learning, the app helps young children learn letter sounds (A–Z) through engaging visuals, satisfying tactile animations, and instant audio feedback.

---

## ✨ Features

- **📱 Interactive Slideshow Mode:** Large, easy-to-read letter cards that focus a child's attention on one letter at a time.
- **🔊 Instant Phonics Playback:** Audio automatically plays when sliding to a new letter or tapping the card.
- **🎨 Kid-Friendly UI/UX:** Warm pastel color palettes, soft rounded corners, and clear visual contrast designed for toddlers and young children.
- **✨ Bounce Tap Animations:** Satisfying tactile visual feedback whenever a card or navigation button is pressed.
- **👈 Modern Floating Controls:** Sleek side navigation arrows (< and >) that maximize screen space for the interactive cards.
- **🌍 Scalable Architecture:** Built with multilingual support in mind, allowing effortless expansion to languages like Swahili, Spanish, French, and more.

---

## 📁 Project Structure

```text
Tujisomee/
│
├── main.py              # Main Kivy application & UI layout
├── mp3.py               # Asynchronous audio loader utility
├── generate_audio.py    # Helper script to automatically generate A-Z speech files
├── requirements.txt     # Python dependency list
├── README.md            # Project documentation
└── mp3/                 # Audio assets directory
    ├── a.mp3
    ├── b.mp3
    └── ... (up to z.mp3)

```

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have **Python 3.9+** installed on your system.

### 2. Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/Tujisomee.git](https://github.com/your-username/Tujisomee.git)
cd Tujisomee

```


2. **Set up a virtual environment (Recommended):**
```bash
# Windows
python -m venv kivy_venv
kivy_venv\Scripts\activate

# Mac/Linux
python3 -m venv kivy_venv
source kivy_venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Generate missing A-Z audio files (Optional):**
If you need to generate or update the default English audio files:
```bash
pip install gTTS
python generate_audio.py

```



---

## 🎮 Running the Application

To start the app, simply execute:

```bash
python main.py

```

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python
* **GUI Framework:** [Kivy](https://kivy.org/) (Core layouts, Carousel, Animations, Canvas instructions)
* **Audio Engine:** `kivy.core.audio` (Non-blocking, cross-platform audio playback)
* **TTS Generator:** `gTTS` (Google Text-to-Speech for automated asset generation)

---

## 🛣️ Roadmap & Future Enhancements

* [x] Single-card slideshow layout with side navigation
* [x] Custom rounded button styling & pastel palettes
* [x] Interactive tap bounce animations
* [ ] **Multilingual Toggle:** One-tap switching between English, Swahili, and other regional languages
* [ ] **"Find the Letter" Quiz Mode:** Fun audio-guided interactive mini-game for kids
* [ ] **Custom Mascot & Illustrated Backgrounds:** Adding friendly animal characters and nature themes
* [ ] **Mobile Packaging:** Android (`.apk`) compilation via Buildozer

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

---

Whenever you're ready to continue building, let me know if we should jump into **Feature 2: Multilingual Language Toggle**!

```
