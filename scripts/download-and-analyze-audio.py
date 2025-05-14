import os
import subprocess
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import time
import soundfile as sf
import json

def download_audio(query, output_name, max_retries=3):
    mp3_path = f"{output_name}.mp3"
    abs_mp3_path = os.path.abspath(mp3_path)
    if os.path.exists(abs_mp3_path):
        print(f"{mp3_path} already exists, skipping download.")
        return abs_mp3_path
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Downloading: {query} (Attempt {attempt}/{max_retries})")
            result = subprocess.run([
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "--audio-quality", "0",
                f"ytsearch:{query}",
                "--match-filter", "duration <= 600",
                "-o", mp3_path
            ], check=True, capture_output=True, text=True)
            time.sleep(2)
            if os.path.exists(abs_mp3_path):
                print(f"Downloaded: {mp3_path}")
                return abs_mp3_path
            else:
                print(f"Error: {mp3_path} not found after download.")
                return None
        except subprocess.CalledProcessError as e:
            print(f"Error downloading '{query}': {e.stderr.strip()}")
            if attempt < max_retries:
                print(f"Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Failed after {max_retries} attempts.")
                return None
        except FileNotFoundError:
            print("Error: 'yt-dlp' not found.")
            return None

def estimate_key(chroma):
    # Chroma to pitch class mapping
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # Sum chroma across time to get pitch class distribution
    chroma_sum = np.sum(chroma, axis=1)
    # Find strongest pitch class
    tonic_idx = np.argmax(chroma_sum)
    tonic = pitch_classes[tonic_idx]
    # Simple heuristic: Assume minor key for techno (can be improved)
    return f"{tonic} minor"

def analyze_audio(audio_path, track_name, analysis_results):
    try:
        y, sr = librosa.load(audio_path)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, start_bpm=120, tightness=100)
        tempo = tempo.item()
        print(f"{track_name} - Estimated tempo: {tempo:.2f} BPM")
        
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        key = estimate_key(chroma)
        print(f"{track_name} - Estimated key: {key}")
        
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', sr=sr)
        plt.colorbar()
        plt.title(f'{track_name} - Chroma Features (Pitch Classes)')
        plt.tight_layout()
        chroma_plot = f'{track_name}_chroma_plot.png'
        plt.savefig(chroma_plot)
        plt.close()
        print(f"Saved chroma plot: {chroma_plot}")
        
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        times = librosa.times_like(onset_env, sr=sr)
        plt.figure(figsize=(10, 4))
        plt.plot(times, onset_env, label='Onset Strength')
        plt.title(f'{track_name} - Rhythmic Onsets')
        plt.xlabel('Time (s)')
        plt.ylabel('Strength')
        plt.legend()
        onset_plot = f'{track_name}_onset_plot.png'
        plt.savefig(onset_plot)
        plt.close()
        print(f"Saved onset plot: {onset_plot}")
        
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        harmonic_wav = f'{track_name}_harmonic.wav'
        percussive_wav = f'{track_name}_percussive.wav'
        sf.write(harmonic_wav, y_harmonic, sr)
        sf.write(percussive_wav, y_percussive, sr)
        print(f"Saved harmonic WAV: {harmonic_wav}")
        print(f"Saved percussive WAV: {percussive_wav}")
        
        analysis_results[track_name] = {"tempo": tempo, "key": key}
    except Exception as e:
        print(f"Error analyzing '{track_name}': {e}")

def main():
    tracks = [
        ("Serial Experiments Lain Sountrack - 2nd Layer Cyberia Club", "cyberia_layer_2"),
        ("Duvet Boa Serial F Lain Official", "duvet"),
        ("Big in Japan Alphaville Official", "big_in_japan")
    ]
    analysis_results = {}
    
    for query, output_name in tracks:
        print(f"\nProcessing: {query}")
        mp3_path = download_audio(query, output_name)
        
        if mp3_path and os.path.exists(mp3_path):
            print(f"Analyzing: {mp3_path}")
            analyze_audio(mp3_path, output_name, analysis_results)
        else:
            print(f"Skipping analysis for '{query}' due to missing MP3.")
    
    with open("analysis_results.json", "w") as f:
        json.dump(analysis_results, f, indent=4)
    print("Saved analysis results to analysis_results.json")

if __name__ == "__main__":
    main()