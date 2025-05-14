import mido
from mido import MidiFile, MidiTrack, Message
import json
import os

def create_midi(filename, notes, tempo=128):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=int(60000000/tempo)))
    track.append(Message('program_change', program=1, time=0))
    ticks_per_beat = 480
    for note, duration in notes:
        track.append(Message('note_on', note=note, velocity=80, time=0))
        track.append(Message('note_off', note=note, velocity=80, time=int(duration * ticks_per_beat)))
    mid.save(filename)
    print(f"MIDI file '{filename}' generated!")

def load_analysis_results():
    if not os.path.exists("analysis_results.json"):
        print("Error: analysis_results.json not found. Run download_and_analyze_audio.py first.")
        return {}
    with open("analysis_results.json", "r") as f:
        return json.load(f)

def get_scale(key):
    scales = {
        "C minor": [60, 62, 63, 65, 67, 68, 70],  # C4, D4, E♭4, F4, G4, A♭4, B♭4
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
    return scales.get(key, scales["C minor"])  # Fallback

def generate_techno_patterns(track_name, tempo, key):
    scale = get_scale(key)
    tempo = tempo if tempo else 128
    
    motif = [
        (scale[0], 0.125),  # Root
        (scale[2], 0.125),  # Third
        (scale[4], 0.125),  # Fifth
        (0, 0.125),         # Rest
        (scale[3], 0.125),  # Fourth
        (scale[4], 0.125),
        (scale[2], 0.125),
        (0, 0.125)
    ]
    
    bass = [
        (scale[0] - 24, 0.25),  # Root, two octaves down
        (0, 0.125),             # Rest
        (scale[0] - 24, 0.125),
        (scale[2] - 24, 0.25),  # Third
        (0, 0.25)
    ]
    
    chords = [
        (scale[0], 1.0),  # Root (i)
        (scale[2], 1.0),  # Third
        (scale[4], 1.0),  # Fifth
        (scale[3], 1.0),  # Root (iv)
        (scale[5], 1.0),  # Third
        (scale[0], 1.0)   # Fifth
    ]
    
    return motif, bass, chords

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
        print(f"Generating MIDI for {track_name} with tempo {tempo:.2f} BPM and key {key}")
        
        motif, bass, chords = generate_techno_patterns(track_name, tempo, key)
        create_midi(f"{track_name}_motif.mid", motif, tempo)
        create_midi(f"{track_name}_bass.mid", bass, tempo)
        create_midi(f"{track_name}_chords.mid", chords, tempo)

if __name__ == "__main__":
    main()