"""
The transformation draws an L-shaped yellow line (4) connecting an azure pixel (8) to a position adjacent to a red pixel (2).
The azure and red pixels remain in their original positions. The L shape is formed by first drawing a vertical line upwards from the
azure pixel and stopping one row above the red pixel. Then a horizontal line to the right from the end of the vertical line,
stopping at the column where the red pixel is.
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])  # Return first instance as (row, col)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure and red pixels.
    azure_pixel = find_pixel(input_grid, 8)
    red_pixel = find_pixel(input_grid, 2)

    if azure_pixel is None or red_pixel is None:
        return output_grid # Return original if pixels are not found

    # Draw the vertical part of the L.
    for row in range(red_pixel[0] + 1, azure_pixel[0]):
        output_grid[row, azure_pixel[1]] = 4

    #Draw horizontal part of the L
    for col in range(azure_pixel[1] + 1, red_pixel[1]):
        output_grid[red_pixel[0]+1, col] = 4

    return output_grid