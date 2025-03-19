"""
1.  Identify Objects: Find all contiguous red (2) blocks/pixels and all yellow (4) pixels in the input grid.
2.  Move Red and Yellow to Row 7 and 8: Move all red and yellow objects to rows 7 and 8. Maintain their original horizontal positions (columns). If the original red block occupies several rows, place those rows starting at row 7.
3.  Clear other pixels: Ensure that all other pixels in the output grid are white (0).
"""

import numpy as np

def find_objects(grid, color):
    """Finds coordinates of all pixels of the specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize the output grid with all white pixels (0).
    output_grid = np.zeros_like(input_grid)
    output_grid[:] = 0

    # Find all red pixels.
    red_pixels = find_objects(input_grid, 2)

    # Find all yellow pixels.
    yellow_pixels = find_objects(input_grid, 4)

    # Move red pixels to rows 7 and 8
    if len(red_pixels) > 0:
        min_row = np.min(red_pixels[:, 0])
        for r, c in red_pixels:
            row_offset = r - min_row
            output_grid[6 + row_offset, c] = 2

    # Move yellow pixels to row 7
    for r, c in yellow_pixels:
        output_grid[6, c] = 4
        
    return output_grid