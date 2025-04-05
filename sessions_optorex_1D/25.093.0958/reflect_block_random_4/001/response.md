```python
import math
import numpy as np # Although not strictly necessary for this task, it's often useful

"""
Reverses the segment of a sequence of digits that lies between the first non-zero digit and the last non-zero digit (inclusive). 
Digits outside this segment (leading and trailing zeros) remain unchanged. If there are no non-zero digits, the sequence remains unchanged.
"""

def find_first_last_non_zero_indices(seq):
    """
    Finds the indices of the first and last non-zero elements in a sequence.

    Args:
        seq: A list of numbers.

    Returns:
        A tuple (first_index, last_index). Returns (None, None) if no non-zero elements are found.
    """
    first = None
    last = None
    for i, x in enumerate(seq):
        # Convert to number if elements are strings, handle potential errors
        try:
            val = int(x)
        except (ValueError, TypeError):
            # Handle cases where elements are not easily convertible to int if necessary
            # For this problem, assuming input is list of ints or convertible strings
            continue 
            
        if val != 0:
            if first is None:
                first = i # Record index of the first non-zero element
            last = i # Update index of the last non-zero element seen so far
    return first, last

def transform(input_grid):
    """
    Reverses the segment of the input list between the first and last non-zero elements.

    Args:
        input_grid: A list of integers.

    Returns:
        A new list with the specified segment reversed.
    """
    # Ensure input is a list (or similar sequence type)
    if not isinstance(input_grid, (list, tuple)):
         # Handle potential string input if necessary based on how it's called
         # Assuming input_grid is already in the correct list format for now
         pass # Or raise TypeError("Input must be a sequence")

    # Find the indices of the first and last non-zero elements
    first_nz, last_nz = find_first_last_non_zero_indices(input_grid)

    # If no non-zero elements exist (first_nz is None), return a copy of the original grid
    if first_nz is None:
        return list(input_grid)

    # Create a copy to avoid modifying the original input list directly
    output_grid = list(input_grid)

    # Extract the sub-sequence to be reversed (inclusive indices)
    # Note: Python slicing is exclusive of the end index, so use last_nz + 1
    sub_sequence = output_grid[first_nz : last_nz + 1]

    # Reverse the extracted sub-sequence
    reversed_sub_sequence = sub_sequence[::-1] # Efficient slicing to reverse

    # Replace the original sub-sequence with the reversed version in the output grid
    output_grid[first_nz : last_nz + 1] = reversed_sub_sequence

    return output_grid

```