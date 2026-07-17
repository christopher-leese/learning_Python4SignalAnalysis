import numpy as np
import matplotlib.pyplot as plt

# [CONFIG] ====================================================================
# Assuming sample rate of 1Hz for simplicity
# Expect left bound to be -0.5Hz, right bound to be 0.5Hz
Fs = 1 # Hz
N = 100 # Pts to simulate & FFT size

# [END CONFIG] ================================================================



# [SIMULATION] ================================================================
# Set up time steps and sine simulation
t = np.arange(N)
s = np.sin(0.15*2*np.pi*t) # sine wave with 0.15 Hz frequency
# Find FFT, process FFT, and find FFT magnitude and phase
S_unshifted = np.fft.fft(s)
S = np.fft.fftshift(S_unshifted)
S_mag = np.abs(S)
S_phase = np.angle(S)

# [END SIMULATION] ============================================================



# [PLOTTING] ==================================================================
# Set up frequency array for plotting
f = np.arange(-Fs/2, Fs/2, Fs/N)

# Set up figures as two subplots
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
ax_magnitude, ax_phase= axes.flat

# Plot FFT magnitude vs frequency
ax_magnitude.grid(True)
ax_magnitude.set_ylabel('FFT Magnitude')
ax_magnitude.plot(f,S_mag,'.-')

# Plot FFT phase vs frequency
ax_phase.grid(True)
ax_phase.set_xlabel('Frequency [Hz]')
ax_phase.set_ylabel('FFT Phase [radians]')
ax_phase.plot(f,S_phase,'.-')
plt.show()

# [END PLOTTING] ==============================================================