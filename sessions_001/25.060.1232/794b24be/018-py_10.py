"""
Transforms an input grid by identifying the topmost-leftmost blue pixel and replacing it with a 1x2 red rectangle.
All other pixels remain unchanged.
"""

import numpy as np

def find_topmost_leftmost_blue(grid):
    """Finds the topmost-leftmost blue pixel in a grid."""
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
        return None  # No blue pixels found

    # Find the minimum row index (topmost)
    min_row = np.min(blue_pixels[:, 0])

    # Filter pixels to only include those on the topmost row
    topmost_pixels = blue_pixels[blue_pixels[:, 0] == min_row]

    # Find the minimum column index among the topmost pixels (leftmost)
    min_col = np.min(topmost_pixels[:, 1])

    return (min_row, min_col)


def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)  # Initialize output grid as a copy
    topmost_leftmost_blue = find_topmost_leftmost_blue(input_grid)

    if topmost_leftmost_blue:
        row, col = topmost_leftmost_blue
        # Create the 1x2 red rectangle, handling potential boundary issues
        output_grid[row, col] = 2  # set first red pixel
        if col + 1 < output_grid.shape[1]:
              output_grid[row, col+1] = 2  # Set the second red pixel (right neighbor)
        

    return output_grid