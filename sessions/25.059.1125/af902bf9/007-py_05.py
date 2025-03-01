"""
1.  Identify Yellow Pixels: Locate all pixels in the input grid that have a value of 4 (yellow).
2.  Check for Presence: If no yellow pixels are found, the transformation is complete, and the output grid is identical to the input grid.
3.  Calculate Center: If yellow pixels are present, calculate the geometric center (center of mass) of the shape they form. This is done by averaging the row and column indices of all yellow pixels.
4. Copy Input: Create a copy of the input as the output grid.
5.  Add Red Pixel: Change the pixel at the calculated center coordinates in the *output grid* to a value of 2 (red).
6.  Return Output: The modified grid, with the added red pixel (or the original if no yellow pixels were present), is the output.
"""

import numpy as np

def find_pixels_by_value(grid, value):
    """Finds coordinates of pixels with a specific value."""
    return np.argwhere(grid == value)

def calculate_center(coordinates):
    """Calculates the center point of a set of coordinates."""
    return np.mean(coordinates, axis=0).astype(int)

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find yellow pixels (value 4)
    yellow_pixels = find_pixels_by_value(input_grid, 4)

    # Check for presence of yellow pixels
    if yellow_pixels.size == 0:
        return output_grid  # Return input grid if no yellow pixels are found
    else:
      # Calculate center point
        center_point = calculate_center(yellow_pixels)

        # Add red pixel (value 2) at the center
        output_grid[center_point[0], center_point[1]] = 2

    return output_grid