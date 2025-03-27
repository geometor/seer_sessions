"""
Processes a grid based on a cellular automaton-like rule applied row by row. 
The color of a cell in row r (for r > 0) is determined by the colors of the cells 
in the row above (r-1) at columns c-1 and c+1.

1. Initialize the output grid as a copy of the input grid.
2. Iterate through rows from 1 to height-1.
3. For each cell (r, c) where 0 < c < width-1:
   a. Get the colors of the cells at (r-1, c-1) and (r-1, c+1). Let them be color_left and color_right.
   b. If both color_left and color_right are non-orange (i.e., not 7):
      i. If color_left is red (2) and color_right is red (2), set output_grid[r, c] to gray (5).
      ii. If color_left is gray (5) and color_right is gray (5), set output_grid[r, c] to red (2).
      iii. If color_left is gray (5) and color_right is red (2), set output_grid[r, c] to red (2).
      iv. If color_left is red (2) and color_right is gray (5), set output_grid[r, c] to gray (5).
   c. Otherwise, the cell output_grid[r, c] retains its initial value (which is copied from the input, typically orange).
4. Return the final output grid.
"""

import numpy as np

# Define color constants
ORANGE = 7
RED = 2
GRAY = 5

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of the input_grid
    # We work on the output_grid, using input_grid as the reference for the previous row
    output_grid = np.copy(input_grid)

    # Iterate through rows, starting from the second row (index 1)
    for r in range(1, height):
        # Iterate through columns, skipping the first and last columns
        # as the rule depends on neighbors c-1 and c+1
        for c in range(1, width - 1):
            # Get the colors of the cells in the *previous* row (r-1) at columns c-1 and c+1
            # Use the state of the grid *before* this row's calculations began
            # In this implementation structure, we read from output_grid[r-1, ...]
            # because the row r-1 has already been fully processed in the previous iteration.
            color_left = output_grid[r - 1, c - 1]
            color_right = output_grid[r - 1, c + 1]

            # Check if both influencing cells are non-orange
            if color_left != ORANGE and color_right != ORANGE:
                # Apply the transformation rules
                if color_left == RED and color_right == RED:
                    output_grid[r, c] = GRAY
                elif color_left == GRAY and color_right == GRAY:
                    output_grid[r, c] = RED
                elif color_left == GRAY and color_right == RED:
                    output_grid[r, c] = RED
                elif color_left == RED and color_right == GRAY:
                    output_grid[r, c] = GRAY
                # If the combination is not one of the above (e.g., one is orange),
                # the cell output_grid[r, c] remains as it was initialized (copied from input)

    # Return the modified grid
    return output_grid