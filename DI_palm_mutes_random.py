import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter


class GuitarStringModel:
    def __init__(self, fs=44100):
        self.fs = fs

    def pluck(self, fundamental_freq, duration=2.0, velocity=1.0, palm_mute=False):
        """Improved Karplus-Strong string synthesis with added randomness"""

        # Calculate delay line length for fundamental frequency
        delay_samples = int(self.fs / fundamental_freq)

        # === Excitation with random filtered noise and random attack decay ===
        excitation_length = max(delay_samples, 100)

        # Random lowpass cutoff frequency for excitation noise (simulate pick hardness)
        cutoff = np.random.uniform(4000, 8000)  # Hz
        b, a = butter(2, cutoff / (self.fs / 2), btype='low')
        noise = np.random.uniform(-1, 1, excitation_length) * velocity
        excitation = lfilter(b, a, noise)

        # Randomize attack envelope decay rate slightly per pluck
        decay_rate = np.random.uniform(0.07, 0.13) * excitation_length
        attack_env = np.exp(-np.arange(excitation_length) / decay_rate)
        excitation *= attack_env

        # Initialize delay line with excitation
        delay_line = np.zeros(delay_samples)
        delay_line[:min(len(excitation), delay_samples)] = excitation[:delay_samples]

        # Calculate total samples needed
        total_samples = int(duration * self.fs)
        output = np.zeros(total_samples)

        # === Randomized damping and low-pass filter coefficients ===
        base_damping = 0.1 if palm_mute else 0.9985
        # Small random variation in damping
        damping = base_damping * np.random.uniform(0.995, 1.005)

        base_lp_coeff = 0.5
        lp_coeff = base_lp_coeff * np.random.uniform(0.95, 1.05)

        # Low frequency oscillator for subtle damping modulation
        lfo_freq = 0.1  # Hz
        lfo = 0.0002 * np.sin(2 * np.pi * lfo_freq * np.arange(total_samples) / self.fs)

        delay_pos = 0
        last_filtered = 0

        for start_idx in range(0, total_samples):
            # Get current sample from delay line
            current_sample = delay_line[delay_pos]

            # Add subtle random noise bursts to simulate finger/string noise
            noise_burst = 0
            if np.random.rand() < 0.00005:  # very rare noise burst
                noise_burst = np.random.uniform(-0.1, 0.1)

            output[start_idx] = current_sample + noise_burst

            # Next sample for averaging (Karplus-Strong filtering)
            next_pos = (delay_pos + 1) % delay_samples
            next_sample = delay_line[next_pos]

            # Apply Karplus-Strong filter: average + damping + low-pass + LFO modulation
            averaged = 0.5 * (current_sample + next_sample)
            filtered = lp_coeff * averaged + (1 - lp_coeff) * last_filtered

            # Modulate damping with slow LFO to simulate timbre fluctuations
            current_damping = damping + lfo[start_idx]
            current_damping = np.clip(current_damping, 0, 1)  # keep damping in reasonable range
            damped = current_damping * filtered

            delay_line[delay_pos] = damped
            last_filtered = filtered

            # Advance delay line position with slight vibrato modulation (fractional delay approximation)
            vibrato_depth = 0.0002  # fraction of delay length
            vibrato_freq = 5.0  # Hz
            vibrato_mod = vibrato_depth * np.sin(2 * np.pi * vibrato_freq * start_idx / self.fs)
            # Normally requires fractional delay interpolation.
            # Approximate by occasionally skipping or repeating a sample:
            if vibrato_mod > 0.001:
                delay_pos = (delay_pos + 2) % delay_samples
            elif vibrato_mod < -0.001:
                delay_pos = (delay_pos + 0) % delay_samples
            else:
                delay_pos = (delay_pos + 1) % delay_samples

        # === Add multiple harmonics with randomized amplitude and decay ===
        output = self._add_body_resonance(output, fundamental_freq)

        # === Simple DI processing with variable saturation and low-level hum ===
        output = self._di_processing(output)

        # Normalize output
        if np.max(np.abs(output)) > 0:
            output = output / np.max(np.abs(output)) * 0.8

        return output

    def _add_body_resonance(self, signal, fundamental_freq):
        """Add multiple harmonics and body resonance with randomness"""
        t = np.arange(len(signal)) / self.fs

        # Add 2nd to 4th harmonics with random amplitude and decay
        for n in [2, 3, 4]:
            amp = np.random.uniform(0.005, 0.012) / n
            decay = np.random.uniform(0.3, 0.6)
            harmonic = amp * np.sin(2 * np.pi * fundamental_freq * n * t)
            harmonic *= np.exp(-t * decay)
            signal += harmonic

        # Body resonance frequency and amplitude randomized slightly
        body_freq = np.random.uniform(140.0, 160.0)
        body_amp = np.random.uniform(0.03, 0.06)
        body_decay = np.random.uniform(1.5, 2.5)
        body_resonance = body_amp * np.sin(2 * np.pi * body_freq * t)
        body_resonance *= np.exp(-t * body_decay)
        signal += body_resonance

        return signal

    def _di_processing(self, signal):
        """Simple DI box simulation with variable saturation and low hum"""
        # High-pass filter to remove DC
        b, a = butter(2, 40, 'hp', fs=self.fs)
        signal = lfilter(b, a, signal)

        # Variable subtle saturation per run
        saturation_gain = np.random.uniform(1.001, 1.003)
        signal = np.tanh(signal * saturation_gain) * 0.9

        # Add low-level hum (50 Hz or 60 Hz)
        hum_freq = np.random.choice([50, 60])
        t = np.arange(len(signal)) / self.fs
        hum = 0.0001 * np.sin(2 * np.pi * hum_freq * t)
        signal += hum

        return signal


# Usage example
def main():
    fs = 44100
    guitar = GuitarStringModel(fs)

    print("Generating guitar notes...")

    E2 = 82.41  # Low E
    A2 = 110.0  # A string
    D3 = 146.83  # D string

    clean_note = guitar.pluck(E2, duration=0.4, velocity=0.3)
    clean_note2 = guitar.pluck(E2, duration=1.0, velocity=0.8)
    muted_note = guitar.pluck(A2, duration=1.5, velocity=0.6, palm_mute=True)
    higher_note = guitar.pluck(D3, duration=2.0, velocity=0.1)

    silence = np.zeros(int(0.2 * fs))

    output = np.concatenate([
        clean_note,
        silence,
        clean_note2,
        silence,
        muted_note,
        silence,
        higher_note
    ])

    print(f"Generated {len(output) / fs:.1f} seconds of audio")
    print("Saving to enhanced_guitar_di3.wav...")

    sf.write('D:\github\AudiblePlanets\enhanced_guitar_di6.wav', output, fs)
    print("Done!")


if __name__ == "__main__":
    main()

# sf.write('D:\github\AudiblePlanets\enhanced_guitar_di4.wav', output, fs)




