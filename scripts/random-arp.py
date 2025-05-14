import mido
from mido import MidiFile, MidiTrack, Message
import random
import json
import os

def create_random_arp(filename, scale, tempo=128, length=32):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=int(60000000/tempo)))
    track.append(Message('program_change', program=1, time=0))
    ticks_per_beat = 480
    
    for _ in range(length):
        note = random.choice(scale)
        duration = random.choice([0.0625, 0.125, 0.25])  # Sixteenth, eighth, quarter
        velocity = random.randint(60, 90)  # Varied dynamics
        track.append(Message('note_on', note=note, velocity=velocity, time=0))
        track.append(Message('note_off', note=note, velocity=velocity, time=int(duration * ticks_per_beat)))
        # Add occasional rests for syncopation
        if random.random() < 0.2:
            track.append(Message('note_on', note=0, velocity=0, time=int(0.0625 * ticks_per_beat)))
    
    mid.save(filename)
    print(f"Random arp MIDI '{filename}' generated!")

def load_analysis_results():
    if not os.path.exists("analysis_results.json"):
        print("Error: analysis_results.json not found.")
        return {}
    with open("analysis_results.json", "r") as f:
        return json.load(f)

def get_scale(key):
    scales = {
        "C minor": [60, 62, 63, 65, 67, 68, 70],
        "C# minor": [61, 63, 64, 66, 68, 69, 71],
        "D minor": [62, 64, 65, 67, 69, 70, 72],
        "D# minor": [63, 65, 66, 68, 70, 71, 73],
        "E minor": [64, 66, 67, 69, 71, 72, 74],  # E4, F#4, G4, A4, B4, C5, D5
        "F minor": [65, 67, 68, 70, 72, 73, 75],
        "F# minor": [66, 68, 69, 71, 73, 74, 76],
        "G minor": [67, 69, 70, 72, 74, 75, 77],
        "G# minor": [68, 70, 71, 73, 75, 76, 78],  # G#4, A#4, B4, C#5, D#5, E5, F#5
        "A minor": [69, 71, 72, 74, 76, 77, 79],
        "A# minor": [70, 72, 73, 75, 77, 78, 80],
        "B minor": [71, 73, 74, 76, 78, 79, 81]   # B4, C#5, D5, E5, F#5, G5, A5
    }
    return scales.get(key, scales["E minor"])  # Fallback

def main():
    analysis_results = load_analysis_results()
    
    tracks = [
        ("cyberia_layer_2", "E minor"),
        ("duvet", "B minor"),
        ("big_in_japan", "G# minor")
    ]
    
    for track_name, default_key in tracks:
        result = analysis_results.get(track_name, {})
        tempo = result.get("tempo", 128)
        key = result.get("key", default_key)
        scale = get_scale(key)
        print(f"Generating random arp for {track_name} with tempo {tempo:.2f} BPM and key {key}")
        create_random_arp(f"{track_name}_random_arp.mid", scale, tempo)

if __name__ == "__main__":
    main()