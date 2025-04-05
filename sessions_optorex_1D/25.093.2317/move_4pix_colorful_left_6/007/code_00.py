import numpy as np

"""
Transforms an input sequence (a NumPy array of 12 integers) by:
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
  # Use np.where to find indices of non-zero elements
  # It returns a tuple of arrays, one for each dimension. We need the first element.
  nonzero_indices = np.where(sequence != 0)[0]
  if len(nonzero_indices) == 0:
    return -1 # Indicate not found
  else:
    return nonzero_indices[0] # Return the first index found

def find_last_nonzero_index(sequence):
  """Finds the index of the last non-zero element in a sequence."""
  nonzero_indices = np.where(sequence != 0)[0]
  if len(nonzero_indices) == 0:
    return -1 # Indicate not found
  else:
    return nonzero_indices[-1] # Return the last index found

def transform(input_sequence):
    """
    Applies the described transformation rule to the input sequence.

    Args:
        input_sequence: A NumPy array of 12 integers.

    Returns:
        A NumPy array of 12 integers representing the transformed sequence.
    """
    # Ensure input is a numpy array (though the environment usually provides this)
    if not isinstance(input_sequence, np.ndarray):
        input_sequence = np.array(input_sequence)

    n = len(input_sequence) # Get sequence length (should be 12)

    # 1. Find the index of the first non-zero element (`first_nz`).
    first_nz = find_first_nonzero_index(input_sequence)

    # 2. If no non-zero element is found (all zeros), return the original sequence.
    if first_nz == -1:
      return input_sequence

    # 3. Find the index of the last non-zero element (`last_nz`).
    last_nz = find_last_nonzero_index(input_sequence)

    # 4. Extract the sub-sequence (the "core block").
    # Use slicing directly on the numpy array
    core_block = input_sequence[first_nz : last_nz + 1]
    core_len = len(core_block)

    # 5. Calculate the target starting index (`new_start`).
    # Subtract 4, clamped at 0.
    new_start = max(0, first_nz - 4)

    # 6. Create a new sequence of n zeros.
    # Initialize with zeros using numpy for efficiency
    output_sequence = np.zeros(n, dtype=input_sequence.dtype)

    # 7. Determine how many elements from the core block can fit.
    # Prevents writing past the end of the output array.
    elements_to_copy = min(core_len, n - new_start)

    # 8. Copy the determined number of elements from the core block into the new sequence.
    # Use array slicing for assignment
    if elements_to_copy > 0:
        output_sequence[new_start : new_start + elements_to_copy] = core_block[0 : elements_to_copy]

    # 9. Return the new sequence.
    return output_sequence
