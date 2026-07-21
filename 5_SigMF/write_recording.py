import numpy as np
import matplotlib.pyplot as plt
import sigmf
import json


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
#           REQUIRES:
#               Accomplished via Recording instance
#               Extension recording.sigmf-meta
#               JSON format, single top-level JSON Object
#               top level obj MUST contain three JSON Objects named:
#                   global, captures, and annotations
#               If a name/value pair applies to a particular segment,
#               then it MUST appear in that segment
#       
#       Set up Recording instance "recording-write"
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
#       
#
# [CONFIG] --------------------------------------------------------------------
Fs = 16384 # semi-arbitrary 2^14 so kHz example frequencies < nyquist
f = 16 # Hz
recording_duration = 2 # seconds

# [END CONFIG]



# [SIMULATION] ----------------------------------------------------------------

# Generate complex signal
qty_samples = Fs * recording_duration
t = np.arange(qty_samples)/Fs

x = np.exp(1j * 2 * np.pi * f * t)
signal = x.astype('<c8').view('<f4') # want signal cf32_le
# ^ using .view for memory efficiency
#   REQUIRES:
#       byte qty in array to be / by new data type size
#       data to be contiguous


# (DEBUG) check signal in time domain
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(t, np.real(x), label="Real")
ax.plot(t, np.imag(x), label="Imaginary")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Signal x, Real vs Imaginary")
ax.legend()
fig.tight_layout()
plt.show()

# [END SIMULATION]



# [UI SERVICE] ----------------------------------------------------------------

# [END UI SERVICE]