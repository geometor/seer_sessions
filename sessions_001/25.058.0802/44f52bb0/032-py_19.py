"""
1. Count the number of red pixels (value '2') in the input grid.
2. Count the number of white pixels (value = 0) that are in the corners of the input grid.
3. Add those two counts.
4. The result is the final output value.
"""

import numpy as np

def count_color(grid, color_value):
    """Counts the number of pixels of a specified color in the grid."""
    return np.sum(grid == color_value)

def count_corner_pixels(grid, color_value):
    """Counts the number of pixels of a specific color in the corners of a grid"""
    rows, cols = grid.shape
    count = 0
    if grid[0, 0] == color_value:
        count += 1
    if grid[0, cols - 1] == color_value:
        count += 1
    if grid[rows - 1, 0] == color_value:
        count += 1
    if grid[rows - 1, cols - 1] == color_value:
        count +=1
    return count

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Count red pixels.
    red_count = count_color(input_grid, 2)

    # Count white corner pixels.
    white_corner_count = count_corner_pixels(input_grid, 0)

    # Calculate the output value.
    output_value = red_count + white_corner_count

    return output_value