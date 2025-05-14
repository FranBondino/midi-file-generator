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

def generate_techno_patterns(track_name, tempo, key):
    # Define scales (MIDI note numbers)
    scales = {
        "C minor": [60, 62, 63, 65, 67, 68, 70],  # C4, D4, E♭4, F4, G4, A♭4, B♭4
        "C# minor": [61, 63, 64, 66, 68, 69, 71],  # C#4, D#4, E4, F#4, G#4, A4, B4
        "A minor": [57, 59, 60, 62, 64, 65, 67]   # A3, B3, C4, D4, E4, F4, G4
    }
    
    # Default to 128 BPM if tempo not provided
    tempo = tempo if tempo else 128
    
    # Select scale based on track
    scale = scales.get(key, scales["C minor"])  # Fallback to C minor
    
    # Motif: Fast arpeggio for lead (eighth notes)
    motif = [
        (scale[0], 0.125),  # Root
        (scale[2], 0.125),  # Third
        (scale[4], 0.125),  # Fifth
        (scale[2], 0.125),
        (scale[0], 0.125),
        (scale[3], 0.125),  # Fourth
        (scale[4], 0.125),
        (scale[2], 0.125)
    ]
    
    # Bass: Offbeat, root-heavy (quarter notes)
    bass = [
        (scale[0] - 24, 0.25),  # Root, two octaves down
        (0, 0.25),              # Offbeat rest
        (scale[0] - 24, 0.25),
        (0, 0.25)
    ]
    
    # Chords: Sustained minor triads (whole notes)
    chords = [
        (scale[0], 1.0),  # Root
        (scale[2], 1.0),  # Third
        (scale[4], 1.0),  # Fifth
        (scale[3], 1.0),  # Fourth (for i–iv progression)
        (scale[5], 1.0),  # Sixth
        (scale[7] - 12, 1.0)  # Seventh, octave down
    ]
    
    return motif, bass, chords

def main():
    # Load analysis results
    analysis_results = load_analysis_results()
    
    # Define tracks with keys
    tracks = [
        ("cyberia_layer_2", "C minor"),
        ("duvet", "C# minor"),
        ("big_in_japan", "A minor")
    ]
    
    for track_name, key in tracks:
        # Get tempo from analysis or default to 128
        tempo = analysis_results.get(track_name, {}).get("tempo", 128)
        print(f"Generating MIDI for {track_name} with tempo {tempo:.2f} BPM and key {key}")
        
        # Generate patterns
        motif, bass, chords = generate_techno_patterns(track_name, tempo, key)
        
        # Create MIDI files
        create_midi(f"{track_name}_motif.mid", motif, tempo)
        create_midi(f"{track_name}_bass.mid", bass, tempo)
        create_midi(f"{track_name}_chords.mid", chords, tempo)

if __name__ == "__main__":
    main()