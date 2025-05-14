import librosa
import matplotlib.pyplot as plt

y, sr = librosa.load("mix.wav")
centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
times = librosa.times_like(centroid, sr=sr)
plt.plot(times, centroid[0])
plt.title('Spectral Centroid (Frequency Balance)')
plt.savefig('mix_balance.png')