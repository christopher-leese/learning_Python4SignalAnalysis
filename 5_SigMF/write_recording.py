import numpy as np
import matplotlib.pyplot as plt
import sigmf


# Write one synthetic cf32_le recording and metadata file.
# Reload it through the Python library,
# verify the sample count, and add one manually known annotation.

# model:
#   INPUTS: recording duration, sample frequency, signal frequency
#       -> flow into config
#   
#   SIMULATION SERVICE:
#
#       Create a complex signal
#           REQUIRES:
#               Extension recording.sigmf-data
#               Complex samples MUST be interleaved, with in-phase comp. first
#               (i.e., I[0] Q[0] I[1] Q[1] ... I[n] Q[n])
#               Signal to be 32-bit floating point, little endian
#               Assign complex signal to above format array var
#
#       Create a metadata file
#           REVISION: INTEGRATED WITH Recording
#           REQUIRES:
#               Accomplished via Recording instance
#               Extension recording.sigmf-meta
#               JSON format, single top-level JSON Object
#               top level obj MUST contain three JSON Objects named:
#                   global, captures, and annotations
#               If a name/value pair applies to a particular segment,
#               then it MUST appear in that segment
#
#       Set up Recording instance "recording"
#           REQUIRES:
#               sigmf.fromarray(samples) FOR complex signal array samples
#               recording.sample_rate = Fs
#               recording.add_capture(start_index, metadata)
#               Inside global:
#                   datatype
#                   sample_rate
#                   version
#                   sha512
#               Inside captures:
#                   sample_start
#                   frequency
#               Inside Annotations:
#                   sample_start
#                   sample_count
#                   freq_lower_edge
#                   freq_upper_edge
#                   --> expecting all of this to be empty, adding it later



# [CONFIG] --------------------------------------------------------------------
filename:str = "recording"
Fs = 16384 # semi-arbitrary 2^14 so kHz example frequencies < nyquist
f = 16 # Hz
recording_duration = 2 # seconds

# [END CONFIG]



# [SIMULATION] ----------------------------------------------------------------

# Generate complex signal
qty_samples = Fs * recording_duration
t = np.arange(qty_samples)/Fs

x = np.exp(1j * 2 * np.pi * f * t)
samples = x.astype('<c8') # want signal cf32_le, c8 inferred as cf32.

# Set up recording
recording = sigmf.fromarray(samples)
recording.sample_rate = Fs

recording.add_capture(
    start_index=0,
    metadata={
        sigmf.FREQUENCY_KEY: f,
    }
)

# Write samples and recording metadata with try/except
try:
    recording.tofile(f"{filename}.sigmf-meta",overwrite=True)
    print(f"Successfully wrote metadata for '{filename}'!")
    samples.tofile(f"{filename}.sigmf-data")
    print(f"Successfully wrote data for '{filename}'!")
except Exception as e:
    print(f"Error: {e}")


# [END SIMULATION]



# [UI SERVICE] ----------------------------------------------------------------

# (DEBUG) check signal in time domain
print("[DEBUG] CONTENT")
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(t, np.real(x), label="Real")
ax.plot(t, np.imag(x), label="Imaginary")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Signal x, Real vs Imaginary")
ax.legend()
fig.tight_layout()
plt.show()
print(recording.dumps(pretty=True))

# [END UI SERVICE]