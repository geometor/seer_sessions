import math
import numpy as np

"""
Rearranges a sequence of digits (represented as a list or NumPy array of integers) 
by identifying the 'core segment' (from the first non-zero digit to the 
last non-zero digit, inclusive). This core segment is then shifted 4 positions 
to the left within the sequence. If shifting 4 positions left would move the 
start of the segment past the beginning of the sequence (index 0), it is placed 
at index 0 instead. The remaining positions are filled with zeros (leading and 
trailing) to maintain the original sequence length. If the input sequence 
contains only zeros, it is returned unchanged.
"""

def _find_first_nonzero_index(int_list):
    """Finds the index of the first non-zero element in a list."""
    for i, num in enumerate(int_list):
        if num != 0:
            return i
    return -1 # Indicate no non-zero element found

def _find_last_nonzero_index(int_list):
    """Finds the index of the last non-zero element in a list."""
    last_idx = -1
    # Iterate backwards for potential minor efficiency, but forward is fine too.
    for i in range(len(int_list) - 1, -1, -1):
        if int_list[i] != 0:
            return i
    return -1 # Should not happen if first_nonzero found one, but defensive.


def transform(input_grid) -> list:
    """
    Shifts the core non-zero segment of a sequence of digits 4 positions to the left.

    Args:
        input_grid: A list or NumPy array of single-digit integers.

    Returns:
        A list representing the transformed sequence of digits.
    """

    # Ensure input is a standard Python list for consistent operations
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assume it's already list-like (e.g., a standard list)
        input_list = list(input_grid) 
        
    original_length = len(input_list)

    # Find the start index of the core segment (first non-zero)
    first_nz_idx = _find_first_nonzero_index(input_list)

    # Handle the case where the input is all zeros
    if first_nz_idx == -1:
        # Return a copy to avoid modifying the original if it was mutable
        return list(input_list) 

    # Find the end index of the core segment (last non-zero)
    last_nz_idx = _find_last_nonzero_index(input_list)

    # Extract the core segment using list slicing
    # Note: Slicing input_list[first_nz_idx : last_nz_idx + 1] is correct
    core_segment = input_list[first_nz_idx : last_nz_idx + 1]
    core_length = len(core_segment)

    # Calculate the number of leading zeros for the output list
    # This is the target start index for the core segment
    num_output_zeros = max(0, first_nz_idx - 4)

    # Construct the output list
    # Start with the calculated number of leading zeros
    output_list = [0] * num_output_zeros
    
    # Append the core segment
    output_list.extend(core_segment)
    
    # Calculate the number of trailing zeros needed to maintain original length
    current_length = len(output_list)
    num_trailing_zeros = original_length - current_length
    
    # Append the trailing zeros
    output_list.extend([0] * num_trailing_zeros)

    # The problem description implies the output should match the input type.
    # Since the error mentioned numpy.ndarray, let's try returning that.
    # If the input was originally a list, this still works.
    # return np.array(output_list, dtype=type(input_grid[0]) if original_length > 0 else int) 
    # Let's return a list first as per the function signature `-> list`
    return output_list