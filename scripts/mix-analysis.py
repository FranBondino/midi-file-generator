import librosa
import numpy as np
import matplotlib.pyplot as plt
import json
import os

def load_analysis_results():
    if not os.path.exists("analysis_results.json"):
        print("Error: analysis_results.json not found.")
        return {}
    with open("analysis_results.json", "r") as f:
        return json.load(f)

def analyze_mix(wav_path, track_name, tempo):
    try:
        y, sr = librosa.load(wav_path, sr=44100)
        fft = np.abs(librosa.stft(y))
        freqs = librosa.fft_frequencies(sr=sr)
        avg_spectrum = np.mean(fft, axis=1)
        
        plt.figure(figsize=(10, 4))
        plt.semilogx(freqs, 20 * np.log10(avg_spectrum + 1e-6))
        plt.title(f'{track_name} Mix Frequency Balance (Tempo: {tempo:.2f} BPM)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.xlim(20, 20000)
        plt.grid(True)
        # Highlight techno-critical ranges
        plt.axvspan(50, 100, alpha=0.2, color='red', label='Kick (50-100 Hz)')
        plt.axvspan(100, 200, alpha=0.2, color='blue', label='Bass (100-200 Hz)')
        plt.axvspan(2000, 5000, alpha=0.2, color='green', label='Leads (2-5 kHz)')
        plt.legend()
        output_path = f'{track_name}_mix_balance.png'
        plt.savefig(output_path)
        plt.close()
        print(f'Saved mix balance plot: {output_path}')
        
        # Basic feedback
        low_energy = np.mean(avg_spectrum[(freqs >= 50) & (freqs <= 200)])
        mid_energy = np.mean(avg_spectrum[(freqs >= 500) & (freqs <= 5000)])
        if low_energy > mid_energy * 1.5:
            print(f'Warning: {track_name} mix may be too bass-heavy. Consider cutting 100-200 Hz.')
        elif mid_energy > low_energy * 1.5:
            print(f'Warning: {track_name} mix may lack low-end. Boost kick/bass at 50-100 Hz.')
    except Exception as e:
        print(f'Error analyzing {wav_path}: {e}')

def main():
    analysis_results = load_analysis_results()
    
    tracks = [
        ("cyberia_layer_2", "E minor"),
        ("duvet", "B minor"),
        ("big_in_japan", "G# minor")
    ]
    
    for track_name, _ in tracks:
        wav_path = f'{track_name}_mix.wav'
        if not os.path.exists(wav_path):
            print(f'Warning: {wav_path} not found. Export mix from Ableton.')
            continue
        tempo = analysis_results.get(track_name, {}).get("tempo", 128)
        print(f'Analyzing mix for {track_name} with tempo {tempo:.2f} BPM')
        analyze_mix(wav_path, track_name, tempo)

if __name__ == "__main__":
    main()