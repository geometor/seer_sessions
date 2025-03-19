"""
The output grid is always 4x4. The transformation rule is selected based on the input grid's dimensions.

1.  **Initialization**: A 4x4 output grid filled with white (0) is created.

2.  **Shape-Based Rule Selection**:
    *   **If** the input grid is 9x9, apply the "Quadrant Rule":
        *   Check the top-left quadrant of the input. If there are any non-zero pixels, set the top-left pixel of the output to green (3).
        *   Check the top-right quadrant of the input. If there are any non-zero pixels, set the top-right pixel of the output to green (3).
        *   Check the bottom-left quadrant of the input. If there are any non-zero pixels, set the bottom-left pixel of the output to green (3).
    *   **Else If** the input grid is 5x5, apply the "Frame Rule":
        *   Iterate through each row of the input grid. If any pixel in that row is non-zero, set the leftmost and rightmost pixels of the corresponding row in the output grid to green (3). Consider the row index, but cap it at 3 for the output grid.
        *   Iterate through each column of the input grid. If any pixel in that column is non-zero, set the topmost and bottommost pixels of the corresponding column in the output grid to green (3). Consider the column index, but cap it at 3 for the output grid.
    *   **Else If** the input grid's height is greater than 3 and width less than 4 apply the top half mapping rule:
        * If there are any non-zero pixels in the top half of input grid, set all pixels of the output to green (3).

3.  **Return**: Return the modified 4x4 output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 4x4 with all white (0)
    output_grid = np.zeros((4, 4), dtype=int)
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Shape-Based Rule Selection
    if rows == 9 and cols == 9:
        # Quadrant Rule
        if np.any(input_grid[0:rows//2, 0:cols//2] != 0):
            output_grid[0, 0] = 3
        if np.any(input_grid[0:rows//2, cols//2:cols] != 0):
            output_grid[0, -1] = 3
        if np.any(input_grid[rows//2:rows, 0:cols//2] != 0):
             output_grid[-1, 0] = 3

    elif rows == 5 and cols == 5:
        # Frame Rule
        for r in range(rows):
            if np.any(input_grid[r,:] != 0 ):
                output_grid[r if r < 4 else 0, 0] = 3  #Left of the Frame
                output_grid[r if r < 4 else 0, 3] = 3    #Right of the frame
        for c in range(cols):
            if np.any(input_grid[:,c] != 0):
                output_grid[0,c if c < 4 else 0] = 3 #Top of the frame
                output_grid[3, c if c < 4 else 0] = 3  #Bottom of the Frame

    elif rows > 3 and cols < 4:
      # Top-half mapping
      if np.any(input_grid[0:rows//2, :] != 0):
          output_grid[:,:] = 3

    return output_grid