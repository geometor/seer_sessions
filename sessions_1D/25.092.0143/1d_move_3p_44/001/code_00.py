"""
Transforms a 1x7 input grid by performing a right cyclic shift of 3 positions 
on the first 6 elements, leaving the 7th element unchanged. The input grid 
typically consists of three identical non-white pixels followed by four white 
pixels. The output grid will have three white pixels, followed by the three 
non-white pixels, followed by one white pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a cyclic shift transformation to a 1x7 input grid.

    Args:
        input_grid (np.ndarray): A 1x7 numpy array representing the input grid.

    Returns:
        np.ndarray: A 1x7 numpy array representing the transformed output grid.
    """
    # Ensure the input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Extract the single row from the input grid
    input_row = input_grid[0]

    # Check if the input row has the expected length (7)
    if len(input_row) != 7:
        # Handle unexpected input size if necessary, 
        # for now, let's assume it's always 7 based on examples
        # Or raise an error: raise ValueError("Input grid must be 1x7")
        # Returning the input unmodified might be safer in some contexts
        return input_grid 

    # Isolate the first 6 elements that will be shifted
    elements_to_shift = input_row[:6]

    # Isolate the last element that remains unchanged
    last_element = input_row[6]

    # Perform a right cyclic shift by 3 positions on the first 6 elements
    # np.roll(array, shift_amount)
    shifted_elements = np.roll(elements_to_shift, 3)

    # Construct the output row by combining the shifted part and the fixed part
    output_row = np.concatenate((shifted_elements, [last_element]))

    # Reshape the output row back into a 1x7 grid format
    output_grid = output_row.reshape(1, 7)

    return output_grid
