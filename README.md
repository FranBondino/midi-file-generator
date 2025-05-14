# Melodic Techno Remix Generator

This repository contains Python scripts to automate the creation of melodic techno remixes for **Cyberia Layer 2**, **Duvet**, and **Big in Japan** using audio analysis and MIDI generation. Designed for beginners in music theory and electronic music production, it integrates with **Ableton Live** to produce club-ready tracks.

The scripts download audio, analyze tempo and key, generate MIDI files for bass, leads, chords, and arpeggios, and analyze mix balance — streamlining the remix process.

---

## 🎵 Features

- **Audio Download and Analysis**  
  Downloads MP3s from YouTube, estimates tempo and key, and separates harmonic/percussive elements.

- **MIDI Generation**  
  Creates techno-style MIDI files (basslines, arpeggios, chords) in detected keys (e.g., E minor, B minor, G# minor).

- **Random Arpeggios**  
  Generates dynamic, randomized arpeggio MIDI for creative flair.

- **Mix Analysis**  
  Analyzes exported remix WAVs for frequency balance.

- **Beginner-Friendly**  
  Automates music theory tasks for use in Ableton Live.

---

## ⚙️ Prerequisites

- **System**: Linux (tested on Ubuntu, Python 3.9)
- **Software**: Ableton Live (Standard/Suite, or trial)
- **Dependencies**:
  - Python libraries:  
    `librosa==0.10.2`, `numpy==1.26.4`, `matplotlib==3.8.4`, `yt-dlp==2024.8.6`, `mido==1.3.2`, `soundfile`
  - System:  
    `ffmpeg`
  - Optional:  
    Free VSTs like *Vital*, *Helm*, or *Surge XT* for use in Ableton

---

## 🛠️ Installation

```bash
# Clone Repository
git clone https://github.com/your-username/midi-file-project.git
cd midi-file-project

# Set Up Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install librosa==0.10.2 numpy==1.26.4 matplotlib==3.8.4 yt-dlp==2024.8.6 mido==1.3.2 soundfile
sudo apt-get install ffmpeg

# Verify Installation
python3 -c "import librosa, numpy, matplotlib, yt_dlp, mido, soundfile; print('Dependencies OK')"
