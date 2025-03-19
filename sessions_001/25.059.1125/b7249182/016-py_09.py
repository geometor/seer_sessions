"""
1.  **Identify Non-Zero Pixels:** Find all pixels in the input grid that have a value other than 0.
2.  **Create Crosses:** For each non-zero pixel:
    *   Create a cross shape centered at the pixel's original location.
    *   Extend a horizontal line and a vertical line, both composed of pixels of the *same color* as the original pixel.
    *   The output crosses are of fixed height/width of 3 pixels.

The cross is formed by 3 horizontal and 3 vertical connected pixels of the same value.
"""

import numpy as np

def find_non_zero_pixels(grid):
    """Finds the coordinates and values of non-zero pixels in a grid."""
    non_zero_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value != 0:
                non_zero_pixels.append(((row_index, col_index), value))
    return non_zero_pixels

def create_cross(grid, center, value):
    """Creates a cross shape in the grid centered at the given coordinates."""
    row, col = center
    height, width = grid.shape
    
    #grid[row, :] = value # full extent
    for i in range(max(0, col - 3), min(width, col + 4)):
        grid[row,i] = value # extend 3 each side

    #grid[:, col] = value # full extent
    for i in range(max(0, row - 3), min(height, row + 4)):
        grid[i,col] = value


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)

    # Find non-zero pixels
    non_zero_pixels = find_non_zero_pixels(input_grid)

    # Create crosses for each non-zero pixel
    for (row, col), value in non_zero_pixels:
        create_cross(output_grid, (row, col), value)

    return output_grid