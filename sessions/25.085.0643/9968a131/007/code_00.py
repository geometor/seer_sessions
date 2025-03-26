"""
Transforms the input grid by modifying rows based on their index. 
Even-indexed rows (0, 2, 4, ...) are copied directly from the input to the output. 
Odd-indexed rows (1, 3, 5, ...) are cyclically shifted one position to the right. 
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid_list):
    """
    Applies a transformation where even rows are copied and odd rows are 
    cyclically shifted right.

    Args:
        input_grid_list (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert list of lists to numpy array for easier row operations
    input_grid = np.array(input_grid_list, dtype=int)
    
    height, width = input_grid.shape
    
    # Initialize output_grid as an empty array with the same shape as the input
    # We will fill it row by row.
    output_grid = np.zeros_like(input_grid)

    # Iterate through each row of the grid using its index 'r'
    for r in range(height):
        # Check if the row index 'r' is even
        if r % 2 == 0:
            # Copy the even row directly from input to output
            output_grid[r, :] = input_grid[r, :]
        # Else (if the row index 'r' is odd)
        else:
            # Perform a cyclic shift one position to the right on the input row
            # The last element becomes the first.
            # Use np.roll for efficient cyclic shifting.
            shifted_row = np.roll(input_grid[r, :], shift=1)
            
            # Assign the shifted row to the corresponding row in the output grid
            output_grid[r, :] = shifted_row

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
