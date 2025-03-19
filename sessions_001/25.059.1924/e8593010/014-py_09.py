"""
Replaces white (0) pixels in the input grid with red (2), green (3), or blue (1) based on their position, 
leaving gray (5) pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing white pixels with specific colors
    based on their location.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid to find white and gray pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5: #Preserve Gray
                continue
            elif output_grid[r,c] == 0: # process only if white
                if c < 3:
                    if r < rows - 3:
                        output_grid[r, c] = 2  # Leftmost White to Red
                    else:
                        output_grid[r,c] = 1 # Bottom White to Blue
                elif c >= cols - 3:
                    if r < rows - 3:
                        output_grid[r, c] = 3  # Rightmost White to Green
                    else:
                        output_grid[r,c] = 2 #Interior, so red
                else:
                    output_grid[r,c] = 2 #Interior, so red

    return output_grid