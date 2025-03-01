"""
The transformation rule is to iterate through each column of the input grid. If a column contains only zeros, replace all values in that column with magenta (6). Otherwise, leave the column unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing columns containing only zeros with magenta pixels.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = [row[:] for row in input_grid]
    
    # Convert to numpy array for easier manipulation
    output_grid = np.array(output_grid)
    
    # Get the number of rows and columns
    num_rows = output_grid.shape[0]
    num_cols = output_grid.shape[1]

    # Iterate through each column
    for j in range(num_cols):
        # Check if all elements in the column are zero
        all_zeros = True
        for i in range(num_rows):
            if output_grid[i, j] != 0:
                all_zeros = False
                break
        
        # If all elements are zero, replace the column with 6
        if all_zeros:
            for i in range(num_rows):
                output_grid[i, j] = 6

    return output_grid.tolist()