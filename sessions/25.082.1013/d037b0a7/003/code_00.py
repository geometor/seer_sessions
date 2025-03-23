"""
1.  **Identify Non-Zero Pixels:** Find all pixels with a value other than 0.
2. **Conditional Horizontal Propagation** If a non-zero pixel is found, fill that pixel's value horizontally leftwards in that row. This leftward spread stops at the left edge of the input, or if any non-zero pixels are in the way.
3.  **Vertical Propagation:** For *every* non-zero pixel in the input grid, propagate its value downwards to the bottom of the grid.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Horizontal Propagation (Leftwards)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                #fill left
                for k in range(c -1, -1, -1):
                    if output_grid[r,k] == 0:
                        output_grid[r,k] = input_grid[r,c]
                    else:
                        break

    # Vertical Propagation (Downwards)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:  # Use input_grid for the trigger
                for k in range(r + 1, rows):
                    output_grid[k, c] = output_grid[r,c]


    return output_grid