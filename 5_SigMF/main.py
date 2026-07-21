import numpy as np
import sigmf as sigmf


# Write one synthetic cf32_le recording and metadata file.
# Reload it through the Python library,
# verify the sample count, and add one manually known annotation.

# model:
#   INPUTS: recording duration, sample frequency, signal frequency
#       -> flow into config
#   
#   
#

# [CONFIG] --------------------------------------------------------------------
Fs = 16384 # semi-arbitrary 2^14 so kHz example frequencies < nyquist
f = 1000 # 1 KHz
recording_duration = 2 # seconds

# [END CONFIG]



# [SIMULATION] ----------------------------------------------------------------


# [END SIMULATION]



# [UI SERVICE] ----------------------------------------------------------------


# [END UI SERVICE]