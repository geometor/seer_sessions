"""
The transformation rule identifies azure pixels. The first encountered azure pixel will be transformed. One green pixel will be generated directly to the right, and one green pixel will be generated directly below, of the azure pixel. All other azure pixels remain unchanged. Other color blocks, such as red, also remain unchanged.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color).tolist()

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    azure_pixels = find_pixels_by_color(input_grid, 8)

    # Transform only the first encountered azure pixel
    if azure_pixels:
        row, col = azure_pixels[0]

        # Generate green pixel to the right
        if col + 1 < output_grid.shape[1]:
            output_grid[row, col + 1] = 3

        # Generate green pixels downwards
        if row + 1 < output_grid.shape[0]:
            output_grid[row + 1, col] = 3

    return output_grid