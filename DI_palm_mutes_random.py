import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter


class GuitarStringModel:
    def __init__(self, fs=44100):
        self.fs = fs

    def pluck(self, fundamental_freq, duration=2.0, velocity=1.0, palm_mute=False):
        """Improved Karplus-Strong string synthesis"""

        # Calculate delay line length for fundamental frequency
        delay_samples = int(self.fs / fundamental_freq)

        # Create initial excitation - burst of filtered noise
        excitation_length = max(delay_samples, 100)
        excitation = np.random.uniform(-1, 1, excitation_length) * velocity

        # Shape the excitation with a quick decay to simulate pick attack
        attack_env = np.exp(-np.arange(excitation_length) / (excitation_length * 0.1))
        excitation *= attack_env

        # Initialize delay line with excitation
        delay_line = np.zeros(delay_samples)
        delay_line[:min(len(excitation), delay_samples)] = excitation[:delay_samples]

        # Calculate total samples needed
        total_samples = int(duration * self.fs)
        output = np.zeros(total_samples)

        # Damping factor - closer to 1.0 for longer sustain
        if palm_mute:
            damping = 0.1  # More damping for palm mute
        else:
            damping = 0.9985  # Less damping for sustained notes

        # Low-pass filter coefficients for string damping
        # Simple one-pole filter: y[n] = a*x[n] + (1-a)*y[n-1]
        lp_coeff = 0.5  # Adjust for brightness (0.1 = dark, 0.9 = bright)

        # Process samples in chunks for efficiency
        chunk_size = 1024
        delay_pos = 0
        last_filtered = 0

        for start_idx in range(0, total_samples, chunk_size):
            end_idx = min(start_idx + chunk_size, total_samples)
            chunk_length = end_idx - start_idx

            for i in range(chunk_length):
                # Get current sample from delay line
                current_sample = delay_line[delay_pos]
                output[start_idx + i] = current_sample

                # Get next sample for averaging (Karplus-Strong filtering)
                next_pos = (delay_pos + 1) % delay_samples
                next_sample = delay_line[next_pos]

                # Apply Karplus-Strong filter: average + damping + low-pass
                averaged = 0.5 * (current_sample + next_sample)
                filtered = lp_coeff * averaged + (1 - lp_coeff) * last_filtered
                damped = damping * filtered

                # Put filtered sample back into delay line
                delay_line[delay_pos] = damped
                last_filtered = filtered

                # Advance delay line position
                delay_pos = next_pos

        # Add some subtle harmonics and body resonance
        output = self._add_body_resonance(output, fundamental_freq)

        # Simple DI-style processing
        output = self._di_processing(output)

        # Normalize
        if np.max(np.abs(output)) > 0:
            output = output / np.max(np.abs(output)) * 0.8

        return output

    def _add_body_resonance(self, signal, fundamental_freq):
        """Add subtle body resonance and harmonics"""
        # Add some second harmonic
        t = np.arange(len(signal)) / self.fs
        harmonic2 = 0.1 * np.sin(2 * np.pi * fundamental_freq * 2 * t)
        harmonic2 *= np.exp(-t * 0.5)  # Decay envelope

        # Simple body resonance around 100-200 Hz
        body_freq = 150.0
        body_resonance = 0.05 * np.sin(2 * np.pi * body_freq * t)
        body_resonance *= np.exp(-t * 2.0)  # Quick decay

        return signal + harmonic2[:len(signal)] + body_resonance[:len(signal)]

    def _di_processing(self, signal):
        """Simple DI box simulation"""
        # Gentle high-pass to remove DC
        b, a = butter(2, 40, 'hp', fs=self.fs)
        signal = lfilter(b, a, signal)

        # Very subtle saturation
        signal = np.tanh(signal * 1.2) * 0.9

        return signal


# Usage example
def main():
    fs = 44100
    guitar = GuitarStringModel(fs)

    print("Generating guitar notes...")

    # Generate different notes
    E2 = 82.41  # Low E
    A2 = 110.0  # A string
    D3 = 146.83  # D string

    # Create a sequence of notes
    clean_note = guitar.pluck(E2, duration=0.4, velocity=0.3)
    clean_note2 = guitar.pluck(E2, duration=1.0, velocity=0.8)
    muted_note = guitar.pluck(A2, duration=1.5, velocity=0.6, palm_mute=True)
    higher_note = guitar.pluck(D3, duration=2.0, velocity=0.1)

    # Add some silence between notes
    silence = np.zeros(int(0.2 * fs))

    # Concatenate the sequence
    output = np.concatenate([
        clean_note, #silence,
        clean_note2, silence,
        muted_note, silence,
        higher_note
    ])

    print(f"Generated {len(output) / fs:.1f} seconds of audio")
    print("Saving to enhanced_guitar_di.wav...")

    # Save the result
    sf.write('D:\github\AudiblePlanets\enhanced_guitar_di3.wav', output, fs)
    print("Done!")


if __name__ == "__main__":
    main()

