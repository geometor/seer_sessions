"""
Applies a left cyclic shift (rotation) of 3 positions to an input NumPy array.
The transformation takes a 1D NumPy array, moves the first 3 elements to the end, 
maintaining the relative order of all elements, and returns the resulting array.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Performs a left cyclic shift of 3 positions on the input NumPy array.

    Args:
        input_array: A 1D NumPy array.

    Returns:
        A 1D NumPy array representing the input array rotated left by 3 positions.
    """
    
    # Define the number of positions to shift left
    shift_amount = 3
    
    # Get the length of the input array
    n = len(input_array)
    
    # Handle the edge case of an empty array
    if n == 0:
        return input_array # Return the empty array as is
        
    # Calculate the effective shift amount using modulo
    # Ensures correct wrapping behavior if shift_amount >= n, though not needed for fixed shift=3 and n=12
    effective_shift = shift_amount % n
    
    # Perform the left rotation using NumPy slicing and concatenation
    # Slice 1: Elements from the effective shift index to the end
    part1 = input_array[effective_shift:]
    
    # Slice 2: Elements from the beginning up to the effective shift index
    part2 = input_array[:effective_shift]
    
    # Concatenate the two parts to form the rotated array
    output_array = np.concatenate((part1, part2))

    # Return the resulting rotated array
    return output_array