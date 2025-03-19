"""
1.  **Check for Azure Pixels:** Examine the input grid for the presence of azure (8) pixels.
2.  **Handle No Azure Case:** If there are no azure pixels, create a 1x1 output grid containing a single black (0) pixel.
3.  **Handle Single Azure Pixel Case:** If there is exactly one azure pixel, create a 1x1 output grid containing a single azure (8) pixel.
4.  **Handle Azure Rectangle Case (General):** If there is a contiguous region of azure pixels (forming a rectangle):
    *   Determine the *width* and *height* of this azure rectangle.
    *   Create an output grid with dimensions equal to the width and height of the azure rectangle.
    *   Fill the top row of the output grid with azure (8) pixels.
    *   Fill all the other rows of the output grid with black (0) pixels.
"""

import numpy as np

def find_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels."""
    return np.where(grid == 8)

def find_rectangle_by_color(grid, color):
    """Finds the top-left and bottom-right coordinates of a rectangle of a specific color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No rectangle found
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def transform(input_grid):
    # Find azure pixel coordinates
    azure_rows, azure_cols = find_azure_pixels(input_grid)

    # Handle no azure case
    if len(azure_rows) == 0:
        return np.array([[0]])

    # Handle single azure pixel case
    if len(azure_rows) == 1:
        return np.array([[8]])

    # Handle azure rectangle case
    top_left, bottom_right = find_rectangle_by_color(input_grid, 8)
    height = bottom_right[0] - top_left[0] + 1
    width = bottom_right[1] - top_left[1] + 1
    output_grid = np.zeros((height, width), dtype=int)
    output_grid[0, :] = 8  # Fill top row with azure

    return output_grid