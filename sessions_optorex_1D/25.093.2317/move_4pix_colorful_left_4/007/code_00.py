import numpy as np
from typing import List, Tuple, Optional

"""
Transforms an input sequence of integers by identifying a 'core block' 
(from the first non-zero element to the last non-zero element, inclusive) 
and shifting this block 4 positions to the left within a new sequence of 
the same length, initialized with zeros. Zeros pad the sequence on the right 
after the shifted block. Elements shifted beyond the beginning (index < 0) 
or end (index >= length) of the sequence are discarded. The final output is 
returned as a list of integers.
"""

# Helper function to find the indices of the first and last non-zero elements
def find_non_zero_bounds_np(sequence: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the index of the first and last non-zero element in a NumPy array.

    Args:
        sequence: The input NumPy array of integers.

    Returns:
        A tuple containing the start and end indices (inclusive) of the 
        non-zero block, or None if no non-zero elements are found.
    """
    # Find indices where elements are not zero
    non_zero_indices = np.nonzero(sequence)[0] # Get indices for the first dimension (works for 1D arrays)
    
    # If no non-zero elements were found, return None
    if len(non_zero_indices) == 0:
        return None
        
    # Otherwise, return the first and last index from the list of non-zero indices
    first_nz_idx = non_zero_indices[0]
    last_nz_idx = non_zero_indices[-1]
    return (first_nz_idx, last_nz_idx)

def transform(input_sequence_list: List[int]) -> List[int]:
    """
    Applies the core block left shift transformation to the input sequence.

    Args:
        input_sequence_list: The input list of integers.

    Returns:
        The transformed list of integers.
    """
    # Convert input list to a NumPy array for easier manipulation
    input_sequence = np.array(input_sequence_list, dtype=int)
    
    # Get the length of the sequence
    n = len(input_sequence)
    
    # Define the fixed amount to shift the core block to the left
    shift_amount = 4

    # Initialize the output sequence as a NumPy array of zeros with the same length
    output_sequence = np.zeros(n, dtype=int) 

    # Find the start and end indices of the core block (first to last non-zero)
    bounds = find_non_zero_bounds_np(input_sequence)

    # If no non-zero elements exist (bounds is None), the output is all zeros.
    # Return the initialized output sequence converted back to a list.
    if bounds is None:
        return output_sequence.tolist() 

    # Unpack the start and end indices
    first_nz_idx, last_nz_idx = bounds

    # Extract the core block from the input sequence using slicing
    core_block = input_sequence[first_nz_idx : last_nz_idx + 1]
    core_len = len(core_block)
    
    # Calculate the *intended* starting position for the core block in the output sequence
    # This is the starting position if there were no boundaries
    output_start_idx_intended = first_nz_idx - shift_amount

    # --- Determine the actual portion of the core block to copy and its destination ---
    # This handles cases where the block shifts partially or fully off the left edge,
    # or would extend beyond the right edge.

    # Initialize variables for slicing the core_block and placing it in the output
    copy_start_in_core = 0          # Starting index within the core_block to copy from
    copy_start_in_output = output_start_idx_intended # Starting index within the output_sequence to place into
    copy_len = core_len             # Number of elements to copy

    # Adjust if the intended start index is negative (shifted off the left boundary)
    if copy_start_in_output < 0:
        # Calculate how many elements are shifted off the left
        off_left_amount = -copy_start_in_output 
        # Adjust the starting point within the core_block to skip these elements
        copy_start_in_core = off_left_amount
        # Reduce the number of elements to copy
        copy_len -= off_left_amount
        # The actual placement in the output sequence will start at index 0
        copy_start_in_output = 0
        
    # Adjust if the block extends beyond the right boundary (index >= n)
    # Check if the calculated end position exceeds the length of the output sequence
    if copy_start_in_output + copy_len > n:
         # Reduce the number of elements to copy so it fits exactly within the array length
         copy_len = n - copy_start_in_output

    # --- Perform the copy operation if there are elements to copy ---
    # Check if after adjustments, there's still a positive number of elements to copy
    if copy_len > 0:
        # Slice the core block to get the exact part that needs to be copied
        core_to_copy = core_block[copy_start_in_core : copy_start_in_core + copy_len]
        # Place this slice into the output sequence at the calculated position
        output_sequence[copy_start_in_output : copy_start_in_output + copy_len] = core_to_copy

    # Convert the final NumPy array back to a standard Python list and return it
    return output_sequence.tolist()