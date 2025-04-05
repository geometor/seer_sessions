import numpy as np
import math # Not strictly needed for this specific logic, but included per template guidelines

"""
Transforms an input NumPy array of integers by cyclically shifting the last 3 
elements to the beginning of the array, while maintaining the relative order 
within the two segments (the moved segment and the remaining segment).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a cyclic shift transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the last 3 elements moved to the front.
    """
    
    # Get the total number of elements in the input array
    n = len(input_grid)
    
    # Define the number of elements to move from the end to the beginning
    k = 3 
    
    # Handle edge case: If the array has fewer than k elements, return it unchanged.
    # This prevents errors with slicing and concatenation for short arrays.
    if n < k:
        return input_grid # Return the original array as is

    # Identify the last k elements using array slicing.
    # Slicing from n-k to the end captures the last k elements.
    last_part = input_grid[n-k:]
    
    # Identify the first n-k elements using array slicing.
    # Slicing from the beginning up to (but not including) n-k captures the first part.
    first_part = input_grid[:n-k]
    
    # Construct the output array by concatenating the last part followed by the first part.
    # np.concatenate takes a tuple or list of arrays to join.
    output_grid = np.concatenate((last_part, first_part))
    
    # Return the newly constructed array.
    return output_grid
