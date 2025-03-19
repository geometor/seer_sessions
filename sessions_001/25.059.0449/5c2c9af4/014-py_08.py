"""
Transforms a grid with sparse red pixels into a grid with red squares,
where the corners of the squares are determined by the locations of the red pixels.
"""

import numpy as np

def find_red_pixels(grid):
    """Finds the coordinates of red pixels in the grid."""
    return np.argwhere(grid == 2)

def draw_filled_square(grid, top_left, bottom_right):
    """Draws a filled square on the grid, given top-left and bottom-right corners."""
    output_grid = np.copy(grid)
    for r in range(top_left[0], bottom_right[0] + 1):
        for c in range(top_left[1], bottom_right[1] + 1):
            output_grid[r, c] = 2  # Set to red
    return output_grid
    
def transform(input_grid):
    """
    Transforms the input grid by identifying red pixels and drawing a filled
    red square whose corners are determined by the min and max coordinates of the red pixels.
    """
    # Find red pixels
    red_pixels = find_red_pixels(input_grid)

    # If no red pixels, return the input grid
    if len(red_pixels) == 0:
        return np.copy(input_grid)

    # Initialize output_grid as all zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Determine top-left and bottom-right corners for the bounding box
    top_left = red_pixels.min(axis=0)
    bottom_right = red_pixels.max(axis=0)

    # Draw the filled square
    output_grid = draw_filled_square(output_grid, top_left, bottom_right)
    
    return output_grid