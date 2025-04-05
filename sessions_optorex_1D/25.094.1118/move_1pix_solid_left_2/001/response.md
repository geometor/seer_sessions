```python
import math
import numpy as np
import collections

"""
Takes a sequence of 12 digits containing a single contiguous block of non-zero digits.
If the non-zero block starts at index 0, the sequence is returned unchanged.
Otherwise, the zero digit immediately preceding the non-zero block is moved to the
end of the sequence, and all elements from the start of the non-zero block onwards
are shifted one position to the left to fill the gap.
"""

def find_first_nonzero_index(sequence):
  """Finds the index of the first non-zero element."""
  for i, digit in enumerate(sequence):
    if digit != 0:
      return i
  return -1 # Indicate no non-zero element found

def transform(input_sequence):
    """
    Applies the described transformation to the input sequence.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """

    # Find the starting index of the non-zero block
    first_nz_index = find_first_nonzero_index(input_sequence)

    # Handle cases where no non-zero block exists or it starts at index 0
    if first_nz_index <= 0:
      # If no non-zeros (-1) or starts at 0, return original sequence
      return list(input_sequence) # Return a copy

    # Initialize output_grid as a copy of the input
    output_sequence = list(input_sequence)

    # Identify the zero to move (it's at first_nz_index - 1)
    zero_to_move = output_sequence.pop(first_nz_index - 1)

    # Append the removed zero to the end
    output_sequence.append(zero_to_move)

    return output_sequence

```