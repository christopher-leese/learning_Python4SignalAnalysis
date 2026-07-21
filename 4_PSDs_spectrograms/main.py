from dataclasses import dataclass
from scipy.signal.windows import tukey

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Generate three bursts:
# - Different start times.
# - Different durations.
# - Different frequency offsets.
# 
# Produce a spectrogram where all three are visually identifiable.
# Then alter the window size and explain what improved and what degraded.

# model:
#   input service: expect 3 bursts with start, end, freq, T_min, hop_div, wq
#       T_min is the shortest duration of signal that we care about         
#           arbitrary 2-5 windows fitted inside, so Tw = T_min / wq
#           we adjust window qty depending on timing localization or freq res.
#           higher qty -> smaller window time -> stronger localization
#           lower qty -> greater window time -> better freq res
#       Hop divisor tells us how far we overlap. Good starter ones are:
#           N/2 (50%), N/4 (75%), and N/8 (87.5%)
#           ^ from least to greatest smoothness/computation
#
#       define @dataclass(frozen=True) class "Burst" with freq, start, end
#       write into array "signal" which is a defined-seconds recording
#       start is closed, end is open interval
#
#       Fs = 2048 # semi-arbitrary so smaller example frequencies < nyquist
#       recording_duration = 1 # seconds
#       qty_samples = int(fs * recording_duration)
#
#       x = np.zeros(qty_samples, dtype=np.complex128) # timeline
#
#       Burst s1(33, 0.1, 0.25)
#       Burst s2(10, 0.3, 0.5)
#       Burst s3(25, 0.6, 0.85)
#
#
#   simulation service:
#       set up ShortTimeFFT params:
#           Tw = T_min / wq
#           N = Fs*Tw
#           hop = N // hop_div
#
#       create ShortTimeFFT:
#           stft = signal.ShortTimeFFT.from_window(
#               "hann",
#               fs=Fs,
#               fft_mode='centered', # expecting complex signals
#               nperseg=N,
#               noverlap=N-hop,
#               scale_to="psd"
#           )
#       
#       Set up signals:
#       t = np.arange(num_samples) / fs
#
#       gate_1 = (t >= s1.start) & (t < s1.end)
#       x[gate_1] += np.exp(1j * 2 * np.pi * s1.freq * t[gate_1])
#
#       gate_2 = (t >= s2.start) & (t < s2.end)
#       x[gate_2] += np.exp(1j * 2 * np.pi * s2.freq * t[gate_2])
#
#       gate_3 = (t >= s3.start) & (t < s3.end)
#       x[gate_3] += np.exp(1j * 2 * np.pi * s3.freq * t[gate_3])
#               
#       power = stft.spectrogram(x) # shape of (frequency bins, time slices)
#       
#       power_db = 10 * np.log10(
#          np.maximum(Sxx, np.finfo(float).tiny)
#       )
#
#       freqs = stft.f
#       times = stft.t(len(x))
#
#   UI service:
#
#   print(f"Window length: {stft.m_num} samples")
#   print(f"Hop: {stft.hop} samples")
#   print(f"Overlap: {stft.m_num - stft.hop} samples")
#   print(f"Time-column spacing: {stft.delta_t} seconds")
#   print(f"Frequency-bin spacing: {stft.delta_f} Hz")
#
# duration_s = len(x) / Fs
# valid_time = (times >= 0.0) & (times <= duration_s)
# 
# times_plot = times[valid_time]
# power_db_plot = power_db[:, valid_time]
# 
# fig, ax = plt.subplots(figsize=(11, 5))
# 
# mesh = ax.pcolormesh(
#     times_plot,
#     freqs,
#     power_db_plot,
#     shading="auto",
# )
# 
# colorbar = fig.colorbar(mesh, ax=ax)
# colorbar.set_label("Power spectral density (dB/Hz)")
# 
# ax.set_xlabel("Time (s)")
# ax.set_ylabel("Baseband frequency (Hz)")
# ax.set_title("SciPy ShortTimeFFT Spectrogram")
# 
# ax.set_xlim(0.0, duration_s)
# ax.set_ylim(-Fs / 2, Fs / 2)
# 
# fig.tight_layout()
# plt.show()
#

# [SETUP] ---------------------------------------------------------------------

@dataclass(frozen=True)
class Burst:
    freq:float
    start:float
    end:float

# [END SETUP]



# [CONFIG] --------------------------------------------------------------------

T_min = 0.2                 # 20ms
hop_div = 4                 # N/4
wq = 5                      # quantity of windows inside T_min
Fs = 16384                  # semi-arbitrary 2^14 so kHz example frequencies < nyquist
recording_duration = 1      # seconds
a = 0.1                     # for Tukey window to smooth signals. 0.1 ~= 10% of signal

s1 = Burst(3300, 0.1, 0.25) # 3.3 kHz
s2 = Burst(1000, 0.3, 0.5)  # 1. kHz
s3 = Burst(2500, 0.6, 0.85) # 2.5 kHz

# [END CONFIG]



# [SIMULATION] ----------------------------------------------------------------
qty_samples = int(Fs * recording_duration)
t = np.arange(qty_samples) / Fs
x = np.zeros(qty_samples, dtype=np.complex128) # timeline

Tw  = T_min / wq
N   = int(Fs*Tw) # samples per segment
hop = N // hop_div

stft = signal.ShortTimeFFT.from_window(
    "hann",
    fs=Fs,
    fft_mode='centered', # expecting complex signals
    nperseg=N,
    noverlap=N-hop,
    scale_to="psd"
)

gate_1 = (t >= s1.start) & (t < s1.end)
signal_1 = np.exp(1j * 2 * np.pi * s1.freq * t[gate_1])
env_1 = tukey(np.size(signal_1), alpha=a)
x[gate_1] += env_1 * signal_1

gate_2 = (t >= s2.start) & (t < s2.end)
signal_2 = np.exp(1j * 2 * np.pi * s2.freq * t[gate_2])
env_2 = tukey(np.size(signal_2), alpha=a)
x[gate_2] += env_2 * signal_2

gate_3 = (t >= s3.start) & (t < s3.end)
signal_3 = np.exp(1j * 2 * np.pi * s3.freq * t[gate_3])
env_3 = tukey(np.size(signal_3), alpha=a)
x[gate_3] += env_3 * signal_3


power = stft.spectrogram(x) # shape of (frequency bins, time slices)


power_db = 10 * np.log10(
   np.maximum(power, 1e-12)
)
freqs = stft.f
times = stft.t(len(x))

# [END SIMULATION]



# [UI SERVICE] ----------------------------------------------------------------

print(f"Window length: {stft.m_num} samples")
print(f"Hop: {stft.hop} samples")
print(f"Overlap: {stft.m_num - stft.hop} samples")
print(f"Time-column spacing: {stft.delta_t:.4f} seconds")
print(f"Frequency-bin spacing: {stft.delta_f:.4f} Hz")

duration_s = len(x) / Fs
valid_time = (times >= 0.0) & (times <= duration_s)

times_plot = times[valid_time]
power_db_plot = power_db[:, valid_time]

fig, ax = plt.subplots(figsize=(11, 5))

mesh = ax.pcolormesh(
    times_plot,
    freqs,
    power_db_plot,
    shading="auto",
)

colorbar = fig.colorbar(mesh, ax=ax)
colorbar.set_label("Power spectral density (dB/Hz)")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Baseband frequency (Hz)")
ax.set_title("SciPy ShortTimeFFT Spectrogram")

ax.set_xlim(0.0, duration_s)
ax.set_ylim(-Fs / 2, Fs / 2)

fig.tight_layout()
plt.show()
# [END UI SERVICE]