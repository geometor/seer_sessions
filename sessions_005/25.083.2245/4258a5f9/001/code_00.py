"""
The transformation rule identifies all '5' (gray) pixels in the input grid. 
Each '5' pixel is copied to the output grid in the same location. Then a 3x3 
block of '1' (blue) pixels, centered on the '5', is created in the output. 
Finally, any '0' (white) pixel in the input that's directly adjacent to the 3x3 
block is also converted to '1' (blue) in the output.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the 8 neighbors of a pixel (Moore neighborhood).
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Initialize output with 1s where 5s are present
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r,c] = 5

    # Iterate on input pixels.
    for r in range(rows):
        for c in range(cols):
            # Create the 3x3 blue block around the '5'.
            if input_grid[r,c] == 5:
                for i in range(max(0, r - 1), min(rows, r + 2)):
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        output_grid[i,j] = 1

    #Expand the blue outwards one additional layer
    output_grid_copy = np.copy(output_grid)
    for r in range(rows):
        for c in range(cols):
            if output_grid_copy[r,c] == 1:
                for nr, nc in get_neighbors(output_grid_copy, r, c):
                    if output_grid_copy[nr, nc] == 0:
                        output_grid[nr,nc] = 1
    return output_grid.tolist()