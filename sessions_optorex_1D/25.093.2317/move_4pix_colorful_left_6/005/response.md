```python
import math
import numpy as np # Use numpy for potential array operations, though list manipulation is sufficient here

"""
Transforms an input sequence of 12 digits (represented as a space-separated string) by:
1. Identifying the 'core block' which starts at the first non-zero element 
   and ends at the last non-zero element (inclusive).
2. Calculating a new starting position for this block by shifting its original 
   start position left by 4 indices, ensuring the new start index is not less than 0.
3. Creating a new sequence initialized with 12 zeros.
4. Placing the extracted 'core block' into the new sequence at the calculated 
   starting position. If the block would extend beyond the end of the 12-element sequence, 
   it is truncated. Zeros fill the remaining positions.
5. If the input sequence contains only zeros, it is returned unchanged.
"""

def find_first_nonzero_index(sequence):
  """Finds the index of the first non-zero element in a sequence."""
  for i, element in enumerate(sequence):
    if element != 0:
      return i
  return -1 # Indicate not found

def find_last_nonzero_index(sequence):
  """Finds the index of the last non-zero element in a sequence."""
  last_nz = -1
  for i, element in enumerate(sequence):
    if element != 0:
      last_nz = i
  return last_nz

def transform(input_str):
    # 1. Examine the input sequence of 12 integers. Convert string to list of ints.
    input_sequence = [int(x) for x in input_str.split()]
    n = len(input_sequence) # Should be 12

    # 2. Locate the index of the first non-zero integer (`first_nz`).
    first_nz = find_first_nonzero_index(input_sequence)

    # 3. If no non-zero integer is present, return the original sequence string.
    if first_nz == -1:
      return input_str

    # 4. If non-zero integers exist, locate the index of the last non-zero integer (`last_nz`).
    last_nz = find_last_nonzero_index(input_sequence)

    # 5. Identify the 'core block'.
    core_block = input_sequence[first_nz : last_nz + 1]
    core_len = len(core_block)

    # 6. Calculate the intended new starting index.
    # 7. Adjust this new starting index (clamp at 0).
    new_start = max(0, first_nz - 4)

    # 8. Create a new sequence of 12 zeros.
    output_sequence = [0] * n

    # 9. Copy the elements of the 'core block' into the new sequence, starting at `new_start`.
    #    Ensure that you do not attempt to write past the end of the 12-element new sequence.
    # Calculate how many elements can actually be placed.
    elements_to_copy = min(core_len, n - new_start)

    # Perform the copy using slicing.
    if elements_to_copy > 0:
        output_sequence[new_start : new_start + elements_to_copy] = core_block[0 : elements_to_copy]

    # 10. Return the newly constructed sequence as a space-separated string.
    return " ".join(map(str, output_sequence))
```