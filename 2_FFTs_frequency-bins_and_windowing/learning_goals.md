# Prelude
This includes learning goals for this topic and my notes on it.

# 1. Questions
- What does DFT represent?
    - DFT means discrete fourier transform. We use discrete operations in computation for practical reasons.
    - DFT takes a finite sequence of equally spaced samples from a time domain, and converts them into a sequence of coefficients describing the frequency domain.
    - DFT is O(N^2). FFT is O(N log (N)) by virtue of implementation. FFT is most efficient when size is a power of 2.
- What is FFT spacing?
    - FFT spacing is the difference in frequency between adjacent FFT bins (discrete frequency intervals)
    - Defined as Fs/N for Fs := sampling frequency and N := FFT size
    - Also known as bin spacing, line spacing, or frequency resolution
- What is `fftfreq`?
    - `fftfreq` returns the sample frequencies of the for the DFT, mapping FFT output bins to corresponding frequency values.
    - For example, 8 bins separated by 0.1 seconds each would result in an `fftfreq` output `[0, 1.25, 2.5, 3.75, -5, -3.75, -2.5, -1.25]`
    - We note that fftfreq does not do any centering. We use `fftshift` for that.
- What is `fftshift`?
    - This function takes an FFT, which has default output `0 (DC) --> +frequencies --> N/2 --> -frequencies --> N-1` and centers it along `N/2`, resulting in the format `-N/2 --> -frequencies --> 0 (DC) --> +frequencies --> ~N/2` (for large N)
        - For smaller N, the last index of the FFT is `Fs/2 - Fs/N`.
- Magnitude vs Power?
    - Magnitude is also known as amplitude in the context of a signal function. It tells us how strong the signal is at an instantaneous point.
    - Power is the square of magnitude (i.e. P = |x(t)|^2). Power tells us the signal's rate of energy transfer at a specific point in time. Power is preferred for physical reasons.
- What is spectral leakage?
    - Spectral leakage is an artifact of a DFT / FFT operation with a signal segment that contains a non-integer quantity of cycles. i.e. the samples cut off at a point which is not continuous with the start.
    - This causes a single frequency to spread into adjacent bins, i.e. the creation of artificial frequencies.
        - These are not actually new frequencies, it's just the FFT representing an in-between using its limited set of bins
    - The result appears smeared with side lobes.
    - Spectral leakage is not aliasing. Aliasing is due to insufficient sample rate.
- What are window functions?
    - Window functions constrain a signal's samples by tapering them to ~zero as we reach both ends.
    - This matters because FFT assumes it's receiving a piece of a periodic signal.
    - Therefore, a sudden transition between the first and last samples will look like many frequencies.
        - Recall the analogy with hitting a nail with a hammer, and the square wave. Sharp transitions cause many frequencies reflecting a `sinc` behavior in the frequency domain.
        - Switching a signal on and off instantly requires energy spread across a wide range of frequencies!
    - Therefore, window functions solve the problem of sharp transitions in a FFT by ensuring the last and first frequencies taper off to ~zero.
    - Several window functions exist that achieve this goal.
- What are the resolution tradeoffs between sample count and frequency-bin spacing?
    - A smaller FFT bin spacing increases precision of peaks in our observation, but it does not add actual frequency resolution to our observation.
        - i.e. adds visual interpolation and peak location precision, so we can find a single peak's center that previously wasn't clear.
        - does not help us resolve two+ separate but close frequencies, i.e. frequencies with separation beneath our resolution
    - A higher frequency resolution comes from more samples, for example, when you collect data for longer.
        - For amplitude resolution, we need more bits per sample.
    - With respect to FFTs, it's not always necessary to input every single sample. For a signal that's always on, you could hypothetically put only 1024 of 100k samples and still get a solid result.

# 2. Exercise
Create two complex tones, add them together, and recover their frequencies.
    - Done using integers 1, 2, 3.
    - Frequencies are recovered graphically by visually identifying spikes.
    - Frequencies are recovered programatically by using `argsort` to find a user-defined quantity of maxima.
        - For example, recovert the top 1, 2, 3, even 100 maxima.
        - We can compare either graphically or numerically. If the first `n` frequencies have significantly greater magnitudes than the remaining frequencies, we may hypothesize that we have `n` complex signals in the final summed signal.
        - Accuracy, as expected, increases with higher simulation points.

Then, repeat with a tone that does not fall exactly on an FFT bin:

- No window
    - Done by randomizing two of the three signals between -3 and 3, and letting one live exactly in bin `Fs/N`. Observed jagged crests / asymmetric spikes.
- Hamming window
    - Hamming is applied in the time domain. Changed randomization to be between -5 and 5. Left the one in `Fs/N` as-is. Observed hilly crests.
- Two different FFT lengths
    - Done, observed greater precision in peak location, but for very close frequencies, it appears as one single peak. So resolution does not improve with greater FFT length.

# 3. Concept Question
Can you predict the FFT-bin spacing before running the code? Can you distinguish frequency resolution from zero-padding or visual interpolation?
- We can predict FFT bin spacing by looking at our sample points quantity (N) and sample rate (Fs). Bin spacing is defined as Fs/N [Hz]. Bin spacing is also known as our frequency resolution.
    - Not to be mistaken by N/Fs, which tells us our observation duration in seconds.
    - So for any FFT, we can predict its bin spacing so long as we have N and Fs.
- We can distinguish frequency resolution from visual interpolation by:
    1. Comparing resolution (Fs/N) to (Fs/N_fft) where N_fft := FFT output length
    2. Overlaying the original FFT points on the zero-padded FFT curve