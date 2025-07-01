import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, iirfilter


class ImprovedGuitarStringModel:
    def __init__(self, fs=44100):
        self.fs = fs

    def pluck(self, fundamental_freq, duration=2.0, velocity=1.0, palm_mute=False):
        """Improved Karplus-Strong synthesis based on real guitar analysis"""

        # IMPROVEMENT 1: More accurate delay line calculation
        delay_samples = int(np.round(self.fs / fundamental_freq))

        # IMPROVEMENT 2: Sharp attack transient (like real guitar - 0.6ms to peak)
        impulse_length = max(int(0.001 * self.fs), 10)  # 1ms sharp attack
        excitation = np.zeros(delay_samples)

        # Sharp initial impulse (mimics pick hitting string)
        impulse = np.zeros(impulse_length)
        impulse[0] = velocity * 5.0  # Sharp initial spike - INCREASED

        # Brief noisy transient following the impulse
        for i in range(1, impulse_length):
            impulse[i] = velocity * 0.8 * np.random.uniform(-1, 1) * np.exp(-i * 0.02)  # INCREASED

        # High-frequency emphasis for pick attack realism
        b_attack, a_attack = butter(2, 0.8, btype='high')
        impulse = lfilter(b_attack, a_attack, impulse)

        # Initialize delay line
        excitation[:len(impulse)] = impulse
        delay_line = excitation.copy()

        # Calculate total samples
        total_samples = int(duration * self.fs)
        output = np.zeros(total_samples)

        # IMPROVEMENT 3: Frequency-dependent damping (realistic decay)
        freq_factor = fundamental_freq / 100.0
        base_damping = 0.15 if palm_mute else 0.9995
        high_freq_damping = base_damping - freq_factor * 0.0001  # Higher frequencies decay faster
        low_freq_damping = base_damping + freq_factor * 0.00005  # Lower frequencies sustain more

        # IMPROVEMENT 4: Multi-stage decay envelope
        # Fast initial decay (like real guitar: 76.6 dB/second)
        initial_decay_rate = 0.9992 if palm_mute else 0.9998
        sustain_decay_rate = 0.9999 if palm_mute else 0.99995
        transition_samples = int(0.05 * self.fs)  # Switch to sustain mode after 50ms

        # IMPROVEMENT 5: Body resonance filters (formants)
        # Real acoustic guitar body resonances
        body_freqs = [85, 150, 200, 250]  # Hz - typical guitar body resonances
        body_filters = []
        for freq in body_freqs:
            if freq < self.fs / 2:
                # Resonant peak filter
                Q = 8.0
                w = 2 * np.pi * freq / self.fs
                b_res, a_res = iirfilter(2, [freq * 0.9, freq * 1.1],
                                         btype='band', ftype='butter', fs=self.fs)
                body_filters.append((b_res, a_res))

        delay_pos = 0
        last_filtered = 0
        body_states = [np.zeros(len(a_res) - 1) for _ in body_filters]  # Filter memory

        for i in range(total_samples):
            # Get current sample
            current_sample = delay_line[delay_pos]

            # Add subtle string noise (much less than original)
            if np.random.rand() < 0.0001:  # Very rare
                current_sample += np.random.uniform(-0.05, 0.05) * velocity

            output[i] = current_sample

            # Next sample for KS averaging
            next_pos = (delay_pos + 1) % delay_samples
            next_sample = delay_line[next_pos]

            # Karplus-Strong filtering with improvements
            averaged = 0.5 * (current_sample + next_sample)

            # Frequency-dependent low-pass filtering
            lp_coeff = 0.6 if fundamental_freq > 200 else 0.8  # Higher notes need more filtering
            filtered = lp_coeff * averaged + (1 - lp_coeff) * last_filtered

            # IMPROVEMENT 6: Multi-stage decay based on time
            if i < transition_samples:
                # Fast initial decay phase
                current_damping = initial_decay_rate
            else:
                # Sustain phase with slower decay
                current_damping = sustain_decay_rate

            # Apply frequency-dependent damping variation
            if fundamental_freq > 150:
                current_damping *= high_freq_damping
            else:
                current_damping *= low_freq_damping

            damped = current_damping * filtered

            delay_line[delay_pos] = damped
            last_filtered = filtered
            delay_pos = (delay_pos + 1) % delay_samples

        # IMPROVEMENT 7: Enhanced body resonance
        output = self._add_enhanced_body_resonance(output, fundamental_freq, body_filters, body_states)

        # IMPROVEMENT 8: Enhanced harmonics with inharmonicity
        output = self._add_realistic_harmonics(output, fundamental_freq)

        # IMPROVEMENT 9: Realistic DI processing
        output = self._enhanced_di_processing(output)

        # Normalize with headroom - INCREASED VOLUME
        if np.max(np.abs(output)) > 0:
            output = output / np.max(np.abs(output)) * 0.95  # Higher normalization level

        return output

    def _add_enhanced_body_resonance(self, signal, fundamental_freq, body_filters, body_states):
        """Add realistic guitar body resonances using multiple formant filters"""
        t = np.arange(len(signal)) / self.fs

        # Apply body resonance filters
        resonant_signal = signal.copy()
        for i, (b_res, a_res) in enumerate(body_filters):
            # Filter the signal through each body resonance
            filtered_component = lfilter(b_res, a_res, signal)
            # Scale based on proximity to fundamental
            body_freq = [85, 150, 200, 250][i]
            proximity = np.exp(-abs(fundamental_freq - body_freq) / 50.0)
            resonant_signal += filtered_component * 0.15 * proximity  # INCREASED

        # IMPROVEMENT: Add realistic harmonics with proper amplitudes
        for n in [2, 3, 4, 5]:
            if fundamental_freq * n < self.fs / 2:
                # More realistic harmonic amplitude scaling
                harm_amp = 0.035 * (1.0 / n ** 1.2)  # Natural harmonic decay - INCREASED
                # Add slight inharmonicity (real strings aren't perfectly harmonic)
                stretch_factor = 1 + (n - 1) * 0.0002  # Stretch tuning effect
                harmonic_freq = fundamental_freq * n * stretch_factor

                # Harmonic with natural envelope
                harmonic = harm_amp * np.sin(2 * np.pi * harmonic_freq * t)
                # Harmonics decay faster than fundamental
                decay_rate = 0.8 + 0.1 * n
                harmonic *= np.exp(-t * decay_rate)
                resonant_signal += harmonic

        return resonant_signal

    def _add_realistic_harmonics(self, signal, fundamental_freq):
        """Add enhanced harmonic content with realistic characteristics"""
        t = np.arange(len(signal)) / self.fs

        # Enhance existing harmonics and add missing ones
        enhanced = signal.copy()

        # Add formant-like resonances typical of guitar
        formant_freqs = [100, 160, 250, 350]  # Typical guitar formants
        for f_freq in formant_freqs:
            if f_freq < self.fs / 2:
                formant_amp = 0.05 * np.exp(-abs(fundamental_freq - f_freq) / 80.0)  # INCREASED
                formant = formant_amp * np.sin(2 * np.pi * f_freq * t)
                formant *= np.exp(-t * 1.2)  # Formants decay
                enhanced += formant

        return enhanced

    def _enhanced_di_processing(self, signal):
        """More realistic DI box simulation"""
        # High-pass filter (typical DI input impedance effect)
        b_hp, a_hp = butter(1, 30, 'hp', fs=self.fs)
        signal = lfilter(b_hp, a_hp, signal)

        # Subtle saturation modeling (tube DI or preamp)
        drive = 1.002  # REDUCED to prevent volume loss
        signal = np.tanh(signal * drive) * 0.98  # INCREASED output level

        # Add very subtle electrical noise (60Hz hum + high freq noise)
        hum_freq = 60  # Hz
        t = np.arange(len(signal)) / self.fs
        hum = 0.00008 * np.sin(2 * np.pi * hum_freq * t)

        # High frequency noise (cable/electronics)
        noise_level = 0.00005
        hf_noise = noise_level * np.random.normal(0, 1, len(signal))
        b_hf, a_hf = butter(2, 0.8, 'high')
        hf_noise = lfilter(b_hf, a_hf, hf_noise)

        signal += hum + hf_noise

        return signal


# Usage example with improvements
def main():
    fs = 44100
    guitar = ImprovedGuitarStringModel(fs)

    print("Generating improved guitar notes...")

    # Test the Bb note that matches your sample
    Bb1 = 58.27  # Actual Bb1 frequency

    # Generate with different velocities and techniques
    soft_note = guitar.pluck(Bb1, duration=2.0, velocity=0.3)
    medium_note = guitar.pluck(Bb1, duration=2.0, velocity=0.7)
    hard_note = guitar.pluck(Bb1, duration=1.5, velocity=1.0)
    muted_note = guitar.pluck(Bb1, duration=1.0, velocity=0.8, palm_mute=True)

    # Create a sequence
    silence = np.zeros(int(0.3 * fs))

    improved_output = np.concatenate([
        soft_note,
        silence,
        medium_note,
        silence,
        hard_note,
        silence,
        muted_note
    ])

    print(f"Generated {len(improved_output) / fs:.1f} seconds of improved audio")
    print("Key improvements:")
    print("- Sharp attack transient (0.6ms like real guitar)")
    print("- Accurate frequency tuning")
    print("- Multi-stage decay (fast initial, slow sustain)")
    print("- Body resonance filters")
    print("- Enhanced harmonics with inharmonicity")
    print("- Realistic DI processing")

    # Save the improved version
    sf.write('improved_guitar_realistic.wav', improved_output, fs)
    print("Saved: improved_guitar_realistic.wav")


if __name__ == "__main__":
    main()
