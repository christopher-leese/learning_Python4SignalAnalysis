# Prelude
This includes learning goals for this topic and my notes on it.

# 1. Questions
- What is Complex Gaussian noise?
    - Complex Gaussian noise is the noise experienced from a signal at baseband. The noise power is split between the real and imaginary components equally.
    - Importantly, the two components are independent of each other, so knowing one doesn't give the other.
    - Generated in Python using `n = np.random.randn() + 1j * np.random.randn()` (not in terms of power/noise power)
- What is Power in this context?

    - 



    - Power in a signal is equal to variance in a signal.
    - We can find the average power of a zero-mean signal/noise using `power = np.var(x)` in Python.
        - It is more convenient to work with "unit power" complex noise, which is obtained by `n = (np.random.randn(N) + 1j*np.random.randn(N))/np.sqrt(2) # AWGN with unity power`
- What does the descriptor "decibel" mean?
    - dB as a unit represents a logarithmic scale. Often, `x_db = 10*log_10(x)` or `= 20*log_10(x)`.
        - When dealing with a power of sorts, we use 10. When handling non-power values like voltage or current, we use 20.
        In DSP, we most often work with power.
        - In programming, it's important to note that `log()` often refers to the natural log. Be sure to use log base 10.
    - This scale is useful for handling number sets with significant ranges, such as 0.00000002 Watts compared to 20 Watts.
        - To visualize both linearly, we'd need a significant amount of 0's. And we likely wouldn't even be able to see the former's noise floor if we plotted it over time.
        - To represent the scales simultaneously, we'll use a logarithmic scale.
    - Undoing dB to linear is simply `x = 10^(x_db/10)`.
    - Importantly, logarithmic scale provides conveniences such as being able to add when we'd normally multiply.
        - For example, with amplifiers 1 (x2), 2 (x13), and 3 (x5): the amplification is 130x total, but the decibel amplification is 3 + 11.1 + 7 = 21.1dB (using 20 as a coefficient because this is not power)

- What is SNR? What is SINR? Why are they different?
    - SNR stands for signal-to-noise ratio. It is the measurement of differences in strength between the signal and the noise. SNR is almost always in dB.
    - Usually, we code in a way s.t. our signals are of unit power (P = 1) so we can create an SNR of 10dB by producing noise that is -10dB in power.
        - We achieve this by adjusting variance when generating the noise.
    - `SNR = P_signal / P_noise` and `SNR_dB = P_signalDb - P_noiseDb`
        - A positive SNR means signal > noise. A negative SNR means signal < noise. Detecting signals at negative SNR is difficult.
    - Since power in a signal is equal to variance, `SNR = var^2(signal) / var^2(noise)`!
- What is controlled SNR injection?

# 2. Exercise
Generate a tone with unit average power. Add complex Gaussian noise at:

- +10 dB
- 0 dB
- −5 dB
- −10 dB

Measure the resulting power numerically and verify that the configured SNR is approximately obtained over sufficiently long sequences.

# 3. Concept Question
Why is noise amplitude not numerically equal to noise power? Why does complex Gaussian noise normally need both independent I and Q components?