# Prelude
This includes learning goals for this topic and my notes on it.

# 1. Questions
- What is `.sigmf-data`? Why is it different from a Non-Conforming Dataset file?
    - `.sigmf-data` is a file extension for Dataset files.
        - It MUST be appended to all Dataset files.
    - NCD files MUST NOT have `.sigmf-data` as an extension. 
        - NCD files support using valid SigMF metadata to describe data that is NOT valid SigMF and formatted according to SigMF Dataset requirements.
- What is `.sigmf-meta`?
    - `.sigmf-meta` is a metadata file extension.
    - Metadata describes its associated Dataset.
    - Metadata files MUST only describe one Dataset file.
    - Metadata files MUST be stored in UTF-8 encoding, and MUST have `.sigmf-meta` as an extension.
    - Metadata files MUST be in the same dir as the Dataset file it describes.
    - It is RECOMMENDED that base filenames of a Recording's Metadata and Data be identical.
- What is `core:datatype`?
    - The SigMF Dataset format of the stored samples in the Dataset file. examples : `[’cf32_le’, ’ri16_le’]` default : `cf32_le` type : `string`
- What is `core:sample_rate`?
    - The sample rate of the signal in samples per second. exclusiveMinimum : `0` maximum : `1000000000000` type : `number`
        - max is specifically 1 THz
- What is `core:frequency`?
    - The frequency of the signal in Hz
    - type : `number` minimum : `-1000000000000` maximum : `1000000000000` examples : `[915000000, 2400000000]`
        - min/max are -+ 1 THz
- What is `core:sample_start`?
    - The sample index at which this Segment takes effect.
    - default : `0` minimum : `0` maximum : `9223372036854775807` type : `integer`
        - max is the max for a 64-bit signed integer
    - References `global_index`, which is the index of a sample relative to an original sample stream
        - If omitted, `global_index` value SHOULD be treated as equal to sample_start.
- What is `core:sample_count`?
    - The number of samples that this Segment applies to.
    - type : `integer` minimum : `0` maximum : `9223372036854775807`
- What are annotation frequency edges?
    - Describe anything regarding the signal data not part of the Captures and Global objects
    - Regarding `freq_lower_edge` and `freq_upper_edge`:
        - Give the frequencies at the lower/upper edges of the annotation.
        - If there is no known center freq, or the center freq. is at baseband, then BOTH fields SHOULD be relative to baseband.
        - It is REQUIRED that either BOTH or NONE are provided.
- What are hash and provenance fields?
    - In context of the `global` object, which consists of `key:value` pairs that tell us about the entire dataset:
        - `sha512` is the SHA512 hash of the Dataset file associated with the SigMF file
        - `version` tells us the ver. of the SigMF spec used to create the Metadata file in format X.Y.Z
- What is `cf32_le`?
    - This is an example string describing SigMF **Dataset** format according to ABNF rules.
    - It specifically describes a "`complex 32-bit-floating-point little-endian`" set of samples.
    - Another example is `ru16_be`, meaning a "`real 16-bit-unsigned-integer big-endian`" set of samples.
    - And one last example, `cu8` means a `complex unsigned-byte` set of samples. 
    - We should note that only IEEE-754 single-precision and double-precision floating-point types are supported by the SigMF Core namespace.
    - Additionally, we should note that complex data types are specified by the bit width of the individual I/Q components, and NOT by the total complex pair bitwidth (like Numpy).

# 2. Exercise
Write one synthetic cf32_le recording and metadata file. Reload it through the Python library, verify the sample count, and add one manually known annotation.
- Done, pretty cool!
- Lessons learned:
    - There does not exist a complex float 32 in numpy, so used complex 8-byte (64 bit) which was inferred as cf32 by SigMF.
    - To determine endianness, we use < or >.
    - Good practice separating write and read, no God files/funcs.

# 3. Concept Question
How do you make a fresh script that validates and reopens your recording without hard-coded knowledge that exists only in the generation script?
- The script MUST check the hash of the recording and compare it to the metadata.
- The script MUST use SigMF's fromfile and read_samples to reopen the recording.
