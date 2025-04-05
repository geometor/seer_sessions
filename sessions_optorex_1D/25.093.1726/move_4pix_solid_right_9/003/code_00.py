"""
Transforms an input 2D NumPy array (shape 1x12) by shifting all non-zero elements within the single row 4 positions (columns) to the right.
The output array is initialized with zeros. For each non-zero element in the input array's first row at column index i,
if the target column index i + 4 is within the bounds of the array (less than 12), the non-zero element is placed
at that target column index in the first row of the output array. Positions in the output array that do not receive a
shifted non-zero element remain zero.
"""

import numpy as np

def transform(input_grid):
    """
    Shifts non-zero elements of a 1x12 NumPy array 4 columns to the right.

    Args:
        input_grid: A 2D NumPy array with shape (1, 12) containing integers.

    Returns:
        A 2D NumPy array with shape (1, 12) representing the transformed sequence.
    """
    # Define sequence length (number of columns) and shift amount based on observations
    sequence_length = 12 # input_grid.shape[1] could be used for generality
    shift_amount = 4

    # Initialize output_grid with zeros, matching the input shape (1, 12)
    output_grid = np.zeros_like(input_grid) # Creates a numpy array of same shape and type, filled with zeros

    # Iterate through the columns of the first (and only) row
    for i in range(sequence_length):
        # Get the element from the input grid's first row at column i
        element = input_grid[0, i]

        # Check if the element is non-zero
        if element != 0:
            # Calculate the target column index by adding the shift amount
            target_index = i + shift_amount

            # Check if the target index is within the bounds of the sequence columns
            if target_index < sequence_length:
                # Place the non-zero element at the target index in the output grid's first row
                output_grid[0, target_index] = element

    # Return the resulting output grid
    return output_grid
