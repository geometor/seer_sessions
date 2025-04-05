```python
import math
import numpy as np

"""
Rearranges a sequence of digits (represented as a list or NumPy array of integers) 
by identifying the 'core segment' (from the first non-zero digit to the 
last non-zero digit, inclusive). This core segment is then shifted 4 positions 
to the left within the sequence. If shifting 4 positions left would result in a 
negative starting index, the segment starts at index 0 instead. The remaining 
positions in the sequence are filled with zeros (leading and trailing) to maintain 
the original sequence length. If the input sequence contains only zeros, it is 
returned unchanged.
"""

def _find_first_nonzero_index(int_list):
    """Finds the index of the first non-zero element in a list."""
    for i, num in enumerate(int_list):
        if num != 0:
            return i
    return -1 # Indicate no non-zero element found

def _find_last_nonzero_index(int_list):
    """Finds the index of the last non-zero element in a list."""
    # Iterate backwards to find the last occurrence efficiently
    for i in range(len(int_list) - 1, -1, -1):
        if int_list[i] != 0:
            return i
    return -1 # Should only happen if list is all zeros

def transform(input_grid) -> list:
    """
    Applies the core segment shift transformation.

    Args:
        input_grid: A list or NumPy array of single-digit integers.

    Returns:
        A list representing the transformed sequence of digits.
    """
    # 1. Receive the input sequence and standardize to list
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assume it's list-like
        input_list = list(input_grid) 
        
    original_length = len(input_list)
    
    # Handle empty input case gracefully
    if original_length == 0:
        return []

    # 2. Identify the "core segment"
    # a. Find the index of the first non-zero digit
    first_nz_idx = _find_first_nonzero_index(input_list)

    # If no non-zero digits exist, return the original sequence (as a list copy)
    if first_nz_idx == -1:
        return list(input_list) 

    # b. Find the index of the last non-zero digit
    last_nz_idx = _find_last_nonzero_index(input_list) # Guaranteed to be found if first_nz_idx != -1

    # c. Extract the core segment
    core_segment = input_list[first_nz_idx : last_nz_idx + 1]
    core_length = len(core_segment)

    # 3. Determine the target starting position for the core_segment
    # a. Calculate the desired start index (shift left by 4)
    target_start_idx = first_nz_idx - 4
    # b. Adjust the start index to ensure it's not negative
    output_start_idx = max(0, target_start_idx)

    # 4. Construct the output sequence
    # a. Create a new list of the original length, initialized with zeros
    output_list = [0] * original_length

    # b. Copy the core_segment into the new list at the calculated start index
    # Calculate the end index for slicing in the output list
    output_end_idx = output_start_idx + core_length 
    # Place the segment, making sure it doesn't exceed the list bounds
    # (This check is somewhat redundant given the logic, but safe)
    if output_end_idx <= original_length:
        output_list[output_start_idx : output_end_idx] = core_segment
    else:
        # This case implies the core segment is too long to fit after shifting, 
        # which shouldn't happen if the logic is correct and length is preserved.
        # However, handle defensively by truncating if necessary.
        length_to_copy = original_length - output_start_idx
        output_list[output_start_idx:] = core_segment[:length_to_copy]


    # 5. Return the constructed output sequence
    return output_list
```