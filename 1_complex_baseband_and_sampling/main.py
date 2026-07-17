import numpy as np
import matplotlib.pyplot as plt

# [CONFIG]
F0 = 500  # requested sinusoid frequency [Hz]
Fs = 2000  # sample rate [samples/s]
N = 2048  # number of samples to simulate
# ----------------------------------------------------------------

# [NYQUIST AND ALIASING INFO]
nyquist_frequency = Fs / 2
# Fold any frequency into the complex sampled-data interval [-Fs/2, Fs/2).
alias_frequency = (F0 + Fs / 2) % Fs - Fs / 2

print(f"Nyquist frequency: {nyquist_frequency:g} Hz")
print(f"Requested frequency: {F0:g} Hz")
print(f"Observed (aliased) frequency: {alias_frequency:g} Hz")
print(f"Aliasing? {not np.isclose(F0, alias_frequency)}")
# ----------------------------------------------------------------

# [GENERATE SAMPLES]
n = np.arange(N)
t = n / Fs
# t is already measured in seconds, so do not divide the exponent by Fs again
x = np.exp(1j * 2 * np.pi * F0 * t)

fig, axes = plt.subplots(3, 1, figsize=(12, 8))
ax_signal, ax_phase, ax_alias = axes.flat

# Showing only a few samples keeps the discrete-time plots readable
shown = 64

# Draw the underlying continuous-time sinusoid densely, then place the actual
# discrete samples on top. This keeps the familiar smooth I/Q view while also
# showing what the sampler actually observes.
reference_cycles = 4
reference_frequency = max(abs(F0), 1)
reference_duration = reference_cycles / reference_frequency
t_reference = np.linspace(0, reference_duration, 2000)
x_reference = np.exp(1j * 2 * np.pi * F0 * t_reference)
reference_sample_count = min(N, int(np.floor(reference_duration * Fs)) + 1)

ax_signal.plot(t_reference, x_reference.real, label="I continuous")
ax_signal.plot(t_reference, x_reference.imag, label="Q continuous")
ax_signal.plot(t_reference, np.abs(x_reference), label="Magnitude")
ax_signal.plot(
    t[:reference_sample_count],
    x.real[:reference_sample_count],
    "o",
    color="tab:blue",
    markersize=3,
    linestyle="none",
    label="I samples",
)
ax_signal.plot(
    t[:reference_sample_count],
    x.imag[:reference_sample_count],
    "o",
    color="tab:orange",
    markersize=3,
    linestyle="none",
    label="Q samples",
)
ax_signal.set_xlabel("Time [s]")
ax_signal.set_ylabel("Amplitude")
ax_signal.set_title("Continuous I/Q and discrete samples")
ax_signal.legend()
ax_signal.grid(True)

ax_phase.plot(n[:shown], np.angle(x[:shown]), "o-", color="tab:green")
ax_phase.set_xlabel("Sample number n")
ax_phase.set_ylabel("Wrapped phase [rad]")
ax_phase.set_title("Phase seen by the sampler")
ax_phase.grid(True)

# The requested and aliased continuous waves differ between samples, but have
# exactly the same value at every sampling instant
demo_samples = 12
t_dense = np.linspace(0, (demo_samples - 1) / Fs, 1000)
requested_wave = np.cos(2 * np.pi * F0 * t_dense)
aliased_wave = np.cos(2 * np.pi * alias_frequency * t_dense)
sample_t = np.arange(demo_samples) / Fs

ax_alias.plot(t_dense, requested_wave, label=f"Requested: {F0:g} Hz")
ax_alias.plot(
    t_dense,
    aliased_wave,
    "--",
    label=f"Alias: {alias_frequency:g} Hz",
)
ax_alias.plot(sample_t, np.cos(2 * np.pi * F0 * sample_t), "ko", label="Samples")
ax_alias.set_xlabel("Time [s]")
ax_alias.set_ylabel("Real amplitude")
ax_alias.set_title("Different continuous waves, identical samples")
ax_alias.legend()
ax_alias.grid(True)

fig.suptitle(f"Sampling {F0:g} Hz at {Fs:g} samples/s")
plt.tight_layout()
plt.show()
# ----------------------------------------------------------------
