"""
Copies the input grid to the output grid, then changes some gray (5) pixels to green (3) based on their position relative to other gray pixels. Gray pixels are changed to green if they have gray neighbors along certain directions and certain locations.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    # Iterate through each cell of the input grid.
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is gray (5).
            if input_grid[r, c] == 5:
                # Check First column, change to 3.
                if c > 0 and input_grid[r,c-1] == 5 :
                  output_grid[r,c] = 3
                #Check for the diognal.
                if r > 0 and c < cols - 1 and input_grid[r - 1, c + 1] == 5:
                   output_grid[r-1,c] = 3
                if r < rows-1 and c > 0 and input_grid[r+1,c-1] == 5:
                   output_grid[r,c] = 3


    return output_grid