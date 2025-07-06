import math
import wave
import struct
import matplotlib.pyplot as plt

# ==========================
# Configuration Parameters
# ==========================

sample_rate = 44100        # CD-quality
duration = 0.2             # 200 ms for a closed hi-hat
num_samples = int(sample_rate * duration)
decay_rate = 0.001         # Envelope decay rate

# ==========================
# LFSR Noise Generator
# ==========================

def lfsr(seed=0xACE1, taps=(16, 14, 13, 11)):
    lfsr_state = seed
    while True:
        xor = 0
        for t in taps:
            xor ^= (lfsr_state >> (t - 1)) & 1
        lfsr_state = ((lfsr_state << 1) & 0xFFFF) | xor
        yield (lfsr_state & 0xFF) - 128  # Centered around 0

# ==========================
# Envelope Generator
# ==========================

def generate_envelope(length, decay_rate):
    return [math.exp(-decay_rate * n) for n in range(length)]

# ==========================
# Signal Generation
# ==========================

# Generate noise and envelope
noise_gen = lfsr()
envelope = generate_envelope(num_samples, decay_rate)
noise_samples = [next(noise_gen) for _ in range(num_samples)]

# Apply envelope to noise
final_output = [
    max(-32767, min(32767, int(noise_samples[i] * envelope[i] * 256)))
    for i in range(num_samples)
]

# ==========================
# WAV File Export
# ==========================

def write_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for s in samples:
            wav_file.writeframes(struct.pack('<h', s))

write_wav("simple_hi_hat.wav", final_output)
