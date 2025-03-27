"""
Draws geometric patterns (a diagonal red line and a horizontal yellow line)
onto the input grid, preserving the first column. The diagonal line starts
at the top-right corner and goes down-left. The horizontal line fills the
bottom row, excluding the first column.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)

    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # Get the dimensions of the grid
    H, W = grid.shape

    # --- Draw the diagonal red line ---
    # Iterate through rows from the top (0) down to the second-to-last row (H-2)
    for r in range(H - 1):
        # Calculate the corresponding column for the diagonal
        # Starts at W-1 for r=0, decreases as r increases
        c = W - 1 - r
        # Ensure the drawing doesn't overwrite the first column (c=0)
        if c >= 1:
            # Set the pixel at (r, c) to red (2)
            output_grid[r, c] = 2

    # --- Draw the horizontal yellow line ---
    # Identify the last row index
    last_row = H - 1
    # Iterate through columns from the second column (1) to the last column (W-1)
    for c in range(1, W):
        # Set the pixel at (last_row, c) to yellow (4)
        output_grid[last_row, c] = 4

    return output_grid.tolist() # Return as list of lists, matching ARC format