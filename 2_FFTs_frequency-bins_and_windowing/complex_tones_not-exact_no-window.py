import numpy as np
import matplotlib.pyplot as plt

# Create three complex tones, add them together, and recover their frequencies.
# This time, have leakage in 2 using random.

# [CONFIG] ====================================================================

# How many maxima we want to find
maxima = 5

# Fs must live above Nyquist
Fs = 16 # Hz

N = 32 # Pts to simulate

# Complex tone 1 config
f1 = Fs/N # Hz

# Complex tone 2 config
f2 = np.random.uniform(-3,3) # Hz

# Complex tone 3 config
f3 = np.random.uniform(-3,3) # Hz


# [END CONFIG]



# [SIMULATION] ================================================================
n = np.arange(N)
t = n/Fs;
f = np.arange(-Fs/2, Fs/2, Fs/N)

x1 = np.exp(1j * 2 * np.pi * f1 * t)
x1_fft = np.fft.fftshift(np.fft.fft(x1))

x2 = np.exp(1j * 2 * np.pi * f2 * t)
x2_fft = np.fft.fftshift(np.fft.fft(x2))

x3 = np.exp(1j * 2 * np.pi * f3 * t)
x3_fft = np.fft.fftshift(np.fft.fft(x3))

S = x1_fft + x2_fft + x3_fft;
S_mags = np.abs(S);


# Recover frequencies, not in order, by finding greatest points.
# Explicit solving only works if we know the qty of signals.
# Otherwise, we can find the n greatest points and compare graphically.

top_indices = np.argsort(S_mags)[-maxima:][::-1]
top_freqs = f[top_indices]
print(f"Top {maxima} frequencies observed (descending magnitude):\n{top_freqs}\n")
print(f"Corresponding magnitudes:\n{S_mags[top_indices]}\n")
# [END SIMULATION]



# [PLOTTING] ==================================================================
# Set up frequency array for plotting
# f established in simulation for recovery purposes

# Set up linear and normalized dB magnitude plots
S_db = 20 * np.log10(S_mags / np.max(S_mags) + 1e-12)

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax_magnitude, ax_db = axes

ax_magnitude.plot(f, S_mags, '.-')
ax_magnitude.set_ylabel('FFT Magnitude')
ax_magnitude.grid(True)

ax_db.plot(f, S_db, '.-')
ax_db.set_xlabel('Frequency [Hz]')
ax_db.set_ylabel('Normalized Magnitude [dB]')
ax_db.set_ylim(-80, 5)
ax_db.grid(True)

plt.tight_layout()
plt.show()

# [END PLOTTING]
