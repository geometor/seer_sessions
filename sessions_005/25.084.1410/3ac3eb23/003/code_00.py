"""
Simulates a downward diagonal cascade propagation process on a grid.

The transformation proceeds row by row, starting from the second row (index 1).
For each cell in the current row, its final color is determined based on the 
colors of the two cells diagonally above it (up-left and up-right) in the 
*previous* row's state.

1. Initialize the output grid as a copy of the input grid.
2. Iterate through rows `r` from 1 to `height - 1`.
3. Iterate through columns `c` from 0 to `width - 1`.
4. For the current cell `(r, c)` in the output grid:
   a. Only consider changing the cell if it is currently white (0). If it's 
      already colored from the input, skip it.
   b. Get the color `color_ul` from the cell diagonally up-left `(r-1, c-1)`. 
      Treat out-of-bounds positions as white (0).
   c. Get the color `color_ur` from the cell diagonally up-right `(r-1, c+1)`. 
      Treat out-of-bounds positions as white (0).
   d. Determine the color for `output_grid[r, c]`:
      - If only one of `color_ul` or `color_ur` is non-white, set 
        `output_grid[r, c]` to that non-white color.
      - If both `color_ul` and `color_ur` are non-white and they are the 
        *same* color, set `output_grid[r, c]` to that color.
      - If both `color_ul` and `color_ur` are white, or if they are non-white 
        but *different* colors, `output_grid[r, c]` remains white (0).
5. Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a row-by-row downward diagonal cascade simulation.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()
    height, width = grid.shape

    # Iterate through rows starting from the second row (index 1)
    for r in range(1, height):
        # Iterate through columns
        for c in range(width):
            
            # Only modify cells that are currently white in the output grid
            # This preserves any initial colors placed below the top row
            if output_grid[r, c] == 0:
                
                # Get color from diagonally up-left, handling boundary
                if c - 1 < 0:
                    color_ul = 0
                else:
                    # Important: Use output_grid[r-1, ...] to get the state 
                    # from the previous simulation step (row)
                    color_ul = output_grid[r-1, c-1] 

                # Get color from diagonally up-right, handling boundary
                if c + 1 >= width:
                    color_ur = 0
                else:
                     # Use output_grid[r-1, ...]
                    color_ur = output_grid[r-1, c+1]

                # --- Apply coloring rules ---
                
                # Case 1: Only up-left has color
                if color_ul != 0 and color_ur == 0:
                    output_grid[r, c] = color_ul
                # Case 2: Only up-right has color
                elif color_ul == 0 and color_ur != 0:
                    output_grid[r, c] = color_ur
                # Case 3: Both have color
                elif color_ul != 0 and color_ur != 0:
                    # Subcase 3a: Both have the SAME color
                    if color_ul == color_ur:
                        output_grid[r, c] = color_ul
                    # Subcase 3b: Different colors - cell remains white (0)
                    # No action needed as output_grid[r, c] is already 0
                # Case 4: Both are white - cell remains white (0)
                # No action needed

    return output_grid
