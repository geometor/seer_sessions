"""
Rearrange a NumPy array of integers by moving all zero elements to the beginning 
while maintaining the relative order of the non-zero elements.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Moves all zeros in a 1D NumPy array to the beginning, preserving the relative 
    order of non-zero elements.

    Args:
        input_grid: A 1-dimensional NumPy array of integers.

    Returns:
        A new 1-dimensional NumPy array with zeros moved to the start.
    """
    # Step 1: Receive the input as a 1-dimensional NumPy array (already done via arg).

    # Step 2: Create a new NumPy array containing only the non-zero elements 
    #         from the input array, preserving their original relative order.
    non_zeros = input_grid[input_grid != 0]

    # Step 3: Count the number of zero elements in the input array.
    # This can be calculated by subtracting the count of non-zeros from the total size.
    num_zeros = input_grid.size - non_zeros.size
    
    # Step 4: Create a new NumPy array containing only zero elements, 
    #         with a length equal to the count determined in the previous step.
    # Ensure the dtype matches the input array's dtype.
    zeros = np.zeros(num_zeros, dtype=input_grid.dtype)

    # Step 5: Concatenate the array of zeros (from step 4) and the array of 
    #         non-zeros (from step 2) to form the final output array.
    output_grid = np.concatenate((zeros, non_zeros))

    # Step 6: Return the resulting NumPy array.
    return output_grid
