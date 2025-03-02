"""
Expands a single-row input grid into a multi-row output grid. The leftmost region of the input, defined by a contiguous sequence of identical colored pixels, is extended downwards, creating a rectangular area of the same color. The remaining cells on the right, starting from where the color changes in the input, are filled with white (0), keeping the output width consistent with the input width. The height of the output grid is equal to the number of pixels of the initial color in the input row.
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
    input_height, input_width = input_grid.shape
    
    # Determine the fill color and boundary.
    fill_color = input_grid[0, 0]
    boundary = 0
    for x in range(input_width):
        if input_grid[0, x] != fill_color:
            break
        boundary += 1

    # Determine output height (number of fill color pixels).
    output_height = boundary

    # Initialize the output grid.
    output_grid = np.zeros((output_height, input_width), dtype=int)

    # Fill the region with the fill color.
    for y in range(output_height):
        for x in range(boundary):
            output_grid[y, x] = fill_color

    return output_grid