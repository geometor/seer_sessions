"""
1.  **Identify the Target Color:**
    *   The program scans the top left section of input grid to find connected non-zero color.

2.  **Extract Subgrid:**
    *   Once the target color is located, locate the subgrid by looking at the top left corner and using it as the anchor

3.   **Form the 3 x 3 output grid**.
"""

import numpy as np

def find_top_left_non_zero_color(grid):
    # Iterate through the grid to find the first non-zero color
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return grid[r, c], r, c
    return 0, -1, -1  # Return 0 if no non-zero color is found


def transform(input_grid):
    """
    Transforms the input grid into a 3x3 output grid based on identifying and using the shape
    starting in the top left corner, defined by the non zero color
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the top-left non-zero color and its coordinates
    target_color, start_row, start_col = find_top_left_non_zero_color(input_grid)

    # Initialize the 3x3 output grid with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # if no target color found - just return empty grid
    if target_color == 0:
        return output_grid

    # Extract the 3x3 subgrid
    for r in range(3):
      for c in range(3):
        output_grid[r,c] = input_grid[start_row + r, start_col + c]


    return output_grid