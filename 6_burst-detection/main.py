import numpy as np

# 

# [SETUP] ---------------------------------------------------------------------

rng = np.random.default_rng()

# EFF:
#   For a given signal and frame length, calculates qty of frames in signal
#   --> Note that frames are back-to-back in series, i.e. non-overlapping
def count_frames_of_length(signal:np.ndarray, length:int):
    return len(signal)//length

# REQ:
#   mL+L-1 MUST NOT exceed signal sample quantity,
#   non-overlapping scenario OR hop size = L
# EFF:
#   Calculates frame energy for a single frame `m` of length `L` samples
def frame_energy(signal:np.ndarray, frame:int, length:int, verbose:bool):
    # For frames `m` of length `L`,
    # energy is defined as: `E[m] = 1/L * sum of |x[n]|^2 from (n = mL) to mL+L-1`
    if (verbose):
        print("\n[BEGIN] frame_energy CALL")
        print(f"mL = {frame*length} | mL+L-1 = {frame*length+length-1}")

    agg:float = 0
    for i in range(frame*length, frame*length+length-1):
        agg += np.abs(signal[i])**2

    if (verbose):
        print(f"Energy = {agg/length}")
        print("[END] frame_energy CALL\n")

    return agg/length

def get_SNR_info(signal_timedomain:np.ndarray, noise_timedomain:np.ndarray, verbose:bool):
    sig_pwr = np.mean(np.abs(signal_timedomain**2))
    nse_pwr = np.mean(np.abs(noise_timedomain**2))
    net_pwr = sig_pwr + nse_pwr
    SNR_dB = 10*np.log10(sig_pwr / nse_pwr)

    if (verbose):
        print(f"sig pwr = {sig_pwr}\nnse pwr = {nse_pwr}\nnet pwr = {net_pwr}\nSNR = {SNR_dB} dB")

    info = np.array(
        [sig_pwr, nse_pwr, net_pwr, SNR_dB],
        np.float64
    )

    return info

# [END SETUP]



# [CONFIG] --------------------------------------------------------------------

debug:bool = True # debug mode on?

Fs = 16384 # semi-arbitrary 2^14 so kHz example frequencies < nyquist
f = 16 # Hz
frame_len = 5 # How long each frame is in samples
recording_duration = 2 # seconds

noise_pwr = 10 #dB

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
frame_qty = count_frames_of_length(noise, frame_len)
print(f"Qty of frames with length {frame_len} = {frame_qty}")

# Fetch SNR info
get_SNR_info(x, noise, True)

# Get energy across ~entire signal pair
sig_energy = frame_energy(x, 1, frame_qty, True)
sig_energy = frame_energy(noise, 1, frame_qty, True)

# [END SIMULATION]



# [UI SERVICE] ----------------------------------------------------------------

# [END UI SERVICE]