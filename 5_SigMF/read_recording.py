import numpy as np
import sigmf
import json


# Write one synthetic cf32_le recording and metadata file.
# Reload it through the Python library,
# verify the sample count, and add one manually known annotation.

# model:
#   INPUTS: recording
#       -> flow into config
#   
#   PROCESSING SERVICE:
#       
#       Reload through Python library:
#           Set up Recording instance "recording-read"
#               REQUIRES:
#                   Both data and metadata base filenames are "recording"
#                   JSON object looks like:
#                   {
#                       "name": "example-channel-0-basename",
#                       "hash": "b4071db26f5c7b0c70f5066eb9..."
#                   }
#           load metadata and associate matching .sigmf-data file
#               REQUIRES:
#                   recording = sigmf.fromfile(file-string)
#                       HAS .read_samples() TO READ .sigmf-data file samples
#                       HAS .get_global_info() TO READ global metadata
#                       HAS .get_annotations() TO READ annotations
#           load recording as a NumPy array:
#               REQUIRES:
#                   samples = recording.read_samples()
#           get sample count:
#               REQUIRES:
#                   sample_qty = len(samples)
#                   --> Note that each complex value counts as 1 sample
#
#           add a manually known annotation:
#               REQUIRES:
#                   core:sample_start key/value pair FOR indicating start idx
#                   sample_count FOR qty of samples annotation applied to
#                   freq_lower_edge, freq_upper_edge FOR defining freq range
#                   label FOR annotation label
#                   generator FOR recording entity that created annotation
#


# [CONFIG] --------------------------------------------------------------------

# [END CONFIG]



# [PROCESSING] ----------------------------------------------------------------

# [END PROCESSING]



# [UI SERVICE] ----------------------------------------------------------------

# [END UI SERVICE]