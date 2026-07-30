# Tujisomee

*Tujisomee* — Swahili for "let's read together" — is an early-stage Kivy
(Python) app prototype for an offline learning tool aimed at helping young
kids in Kenya learn through sound and repetition.

This is an early prototype. Two buttons currently play audio and track
click count as a proof of concept for the tap-to-hear interaction pattern
the full app will be built around.

## Status

🚧 **Early prototype** — core interaction (tap a button, hear a sound,
track engagement) is working. Not yet tied to real lesson content.

## Requirements

- Python 3.9+
- [Kivy](https://kivy.org/)
- An audio playback method (currently `playsound`, referenced via `mp3.py`)

```bash
pip install kivy playsound
```

## Project structure

```
tujisomee/
├── main.py            # the Kivy App — UI, buttons, click tracking
├── mp3.py             # audio playback helper (play_sounds)
├── requirements.txt
└── sounds/            # audio files referenced by play_sounds()
    ├── button_a.mp3
    └── button_b.mp3
```

## Running it

```bash
python main.py
```

You should see:
- Two static welcome labels
- A counter label (starts at `0`)
- **Play Sound A** and **Play Sound B** buttons — each plays a sound and
  increments the counter

## Known issues / next fixes

- [ ] `play_sounds()` currently takes no arguments, so both buttons trigger
      identical behavior. It needs a file path argument so each button
      plays its own distinct sound.
- [ ] No real audio files exist yet in `sounds/` — placeholders or real
      recordings need to be added and wired up.
- [ ] `playsound` blocks the app while audio plays. Consider switching to
      Kivy's own `kivy.core.audio.SoundLoader`, which is non-blocking and
      packages more reliably for Android via Buildozer.
- [ ] `self.count` currently counts total clicks across both buttons
      combined — decide whether it should track something more meaningful
      (e.g. sounds heard, letters practiced) as real content is added.

## Roadmap

1. Fix `play_sounds()` to accept a filepath and wire each button to its own
   sound
2. Add real audio content to `sounds/`
3. Swap `playsound` → `SoundLoader`
4. Replace hardcoded buttons with content driven by a simple JSON file
   (letter/word/sound), so new lessons don't require code changes
5. Add basic progress tracking (local SQLite) so progress persists between
   app runs
6. Test on a real low-end Android device
7. Package with [Buildozer](https://github.com/kivy/buildozer) into an
   installable `.apk`

## Why this matters

Many early-grade classrooms in Kenya are under-resourced and short on
trained teachers, particularly in rural areas. An offline-first phone app
that repeats letter/word sounds as often as a child needs — without
requiring mobile data — can meaningfully support phonics practice both in
and out of the classroom.