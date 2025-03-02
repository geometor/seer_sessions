"""
Expands a single-row input grid into a multi-row output grid. The gray (5) region on the left side of the input is extended downwards, creating a rectangular gray area. The remaining cells on the right are filled with white (0), keeping output width consistent.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a single-row input grid into a multi-row output grid.
    
    Args:
        input_grid: A numpy array representing the input grid.
    
    Returns:
        A numpy array representing the output grid.
    """
    # Initialize the output grid with the same width as the input and a height of 5.
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((5, input_width), dtype=int)

    # Find the boundary between gray and white pixels.
    boundary = 0
    for x in range(input_width):
        if input_grid[0, x] == 0:
            break
        boundary += 1

    # Fill the gray region.
    for y in range(5):
        for x in range(boundary):
            output_grid[y, x] = 5

    # The rest of the grid is already initialized to 0 (white), so no further action is needed.

    return output_grid