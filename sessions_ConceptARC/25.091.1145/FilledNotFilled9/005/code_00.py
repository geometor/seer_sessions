"""
Process the grid one row at a time. For each row, identify the column positions of all blue (1) pixels. If a row contains fewer than two blue pixels, it remains unchanged. If a row contains two or more blue pixels, find the column index of the leftmost blue pixel (min_col) and the rightmost blue pixel (max_col). Change the color of all white (0) pixels located at (row, c) where min_col < c < max_col to red (2). Leave all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Fills white pixels horizontally between the leftmost and rightmost blue pixels in each row.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to a numpy array for efficient manipulation
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Iterate through each row index r
    for r in range(height):
        # Find the column indices of blue (1) pixels in the current row
        blue_cols_indices = np.where(grid[r, :] == 1)[0]

        # Check if the number of blue pixels in the row is 2 or more
        if len(blue_cols_indices) >= 2:
            # Determine the minimum column index of blue pixels
            min_c = np.min(blue_cols_indices)
            # Determine the maximum column index of blue pixels
            max_c = np.max(blue_cols_indices)

            # Iterate through column indices c strictly between min_c and max_c
            for c in range(min_c + 1, max_c):
                # Check if the pixel at (r, c) in the original input grid is white (0)
                if grid[r, c] == 0:
                    # If it's white, change the corresponding pixel in the output grid to red (2)
                    output_grid[r, c] = 2

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()