"""
1.  Identify Red Pixels: Locate all pixels with the color red (value 2) within the input grid.
2.  Determine Bounding Box: Calculate the bounding box that encloses all the red pixels. This is done by finding the minimum and maximum row and column indices of the red pixels.
3.  Create Output Grid: Create a new grid with dimensions equal to the height and width of the bounding box.
4.  Fill with Gray: Fill every cell of the output grid with the color gray (value 5).
"""

import numpy as np

def get_red_pixels(grid):
    """Finds coordinates of all red pixels in the grid."""
    return np.argwhere(grid == 2)

def calculate_bounding_box(red_pixels):
    """Calculates the bounding box dimensions from red pixel coordinates."""
    if len(red_pixels) == 0:
        return 0, 0  # Handle no red pixels case
    min_row = np.min(red_pixels[:, 0])
    max_row = np.max(red_pixels[:, 0])
    min_col = np.min(red_pixels[:, 1])
    max_col = np.max(red_pixels[:, 1])
    return max_row - min_row + 1, max_col - min_col + 1

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # Convert input to numpy array for easier processing
    input_grid = np.array(input_grid)

    # Identify Red Pixels
    red_pixels = get_red_pixels(input_grid)

    # Determine Bounding Box
    height, width = calculate_bounding_box(red_pixels)

    # Create Output Grid and Fill with Gray (handle edge case of no red pixels)
    if height > 0 and width > 0:
      output_grid = np.full((height, width), 5)  # Create and fill with gray
    else:
      output_grid = np.array([])

    return output_grid.tolist()