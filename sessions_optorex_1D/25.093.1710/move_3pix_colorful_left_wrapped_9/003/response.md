```python
"""
Rotates an input sequence (list or array) of integers left by 3 positions.
The transformation moves the first 3 elements of the sequence to the end,
maintaining the relative order of all elements.
"""

import numpy as np

def transform(input_sequence):
    """
    Applies a left cyclic shift of 3 positions to an input sequence.

    Args:
        input_sequence: A list or NumPy array of integers.

    Returns:
        A NumPy array representing the sequence after the rotation.
    """
    # Define the amount to shift
    shift_amount = 3

    # Ensure input is a NumPy array for consistent slicing and concatenation
    input_array = np.array(input_sequence)

    # Get the length of the array
    n = len(input_array)

    # Handle cases where the array is empty or too short for the shift
    # Using modulo ensures correct behavior even if n < shift_amount (rotation wraps around)
    # Although examples show n=12 > 3, this makes the function more robust.
    if n == 0:
        return input_array # Return empty array if input is empty

    effective_shift = shift_amount % n

    # Perform the left rotation using slicing and concatenation:
    # 1. Slice the array from the effective_shift index to the end.
    part1 = input_array[effective_shift:]
    
    # 2. Slice the array from the beginning up to the effective_shift index.
    part2 = input_array[:effective_shift]
    
    # 3. Concatenate part1 followed by part2 to get the rotated array.
    output_array = np.concatenate((part1, part2))

    # Return the resulting rotated array
    return output_array
```