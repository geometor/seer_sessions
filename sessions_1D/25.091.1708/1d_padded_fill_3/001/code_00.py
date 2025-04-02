"""
Transforms an input grid by processing each row independently. 
For each row in the input grid:
1. Find all non-white pixels (value > 0).
2. If non-white pixels exist:
   a. Identify their color (assuming only one non-white color per row).
   b. Find the minimum column index (leftmost) and maximum column index (rightmost) of these non-white pixels.
   c. In the corresponding row of the output grid, draw a horizontal line of that color from the minimum column index to the maximum column index (inclusive).
3. If a row contains only white pixels (value = 0), the corresponding row in the output grid remains all white.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the row-based horizontal line drawing transformation.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid. 
    # This handles rows that are entirely white correctly.
    output_grid = np.copy(input_grid) 
    height, width = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(height):
        row = input_grid[r, :]
        
        # Find the column indices of non-white pixels in the current row
        non_white_indices = np.where(row > 0)[0]

        # Check if there are any non-white pixels in this row
        if non_white_indices.size > 0:
            # Determine the color (use the color of the first non-white pixel found)
            color = row[non_white_indices[0]]
            
            # Find the minimum (leftmost) and maximum (rightmost) column index
            min_col = np.min(non_white_indices)
            max_col = np.max(non_white_indices)
            
            # Fill the corresponding row in the output grid with the color 
            # between min_col and max_col (inclusive)
            output_grid[r, min_col : max_col + 1] = color
        # else: 
            # If the row was all white, the output_grid row (copied from input) is already correct.

    return output_grid
