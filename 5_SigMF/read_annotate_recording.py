import sigmf


# Write one synthetic cf32_le recording and metadata file.
# Reload it through the Python library,
# verify the sample count, and add one manually known annotation.

# model:
#   INPUTS: recording filename, sample_start, sample_count,
#           freq_lower_edge, freq_upper_edge, label_name
#       TRADE STUDY:
#           compared sample count to duration, duration req Fs,
#           possible but just not within this scope
#
#       REQUIRES: file to be in same folder as read_annotate_recording.py
#       -> flow into config
#   OUTPUTS: annotated file recording as "filename-annotated.sigmf-meta"
#   
#   PROCESSING SERVICE:
#       
#       Reload through Python library:
#           Set up input Recording instance "recording"
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
#               Properties inside Annotations:
#                   sample_start
#                   sample_count
#                   freq_lower_edge
#                   freq_upper_edge


# [CONFIG] --------------------------------------------------------------------
recording_name:str = "recording"
label_name:str = "signal of interest"

sample_start = 0
sample_count = 32768
freq_lower_edge = 15
freq_upper_edge = 17

# [END CONFIG]



# [PROCESSING] ----------------------------------------------------------------
recording = sigmf.fromfile(f"{recording_name}.sigmf-meta")

samples = recording.read_samples()
sample_qty = len(samples)

assert(sample_start >= 0)
assert(sample_count <= sample_qty - sample_start)

try:
    recording.add_annotation(
        start_index=sample_start,
        length=sample_count,
        metadata=
        {
            "core:label": label_name,
        },
    )
except Exception as e:
    print(f"Error: {e}")

try:
    recording.tofile(f"{recording_name}.sigmf-meta", overwrite=True)
    print(f"Successfully wrote annotation for '{recording_name}'!")
except Exception as e:
    print(f"Error: {e}")

# [END PROCESSING]



# [UI SERVICE] ----------------------------------------------------------------
print(f"Samples = {sample_qty}")
print(f"Annotations = {recording.get_annotations()}")

# [END UI SERVICE]