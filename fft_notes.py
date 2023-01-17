import numpy as np
import sounddevice as sd
import scipy.fftpack as fft
from notes import note_mapping

# Define the sample rate and duration of the recording
sample_rate = 44100
duration = 5

# Record audio from the microphone
recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
print('start ...')
sd.wait()
print('stop')

# Apply the FFT to the recording
fft_output = fft.fft(recording[:, 0])

# Find the dominant frequencies
magnitude = np.abs(fft_output)
max_freq = np.argmax(magnitude)
dominant_freq = max_freq * sample_rate / len(recording[:, 0])

note = None
min_diff = float('inf')
for key, value in note_mapping.items():
    diff = abs(dominant_freq - value)
    if diff < min_diff:
        min_diff = diff
        note = key

print(min_diff)
# Output the detected musical note
print("The detected musical note is:", note)
