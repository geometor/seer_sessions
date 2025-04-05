import numpy as np
import math

"""
Transforms an input 1D NumPy array by identifying the shortest repeating sequence 
(the 'fundamental pattern') within the initial non-zero part of the array. 
This fundamental pattern is then repeated to fill a new array of the same 
length as the original input, truncating the last repetition if necessary.
"""

def find_fundamental_pattern(sequence):
    """
    Finds the shortest repeating pattern at the beginning of a NumPy array sequence.

    Args:
        sequence: A 1D NumPy array of integers representing the non-zero prefix.

    Returns:
        A 1D NumPy array representing the fundamental pattern. Returns the 
        original sequence if no repeating pattern is found within the first half,
        or if the sequence is too short to contain a repetition.
    """
    n = len(sequence)
    if n == 0:
        return np.array([], dtype=sequence.dtype) # Return empty array of same type
        
    # Iterate through possible pattern lengths from 1 up to half the sequence length
    for p_len in range(1, n // 2 + 1):
        # Check if the sequence is long enough for the comparison
        if n >= 2 * p_len:
            # Compare the first block with the second block
            if np.array_equal(sequence[0:p_len], sequence[p_len:2 * p_len]):
                return sequence[0:p_len] # Found the shortest repeating pattern

    # If no repeating pattern is found by checking the first half,
    # the fundamental pattern is the entire non-zero sequence itself.
    return sequence

def transform(input_grid):
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Get the total length of the input array
    L = len(input_grid)

    # Find the index of the first zero, if any
    zero_indices = np.where(input_grid == 0)[0]
    if len(zero_indices) > 0:
        first_zero_index = zero_indices[0]
    else:
        # No zeros found, the entire grid is the prefix
        first_zero_index = L 

    # Extract the non-zero prefix
    non_zero_prefix = input_grid[:first_zero_index]

    # Handle case where the input starts with 0 or is all zeros
    if len(non_zero_prefix) == 0:
        # If the input was empty or all zeros, return zeros of the same length
        return np.zeros(L, dtype=input_grid.dtype)

    # Find the fundamental repeating pattern within the prefix
    fundamental_pattern = find_fundamental_pattern(non_zero_prefix)
    
    pattern_len = len(fundamental_pattern)

    # Handle case where the pattern finding somehow returns empty (should not happen with current logic if prefix exists)
    if pattern_len == 0:
         return np.zeros(L, dtype=input_grid.dtype) # Fallback

    # Calculate how many times the pattern needs to be repeated (at least partially)
    # to fill the output length L. Use ceiling division.
    num_repeats = math.ceil(L / pattern_len)

    # Create the tiled/repeated pattern
    # np.tile repeats the whole array 'num_repeats' times
    tiled_pattern = np.tile(fundamental_pattern, num_repeats)

    # Truncate the repeated pattern to the exact original length L
    output_grid = tiled_pattern[:L]

    return output_grid