"""
1.  **Identify Green Pixels**: Locate all pixels with a value of 3 (green) within the input grid.
2. **Determine the Overall Center:** calculate the center point by getting the minimum and maximum of both row and column.
3.  **Transform Based on Quadrant**: For each green pixel:
    *   If the pixel is in the top-left relative to the calculated center, change its color to magenta (6).
    *    If the pixel is in the top-right or bottom-left, change its color to blue (1).
    *   If the pixel is the bottom-right relative to the center, change its color to red (2).
4.  **Output**: The output grid is the input grid with the green pixels transformed according to the quadrant rule.
"""

import numpy as np

def get_green_pixels(grid):
    """Finds the coordinates of all green pixels in the grid."""
    green_pixels = np.where(grid == 3)
    return list(zip(green_pixels[0], green_pixels[1]))

def calculate_center(coords):
    """Calculates the center (average row and column) of a list of coordinates."""
    if not coords:
        return None, None
    min_row = min(coords, key=lambda p: p[0])[0]
    max_row = max(coords, key=lambda p: p[0])[0]
    min_col = min(coords, key=lambda p: p[1])[1]
    max_col = max(coords, key=lambda p: p[1])[1]
    center_row = (min_row + max_row) / 2
    center_col = (min_col + max_col) / 2
    return center_row, center_col

def transform_pixel(row, col, center_row, center_col):
    """Determines the new color of a pixel based on its position relative to the center."""
    if row <= center_row and col <= center_col:
        return 6  # Magenta
    elif (row > center_row and col <= center_col) or (row <= center_row and col > center_col):
        return 1  # Blue
    else:
        return 2  # Red

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all green pixels
    green_pixels = get_green_pixels(input_grid)

    # Calculate the overall center of green pixels
    center_row, center_col = calculate_center(green_pixels)
    
    if center_row is None or center_col is None:
        return output_grid

    # Transform each green pixel based on its quadrant
    for row, col in green_pixels:
        new_color = transform_pixel(row, col, center_row, center_col)
        output_grid[row, col] = new_color

    return output_grid