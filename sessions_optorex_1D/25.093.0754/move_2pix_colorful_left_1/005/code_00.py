"""
Transforms an input grid (assumed to be a 1xN NumPy array of integers) by:
1. Extracting the 1D sequence of integers.
2. Identifying the contiguous subsequence ('core sequence') starting with the 
   first non-zero integer and ending with the last non-zero integer.
3. Shifting this core sequence left by two positions relative to its original 
   starting position, but ensuring its new starting index is not less than 0.
4. Constructing the output sequence by placing the appropriate number of 
   leading zeros, followed by the shifted core sequence, and padding with 
   trailing zeros to maintain the original length N.
5. If the input sequence contains only zeros, it is returned unchanged.
6. The final output is formatted as a 1xN NumPy array.
"""

import numpy as np
import math # Although not used, included as per template suggestion

def _find_first_last_nonzero(sequence):
    """
    Finds the index of the first and last non-zero element in a sequence.

    Args:
        sequence: A list or 1D numpy array of numbers.

    Returns:
        A tuple (first_nonzero_index, last_nonzero_index).
        Returns (None, None) if no non-zero element is found.
    """
    first_nonzero_index = None
    last_nonzero_index = None
    # Iterate through the sequence with index
    for i, val in enumerate(sequence):
        # Check if the value is not zero
        if val != 0:
            # If this is the first non-zero found, record its index
            if first_nonzero_index is None:
                first_nonzero_index = i
            # Always update the last non-zero index found
            last_nonzero_index = i
    return first_nonzero_index, last_nonzero_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A 1xN NumPy array of integers.

    Returns:
        A 1xN NumPy array representing the transformed sequence.
    """
    # 1. Extract the primary 1D sequence of digits from the input structure.
    # Assuming input_grid is always shape (1, N) based on previous errors.
    if input_grid.shape[0] != 1:
        # Handle unexpected input shape if necessary, though ARC typically uses consistent shapes.
        # For now, proceed assuming shape (1, N)
        pass 
        
    input_sequence = input_grid[0].tolist() # Convert to list for easier handling
    original_length = len(input_sequence) # Let its length be N.

    # 2. Find the index of the first non-zero digit (`first_nz`).
    # 3. Find the index of the last non-zero digit (`last_nz`).
    first_nz, last_nz = _find_first_last_nonzero(input_sequence)

    # If no non-zero digit exists, return the original input grid.
    if first_nz is None:
        return np.copy(input_grid) # Return a copy to avoid modifying original

    # 4. Extract the 'core sequence'.
    core_sequence = input_sequence[first_nz : last_nz + 1]

    # 5. Calculate the starting index (`output_start`) for the core sequence in the output.
    output_start_index = max(0, first_nz - 2)

    # 6. Construct the output sequence (length N) as a list.
    # a. Start with leading zeros.
    leading_zeros = [0] * output_start_index
    
    # b. Append the core sequence.
    output_sequence_parts = leading_zeros + core_sequence
    
    # c. Append trailing zeros until the total length reaches N.
    num_trailing_zeros = original_length - len(output_sequence_parts)
    # Ensure non-negative number of zeros
    trailing_zeros = [0] * max(0, num_trailing_zeros) 
    
    output_sequence_list = output_sequence_parts + trailing_zeros

    # 7. Convert the constructed list back into a 1xN NumPy array format.
    # Ensure the output dtype matches the input dtype.
    output_grid = np.array([output_sequence_list], dtype=input_grid.dtype)

    # 8. Return the constructed output grid.
    return output_grid