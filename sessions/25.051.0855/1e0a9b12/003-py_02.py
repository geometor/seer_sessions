"""
Transformation Rule: Move all non-zero colored cells to the bottom-most available row within their respective columns, maintaining their relative order, and fill the remaining cells with zeros.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving non-zero cells to the bottom of their columns.
    
    Args:
        input_grid (list of lists): The input grid.
        
    Returns:
        list of lists: The transformed output grid.
    """
    input_grid = np.array(input_grid)  # Ensure input_grid is a NumPy array
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each column
    for j in range(cols):
        # Extract non-zero elements for the current column
        column_elements = [input_grid[i, j] for i in range(rows) if input_grid[i, j] != 0]
        
        # Place elements at the bottom of the output column
        for k, value in enumerate(column_elements):
            output_grid[rows - len(column_elements) + k, j] = value

    return output_grid.tolist()