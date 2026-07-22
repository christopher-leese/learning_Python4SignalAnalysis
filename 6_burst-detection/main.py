import numpy as np
import utilities as utils

# 

# [SETUP] ---------------------------------------------------------------------

rng = np.random.default_rng()

# [END SETUP]



# [CONFIG] --------------------------------------------------------------------

# debug settings
debug:bool = True # debug mode on?

# cplx signal gen settings
Fs = 16384 # semi-arbitrary 2^14 so kHz example frequencies < nyquist
f = 16 # Hz
frame_len = 5 # How long each frame is in samples
recording_duration = 2 # seconds

# noise gen settings
noise_pwr = 1 #dB

# config checks
assert(noise_pwr > 0)

# [END CONFIG]



# [SIMULATION] ----------------------------------------------------------------

# Generate complex signal
qty_samples = Fs * recording_duration
t = np.arange(qty_samples)/Fs
x = np.exp(1j * 2 * np.pi * f * t)
# Complex signal generation debug
if(debug):
    print(f"Signal frames: {qty_samples}")

# Generate noise
noise = np.sqrt(noise_pwr/2) * (
    rng.standard_normal(qty_samples) + 1j * rng.standard_normal(qty_samples)
)

# Get frame count, shared amongst noise and signal
frame_qty = utils.count_frames_of_length(noise, frame_len)
print(f"Qty frames with length {frame_len} = {frame_qty}")

# Fetch SNR info
SNR_info = utils.get_SNR_info(x, noise, True)

# Get energy across ~entire signal pair
sig_energy = utils.frame_energy(x, 1, frame_qty, False)
noise_energy = utils.frame_energy(noise, 1, frame_qty, False)

# Compare whole-signal frame energy measurement to ASOT SNR info measurement
sig_compared = utils.sig_pwr_equal(SNR_info[0], sig_energy, 0)
noise_compared = utils.sig_pwr_equal(SNR_info[1], noise_energy, 0)
print(sig_compared, noise_compared)

# [END SIMULATION]



# [UI SERVICE] ----------------------------------------------------------------

# [END UI SERVICE]