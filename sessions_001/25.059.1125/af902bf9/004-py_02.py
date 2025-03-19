"""
1.  **Identify Corner Pixels:** Locate all pixels with the value '4' (yellow) in the input grid.
2.  **Form Rectangle:** Consider these yellow pixels as defining the opposite corners of an implied rectangle.
3.  **Calculate Center:** Determine the center point of this rectangle. The center's row is the average of the yellow pixels rows, and its columns are the average of the yellow pixels' columns.
4.  **Add center object:** Add a red pixel (value '2') to the output at a position determined by the calculated center point.
5.  **Output:** The output grid is a copy of the input grid, with the addition of the red center pixel.
"""

import numpy as np

def find_pixels_by_value(grid, value):
    """Finds coordinates of pixels with a specific value."""
    return np.argwhere(grid == value)

def calculate_center(coordinates):
    """Calculates the center point of a rectangle given corner coordinates."""
    return np.mean(coordinates, axis=0).astype(int)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find corner pixels (value 4)
    corner_pixels = find_pixels_by_value(input_grid, 4)

    # Calculate center point
    if len(corner_pixels) > 0: # handle empty corner case
        center_point = calculate_center(corner_pixels)

        # Add center pixel (value 2)
        output_grid[center_point[0], center_point[1]] = 2

    return output_grid