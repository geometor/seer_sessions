"""
Propagate colored pixels downwards in a cascading pattern.

1. Create a copy of the input grid; this will be the working output grid.
2. Iterate through each row of the working grid, from the top row (row index 0) 
   down to the second-to-last row (row index height - 2). Let the current 
   row index be r.
3. Within each row r, iterate through each column (column index c) from left 
   to right (index 0 to width - 1).
4. Examine the pixel at position (r, c) in the working grid. Let its color 
   be current_color.
5. If current_color is not white (0):
   a. Consider the target position (r + 1, c - 1) (down-left).
      i. Check if this position is within the grid boundaries.
      ii. If it is within bounds, check the color of the pixel at 
          (r + 1, c - 1) in the working grid.
      iii. If the color at (r + 1, c - 1) is white (0), change its color 
           to current_color.
   b. Consider the target position (r + 1, c + 1) (down-right).
      i. Check if this position is within the grid boundaries.
      ii. If it is within bounds, check the color of the pixel at 
          (r + 1, c + 1) in the working grid.
      iii. If the color at (r + 1, c + 1) is white (0), change its color 
           to current_color.
6. After iterating through all relevant rows and columns, the working grid 
   contains the final output. Return this grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a downward cascading propagation rule to colored pixels in a grid.
    
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

    # Iterate through rows from top to second-to-last
    for r in range(height - 1):
        # Iterate through columns
        for c in range(width):
            # Get the color of the current pixel in the potentially modified grid
            current_color = output_grid[r, c]

            # If the current pixel is not white (background)
            if current_color != 0:
                # --- Check and potentially color the down-left position ---
                target_r_dl = r + 1
                target_c_dl = c - 1

                # Check if down-left target is within grid bounds
                if 0 <= target_c_dl < width: # target_r_dl is always < height here
                    # Check if the target pixel in the output grid is currently white
                    if output_grid[target_r_dl, target_c_dl] == 0:
                        # Change the target pixel's color to the current color
                        output_grid[target_r_dl, target_c_dl] = current_color

                # --- Check and potentially color the down-right position ---
                target_r_dr = r + 1
                target_c_dr = c + 1

                # Check if down-right target is within grid bounds
                if 0 <= target_c_dr < width: # target_r_dr is always < height here
                     # Check if the target pixel in the output grid is currently white
                    if output_grid[target_r_dr, target_c_dr] == 0:
                        # Change the target pixel's color to the current color
                        output_grid[target_r_dr, target_c_dr] = current_color

    return output_grid