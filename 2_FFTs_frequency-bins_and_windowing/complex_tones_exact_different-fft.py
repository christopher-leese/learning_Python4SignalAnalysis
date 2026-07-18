import numpy as np
import matplotlib.pyplot as plt

# Create two complex tones, add them together, and recover their frequencies.
# Different FFT sizes

# [CONFIG] ====================================================================

# How many maxima we want to find
maxima = 5

# Fs must live above Nyquist
Fs = 16 # Hz

N = 32 # Pts to sample

# Complex tone 1 config
f1 = 1 # Hz

# Complex tone 2 config
f2 = 2.25 # Hz, halfway between 32pt FFT bins

fft_len_1 = 32
fft_len_2 = 128

# [END CONFIG]



# [SIMULATION] ================================================================
n = np.arange(N)
t = n/Fs
f = np.arange(-Fs/2, Fs/2, Fs/N)

x1 = np.exp(1j * 2 * np.pi * f1 * t)
x2 = np.exp(1j * 2 * np.pi * f2 * t)

s = x1 + x2

S1 = np.fft.fftshift(np.fft.fft(s, n=fft_len_1))
S2 = np.fft.fftshift(np.fft.fft(s, n=fft_len_2))

# Set up frequencies for x axis on plotting
freqs1 = np.fft.fftshift(
    np.fft.fftfreq(fft_len_1, d=1/Fs)
)

freqs2 = np.fft.fftshift(
    np.fft.fftfreq(fft_len_2, d=1/Fs)
)

# [END SIMULATION]



# [PLOTTING] ==================================================================
# Set up frequency array for plotting, two subplots showcasing diff FFT sizes

fig, axes = plt.subplots(2, 1, figsize=(10, 8))

axes[0].plot(freqs1, np.abs(S1), '.-')
axes[0].set_title('32-point FFT')
axes[0].grid(True)

axes[1].plot(freqs2, np.abs(S2), '.-')
axes[1].set_title('128-point FFT of the same 32 samples')
axes[1].set_xlabel('Frequency [Hz]')
axes[1].grid(True)

plt.tight_layout()
plt.show()

# [END PLOTTING]
