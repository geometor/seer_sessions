"""
Replace specific yellow (4) pixels with magenta (6) pixels based on their horizontal neighbors.  If a yellow pixel has yellow neighbors on both sides (left and right), it changes to magenta. If a yellow pixel has white neighbors on both sides, it changes to magenta. Otherwise, the pixel remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    # Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is yellow (4)
            if input_grid[r, c] == 4:
                # Check neighbors for yellow pixels
                left_neighbor_yellow = (c > 0 and input_grid[r, c-1] == 4)
                right_neighbor_yellow = (c < cols - 1 and input_grid[r, c+1] == 4)

                # Check neighbors for white pixels
                left_neighbor_white = (c > 0 and input_grid[r, c-1] == 0)
                right_neighbor_white = (c < cols - 1 and input_grid[r, c+1] == 0)
                
                # Apply the transformation rule
                if (left_neighbor_yellow and right_neighbor_yellow) or (left_neighbor_white and right_neighbor_white):
                    output_grid[r, c] = 6

    return output_grid