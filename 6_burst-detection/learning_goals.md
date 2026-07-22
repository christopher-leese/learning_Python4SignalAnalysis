# Prelude
This includes learning goals for this topic and my notes on it.

# 1. Questions
Specific to detection theory
1. What is a true positive / detected burst?
- When a system or observer correctly identifies the presence of a signal or event

2. What is a missed burst?
- When a system or observer fails to identify the presence of a signal or event

- Therefore classifies it as noise instead
3. What is a false alarm?
- When a system or observer identifies noise as the presence of a signal or event

4. What is the probability of detection?
- The likelihood that a specific target / signal is identified GIVEN that it is actually present in the observation area or system
- Conditional probability metric used to evaluate effectiveness of detection systems (eg radar, temp sensors, etc)

5. What is the false-alarm rate (FAR)?
- The frequency with which an observer or detection system incorrectly identifies a signal as present when only background noise exists
- Ratio of false positives divided by total noise-only trials (false positives + true negatives)

6. What is varying or moving the decision threshold?
- A strategy used to minimize the probability of false alarms while maximizing detection probability.
    - Get data by evaluating the detector across many threshold values (restrictive to permissive)
    - Specifically want to measure Probability of Detection and Probability of False Alarm
- Lowering detection criterion raises both hit and false-alarm rates, while raising it lowers both.
- Overlaying probability density curves for FA and hit wrt a common metric (e.g. voltage) lets us inform how we move the threshold
- https://www.cns.nyu.edu/~david/courses/perception/lecturenotes/sdt/sdt.html

# 2. Exercise
Use a frame-energy detector to detect bursts. For frames `m` of length `L`, energy is defined as: `E[m] = 1/L * sum of |x[n]|^2 from (n = mL) to mL+L-1`
Then:
1. Estimate the noise floor from known noise-only synthetic frames.
2. Select a threshold above the noise floor.
3. Mark frames above the threshold.
4. Merge contiguous marked frames.
5. Convert frame indices back to sample indices.
6. Measure errors against exact synthetic start and stop samples.

Experiment:
For each SNR level, run many independently generated recordings and calculate:
- `PD = detected true bursts / total true bursts`
- `PF = noise trials declared as present / total noise trials`

# 3. Concept Question
How do you change the threshold to produce an expected (arbitrary desirable) trade between missed detections and false alarms? Let the evaluation be based on multiple randomized trials rather than one attractive spectrogram.
