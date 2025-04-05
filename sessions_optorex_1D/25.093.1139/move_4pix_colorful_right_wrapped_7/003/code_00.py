"""
Transforms the input 1D NumPy array by moving the last 4 elements to the 
beginning and keeping the first 8 elements after them.

1. Receive the input as a 1D NumPy array of 12 integers.
2. Extract the last 4 elements of the input array (indices 8 to 11).
3. Extract the first 8 elements of the input array (indices 0 to 7).
4. Concatenate the segment containing the last 4 elements and the segment 
   containing the first 8 elements, in that order (last 4 followed by first 8).
5. Return the resulting concatenated 1D NumPy array.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a cyclic shift to a 1D NumPy array of length 12.
    Moves the last 4 elements to the front.
    """
    # Ensure the input is a 1D array (or flatten if necessary, though examples suggest it's already 1D)
    # For this specific task with fixed size 12, direct indexing is safe.
    if input_grid.ndim > 1:
        # This case shouldn't happen based on examples, but handles potential variation
        input_grid = input_grid.flatten() 
        
    if len(input_grid) != 12:
        # Handle unexpected input length if necessary
        raise ValueError("Input array must have length 12")

    # Define the split point index (after the first 8 elements)
    split_point = 8

    # Extract the first 8 elements (indices 0 through 7)
    first_segment = input_grid[:split_point]

    # Extract the last 4 elements (indices 8 through 11)
    second_segment = input_grid[split_point:]

    # Concatenate the second segment (last 4) followed by the first segment (first 8)
    output_grid = np.concatenate((second_segment, first_segment))

    return output_grid
