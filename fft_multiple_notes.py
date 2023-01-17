import numpy as np
import sounddevice as sd
import scipy.fftpack as fft
import scipy.signal as signal
from notes import note_mapping

# Define the sample rate and duration of the recording
sample_rate = 44100
duration = 0.1  # Change the duration of the recording to capture multiple notes

# Create a list to store the detected notes
detected_notes = []

def callback(indata, frames, time, status):
    if np.max(indata) > 0:  # check if there is any sound
        # Apply the Wiener filter to the recording
        filtered_data = signal.wiener(indata[:, 0])

        # Apply the FFT to the filtered recording
        fft_output = fft.fft(filtered_data)

        # Find the dominant frequencies
        magnitude = np.abs(fft_output)
        max_freq = np.argmax(magnitude)
        dominant_freq = max_freq * sample_rate / len(filtered_data)

        # Map the dominant frequency to a musical note
        note = None
        min_diff = float('inf')
        for key, value in note_mapping.items():
            diff = abs(dominant_freq - value)
            if diff < min_diff:
                min_diff = diff
                note = key
        detected_notes.append(note)
        print(note)
    else:
        print("waiting for note...")
    

stream = sd.InputStream(callback=callback,
                       channels=1,
                       samplerate=sample_rate,
                       blocksize=int(sample_rate * 0.1),
                       dtype=np.float32,
                       latency='low')
with stream:
    sd.sleep(50000)
  
print(detected_notes)
