import numpy as np
import matplotlib.pyplot as plt

# Generate a tone with unit average power. Add complex Gaussian noise at:
# +10 dB
# 0 dB
# −5 dB
# −10 dB
# Then, measure the resulting power numerically and verify that the
# configured SNR is approximately obtained over sufficiently long sequences.

# model:
#   enter sample freq, tone freq, tgt snr's
#       -> x:signal
#           - requires time array t = n/Fs : sample*seconds
#       setup complex gaussian noise
#          for each tgt snr:
#               tgt_pwr = 10^(SNR_dB/10)
#               noise_pwr = x_pwr / tgt_pwr : squared amplitude
#               noise = sqrt(n/2)*(random Gaussian real + random Gaussian IM)
#                   ^ to evenly distribute the noise, creating CGN
#               y = x + noise # to apply the noise to signal x
#               signal_power = sqrt(magnitude(x^2))
#               noise_power  = sqrt(magnitude(noise^2))
#               total_power  = sqrt(magnitude(y^2))
#               measured_snr_db = 10*log_10(signal_power / noise_power)

# [CONFIG] --------------------------------------------------------------------

Fs = 32 # Sample freq
f = 1 # Tone freq

N_sample = 64 # Sample pts

# [END CONFIG]



# [SIMULATION] ----------------------------------------------------------------

print(f"Sampling at {Fs} Hz for {N_sample/Fs} seconds")

# Set up intervals
n       = np.arange(N_sample)
t       = n/Fs

# Create complex tone
x       = np.exp(1j * 2 * np.pi * f * t)
x_pwr   = np.mean(np.abs(x)**2)

# Set up complex Gaussian noise at goal SNRs and add
rng = np.random.default_rng()
snr_vals_db = [-10,-5,0,10]

for tgt in snr_vals_db:
    tgt_pwr = (10**(tgt/10))
    noise_pwr = x_pwr / tgt_pwr

    # need to distribute equally between real/im components
    noise = np.sqrt(noise_pwr/2) * (
        rng.standard_normal(N_sample) + 1j * rng.standard_normal(N_sample)
    )

    y = x + noise # signal after
    measured_noise_pwr = np.mean(np.abs(noise ** 2))
    measured_total_pwr = np.mean(np.abs(y ** 2))
    measured_snr_db = 10 * np.log10(
        x_pwr / noise_pwr
    )

    print(f"\nTarget SNR:   {tgt:>3} dB")
    print(f"Signal power: {x_pwr:.4f}")
    print(f"Noise power:  {measured_noise_pwr:.4f}")
    print(f"Total power:  {measured_total_pwr:.4f}")
    print(f"Measured SNR: {measured_snr_db:.2f} dB")

# [END SIMULATION]