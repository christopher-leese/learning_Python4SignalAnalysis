# Prelude
This includes learning goals for this topic and my notes on it.
It's important to note that `welch` and `ShortTimeFFT` have succeeded `spectrogram` and `stft`.

# 1. Questions
- What is "welch"?
    - `welch` stands for Welch's method, which estimates power spectral density.
- What is "ShortTimeFFT"? Why is it different from FFT?
    - `ShortTimeFFT` repeatedly applies FFT to short, windowed segments of a longer signal to produce a time-frequency representation. We know this as the spectrogram. It tells us how spectral content changes over time.
    - FFT is meant for stationary signals where frequency is constant, giving high-res freq resolution.
    - ShortTimeFFT is designed for non-stationary signals, trading some freq. resolution for time localization.
        - Time localization is the ability to determine when specific events / frequencies happen within a signal.
    - Programmatically, FFT computes a single spectrum for the whole input block. STFT multiplies the signal by a sliding window function and computes the FFT for each frame. STFT therefore creates a 2D matrix of time vs frequency (as opposed to an FFT's array of coefficients).
        - FFT resolution is determined by total signal length, whereas STFT has a tradeoff between long/short windows: the former gives better freq. res. but worse time res., and short windows give worse freq. res but better time res.
- PSD versus raw FFT magnitude?
    - PSD estimates the power distribution per unit, per unit frequency bandwidth, normalized to make it independent of record length and resolution.
        - i.e. average power density, and is normalized by bandwidth
    - FFT magnitude tells us signal amplitude and varies with record length and frequency bin size (i.e. scales w/ qty of samples!)
- What is window length?
    - Window length is the length of a single frame in a window function.
    - Window length is relevant in ShortTimeFFTs, where a sliding window function constraints where the FFT is applied.
- What is hop size
    - Hop size is the number of samples between consecutive frames.
    - Hop size tells us the step size by which the analysis window shifts across the entire signal.
    - in `SciPy`, hop size is determined automatically by `hop size = nperseg - noverlap`. 
        - `nperseg` is the length of the segment (window) in samples. 
        - `noverlap` is the number of overlapping samples between consecutive segments.
- What is overlap?
    - Overlap is the quantity of overlapping samples between consecutive segments.
- Time resolution versus frequency resolution?
    - Time resolution describes how granular our time intervals are.
        - Meaning, we can better localize transient events / changes in our signal.
    - Frequency resolution describes how granular our frequency intervals are.
        - Meaning, we can better distinguish between closely-spaced spectral peaks.
- Converting STFT magnitude or power to decibels?
    - For STFT magnitude, we use `20 * log10(stft_magnitude)` since it does not have a power unit.
    - For STFT power, we use `10 * log10(stft_power)` because it has a power unit.
    - For clarification, 20 comes from `log(x^2) = 2log(x)`.

# 2. Exercise
Generate three bursts:
- Different start times.
- Different durations.
- Different frequency offsets.

Produce a spectrogram where all three are visually identifiable. Then alter the window size and explain what improved and what degraded.
- Decreased window size to 2, then 1:
    - Looks very jagged and start/end noise stretches deeper into the signal, so that means time resolution suffers
- Increased window size to 15, then 50:
    - Looks extremely smooth, but the entire signal looks like a big blur across the y-axis (baseband, Hz), meaning frequency resolution suffers.
- Summarily, the window size behaviors match what I expected!
- lessons learned:
    - Initially had small hz (magnitude 10) appeared nearly DC.
    - Changed to kHz vals and experienced aliasing because Fs was insufficient!
        - Resolved by making Fs huge wrt vals
    - Giant cross-spectrum bands appearing at start/stop of signals because no window was in place
        - Applied Tukey envelopes for each signal, have to ensure Tukey arg0 is the size of the signal, not just its nonzero parts. We would have to do more processing w/ nonzero checking if our signals weren't guaranteed to be on and off at given times.


# 3. Concept Question
How do you select an STFT window length based on the shortest burst duration and desired frequency resolution (rather than by arbitrary trial and error)?
- Window length `wl` is defined as `wl = window duration [seconds] * sample rate [samples/sec]`:
    - Then, window duration is our shortest burst duration `min_dur`, and sample rate is `Fs`.
    - Therefore, `wl = min_dur * Fs`. For example, a minimum duration of interest `100ms` and resolution `10Hz` tells us `wl = 1000`.
    - There are two caveats!
        - For a desired frequency resolution, the window must be at least `= 1/Fs`. That gives us enough time cycles to distinguish frequencies, otherwise we don't have enough time precision.
        - For a desired minimum burst duration (without smear/other loss of precision), the window should be no longer than the burst itself. Better, the window should be less than a significant fraction of it.
        - Therefore, the constraint `1/Fs <= wl < min_dur` applies.