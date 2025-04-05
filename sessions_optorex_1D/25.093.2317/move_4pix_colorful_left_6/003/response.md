```python
import numpy as np # Use numpy for array handling as suggested by error messages

"""
Transforms an input sequence (list or array of 12 integers) by:
1. Identifying the 'core block' which starts at the first non-zero element 
   and ends at the last non-zero element (inclusive).
2. Calculating a new starting position for this block by shifting its original 
   start position left by 4 indices, but not going below index 0.
3. Creating a new sequence of 12 zeros.
4. Placing the extracted 'core block' into the new sequence at the calculated 
   starting position. Zeros fill the remaining positions.
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

def transform(input_sequence):
    """
    Applies the described transformation rule to the input sequence.

    Args:
        input_sequence: A list or numpy array of 12 integers.

    Returns:
        A list or numpy array of 12 integers representing the transformed sequence.
    """
    # Convert input to list for consistent processing, handle potential numpy array input
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        input_list = list(input_sequence) # Ensure it's a mutable list

    n = len(input_list) # Should always be 12 based on examples

    # 1. Find the index of the first non-zero element (`first_nz`).
    first_nz = find_first_nonzero_index(input_list)

    # 2. If no non-zero element is found (the sequence is all zeros), return the original sequence.
    if first_nz == -1:
      # Return in the original format if possible (numpy array or list)
      return input_sequence

    # 3. Find the index of the last non-zero element (`last_nz`).
    last_nz = find_last_nonzero_index(input_list)

    # 4. Extract the sub-sequence (the "core block").
    core_block = input_list[first_nz : last_nz + 1]
    core_len = len(core_block)

    # 5. Calculate the target starting index for the core block.
    new_start = max(0, first_nz - 4)

    # 6. Create a new sequence of n zeros.
    output_sequence = [0] * n

    # 7. Place the extracted core block into the new sequence.
    # Calculate the actual end index in the output sequence, respecting bounds.
    end_index_output = min(new_start + core_len, n)
    # Calculate how many elements of the core block can actually be copied.
    num_elements_to_copy = end_index_output - new_start

    # Copy the appropriate part of the core block.
    if num_elements_to_copy > 0:
        output_sequence[new_start : end_index_output] = core_block[:num_elements_to_copy]

    # 8. Return the resulting sequence. Return as numpy array if input was numpy array.
    if isinstance(input_sequence, np.ndarray):
        return np.array(output_sequence)
    else:
        return output_sequence
```