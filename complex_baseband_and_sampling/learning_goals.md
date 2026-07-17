# Prelude
This includes learning goals for this topic and my notes on it.

# 1. Become familiar with:
- Complex samples `x[n]=I[n]+jQ[n]`
    - Used in IQ sampling, hence I and Q.
- Positive and negative frequencies
    - Found negative frequencies to be the portion of the OG signal below the carrier frequency.
- Sample rate
    - To get all information from a signal (and therefore, to avoid aliasing), sample rate should be 2x the frequency. This is the Nyquist rate.
- Nyquist zones
    - The first Nyquist zone is the frequency spectrum from DC to f_s/2 for f_s := sampling freq.
- Aliasing
    - Phenomenon where high-freq signals are misrepresented as lower frequencies due to insufficient sampling 
- Why I/Q captures preserve phase and frequency direction
    - IQ sampling preserves phase and frequency direction through its representation of signals as complex numbers.
    - Frequency direction is determined by mixing the signal with both a cosine (in-phase AKA I) and sine (quadrature AKA Q) local oscillator. This captures the signal's rotation in the complex plane.
        - A signal with a frequency greater than the center frequency is positive.
        - A signal with a frequency less than the center frequency is negative.
        - Positive corresponds to CCW, or when I leads Q by 90 degrees.
        - Negative corresponds to CW, or when I lags Q by 90 degrees.
        - Real-only sampling can not achieve this because it does not have an imaginary component.
    - A simple example uses Icos(2pift) + Qsin(2pift), equivalent to Acos(2pift - Phi) for A = sqrt(I^2+Q^2) and Phi = tan^-1(Q/I).

# 2. Exercise

Generate: `x[n]=e^(j2πf_0n/(fs))`. Then:

- Plot I[n]
    - Done
- Plot Q[n]
    - Done
- Plot ∣x[n]∣
    - Done
- Plot ∠x[n]
    - Done

- Repeat for positive and negative f_0
    - Comparing I and Q components:
        - Positive sees Q lagging I by 90 degrees, plus phase linearly decreasing on the time-angle plot.
        - Negative sees Q leading I by 90 degrees, plus phase linearly increasing on the time-angle plot.
- Choose f_0 above Nyquist and observe aliasing
    - Done, matches what I saw on PySDR where too-low sample rate causes ambiguity and mismatched reconstructions of the func
    
# 3. Theory Question
- Why is a complex signal at −100 kHz is distinguishable from one at +100 kHz?
    - Because of the way that we measure them relative to the tuning frequency. A frequency < the tuning frequency will be observed as "negative" because that represents opposite direction of phase rotation. In complex baseband, that direction tells us whether the signal is above or below the tuning frequency.
    - Behaviorally, a frequency < the tuning frequency will:
        - have the In-phase (I) component lagging the Quadrature (Q) component by 90deg when visualized
        - appear to rotate clockwise on the real-complex plane
    - And vice versa for positive frequencies:
        - I leads Q by 90deg instead of lagging,
        - Rotates CCW on the real-complex plane,
        - appears positive relative to the tuning freq.
    - However, we should note that if the file uses I - jQ, then I and Q are exchanged, Q is negated, and the receiver introduces spectrum inversion. So it's critical to establish convention before doing any work.
- Why are frequency values in a baseband file actually offsets rather than necessarily absolute RF frequencies?
    - SDRs tend to mix selected RF regions down so that the tuned center maps to 0 Hz. Then, baseband frequency = radio frequency - center frequency.
        - This has several benefits in cost and efficiency, since sampling at lower rates is cheaper.
        - This is achievable through several physical methods, including filtering and mixing.
    - 0Hz in this context represents either a signal at the tuning freq. or a DC component.
    - Absolute RF frequencies can be approximately reconstructed when the center-freq metadata and sign convention are known.