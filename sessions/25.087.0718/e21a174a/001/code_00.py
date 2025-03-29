"""
Flips the input grid vertically. The content of each row in the input grid is moved 
to the corresponding row in the output grid such that the top row becomes the bottom 
row, the second row becomes the second-to-last row, and so on. The background color 
and all objects are preserved, only their vertical position changes.
"""

import numpy as np

def transform(input_grid):
    """
    Flips the input grid vertically.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the vertically flipped output grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    
    # Get the height (number of rows) of the input grid
    height = input_array.shape[0]
    
    # Create a new NumPy array of the same shape and type as the input,
    # which will serve as the output grid. It's initialized with zeros,
    # but will be filled row by row.
    output_array = np.zeros_like(input_array)
    
    # Iterate through each row of the input grid using its index 'i'
    for i in range(height):
        # Calculate the target row index in the output grid for the vertical flip.
        # Input row 0 goes to output row height-1.
        # Input row 1 goes to output row height-2.
        # ...
        # Input row height-1 goes to output row 0.
        target_row_index = height - 1 - i
        
        # Copy the entire content of the current input row (input_array[i, :])
        # to the calculated target row in the output array.
        output_array[target_row_index, :] = input_array[i, :]
        
    # Convert the resulting NumPy array back to a list of lists format
    output_grid = output_array.tolist()
    
    return output_grid
