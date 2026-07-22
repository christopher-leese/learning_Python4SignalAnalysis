import numpy as np

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

# REQ:
#   noise power > 0
# EFF:
#   Given signal and noise ndarrays,
#   returns signal power, noise power, net power, and SNR in dB
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

# REQ:
#   sig_pwr_0, sig_pwr_1 to share units
# EFF:
#   Returns whether two signal powers are approximately equal with respect to
#   a given decimal threshold
def sig_pwr_equal(sig_pwr_0:float, sig_pwr_1:float, threshold:int) -> bool:
    diff = round(sig_pwr_0 - sig_pwr_1, threshold)
    return (diff == 0)