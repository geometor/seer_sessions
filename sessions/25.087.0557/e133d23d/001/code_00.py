"""
Combine information from two halves of an input grid, separated by a yellow line, based on specific color conditions.

1. Identify the vertical column composed entirely of yellow (4) pixels in the input grid. This column serves as a separator.
2. Define the 'left subgrid' as the rectangular region of the input grid to the left of the yellow separator column.
3. Define the 'right subgrid' as the rectangular region of the input grid to the right of the yellow separator column.
4. Create a new output grid with the same dimensions as the left (and right) subgrids. Initialize all its pixels to white (0).
5. Iterate through each row `r` and column `c` within the dimensions of the subgrids.
6. For each position `(r, c)`:
    a. Check the color of the pixel at `(r, c)` in the 'left subgrid'.
    b. Check the color of the pixel at `(r, c)` in the 'right subgrid'.
    c. If the pixel in the 'left subgrid' is magenta (6) OR the pixel in the 'right subgrid' is azure (8), set the pixel at `(r, c)` in the output grid to red (2).
7. The final state of the new grid is the result.
"""

import numpy as np

# Color constants
WHITE = 0
MAGENTA = 6
YELLOW = 4
AZURE = 8
RED = 2

def find_separator_column(grid):
    """Finds the index of the vertical column made entirely of yellow."""
    height, width = grid.shape
    for c in range(width):
        is_separator = True
        for r in range(height):
            if grid[r, c] != YELLOW:
                is_separator = False
                break
        if is_separator:
            return c
    return -1 # Should not happen based on task description

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    Combines two subgrids based on color conditions (magenta OR azure -> red).
    """
    input_grid = np.array(input_grid) # Ensure it's a numpy array
    height, width = input_grid.shape

    # 1. Identify the vertical yellow separator column.
    separator_col = find_separator_column(input_grid)
    if separator_col == -1:
        # Handle error case if separator not found, though priors suggest it always exists
        print("Error: Yellow separator column not found.")
        return input_grid # Or raise an error

    # 2. Define the 'left subgrid'.
    left_subgrid = input_grid[:, 0:separator_col]

    # 3. Define the 'right subgrid'.
    right_subgrid = input_grid[:, separator_col + 1:width]

    # Ensure subgrids have expected dimensions (should be same)
    subgrid_height, subgrid_width = left_subgrid.shape
    if left_subgrid.shape != right_subgrid.shape:
         print("Error: Subgrids have different dimensions.")
         # Handle error
         return input_grid

    # 4. Create a new output grid, initialized to white.
    output_grid = np.full((subgrid_height, subgrid_width), WHITE, dtype=int)

    # 5. Iterate through each position (r, c) in the subgrids.
    for r in range(subgrid_height):
        for c in range(subgrid_width):
            # 6a. Check pixel in left subgrid.
            left_pixel = left_subgrid[r, c]
            # 6b. Check pixel in right subgrid.
            right_pixel = right_subgrid[r, c]

            # 6c. Apply the OR condition.
            if left_pixel == MAGENTA or right_pixel == AZURE:
                output_grid[r, c] = RED
            # Otherwise, it remains WHITE (already initialized)

    # 7. Return the final output grid.
    return output_grid.tolist() # Convert back to list of lists for consistency