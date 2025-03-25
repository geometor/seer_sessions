"""
Transforms an input grid by generating a pattern of '1's and '5's based on the positions of '5's in the input grid. '5's are copied from input to output, and '1's are placed adjacent to '5's in a checkerboard-like fashion.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the location of '5's.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Copy '5's directly
            if input_grid[r, c] == 5:
                output_grid[r, c] = 5
            # Check for '5' in the previous position in the same row
            elif c > 0 and input_grid[r, c - 1] == 5:
                output_grid[r, c] = 1
            # check for '5' in next position on same row
            elif c < cols - 1 and input_grid[r, c+1] == 5:
                output_grid[r,c] = 1
            # Check for '5' in the previous position in the next row
            elif r < rows - 1 and c > 0 and input_grid[r + 1, c - 1] == 5:
                output_grid[r, c] = 1
            # Check for 5 in current position of next row
            elif r < rows - 1 and input_grid[r+1,c] == 5:
                output_grid[r,c] = 5
            #check for '5' in next position on next row
            elif r < rows - 1 and c < cols - 1 and input_grid[r+1, c+1] == 5:
                output_grid[r,c] = 1


    return output_grid.tolist()