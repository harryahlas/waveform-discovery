import numpy as np


from scipy.io.wavfile import write

# Parameters
sample_rate = 44100  # Samples per second
duration = 2.0       # Duration of the note in seconds
frequency = 440.0    # Frequency of the note (A4 in this case)

# Calculate the number of samples
num_samples = int(sample_rate * duration)

# Calculate the delay line length
delay_line_length = int(sample_rate / frequency)

# Initialize the delay line with random noise
delay_line = np.random.uniform(-1, 1, delay_line_length)

# Initialize the output array
output = np.zeros(num_samples)

# Karplus-Strong loop
for i in range(num_samples):
    # The current sample is the average of the first two samples in the delay line
    output[i] = delay_line[0]
    avg = 0.5 * (delay_line[0] + delay_line[1])
    # Shift the delay line and apply the damping factor
    delay_line[:-1] = delay_line[1:]
    delay_line[-1] = avg * 0.996  # Damping factor to simulate energy loss

# Normalize the output to the range of int16
output = np.int16(output / np.max(np.abs(output)) * 32767)

# Write the output to a WAV file
write("plucked_string.wav", sample_rate, output)

import os

os.getcwd()
