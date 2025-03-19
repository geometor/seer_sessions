"""
1.  **Find all Red Pixels:** Locate all pixels with the color red (2) in the input grid, storing their (row, column) coordinates.
2.  **Find all Green Pixels:** Locate all pixels with the color green (3) in the input grid, storing their (row, column) coordinates.
3.  **Iterate and Draw:**
    *   For each red pixel:
        *   Iterate through all of the green pixels.
        *   If a green pixel's row coordinate is greater than the red pixel's row coordinate:
            *   Draw a vertical line of azure (8) pixels.
            *   The line starts at the row of the red pixel.
            *   The line ends at the row immediately *above* the green pixel.
            *   The line's column is the same as the green pixel's column.
4. **Preserve Other Pixels:** Ensure all other input pixels are in the output.
5. **Handle No Valid Pairs:** If no red pixels, or no green pixels exist, or no valid pairs where a red pixel is above a green pixel exist, return the input grid.
"""

import numpy as np

def find_all_pixels(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.where(grid == color)
    return list(zip(coords[0], coords[1]))

def draw_vertical_line(grid, start_row, end_row, column, color):
    # Draw a vertical line on the grid.
    for row in range(start_row, end_row + 1):
        grid[row, column] = color
    return grid

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all red and green pixels
    red_pixels = find_all_pixels(input_grid, 2)
    green_pixels = find_all_pixels(input_grid, 3)

    if not red_pixels or not green_pixels:
        return output_grid  # Return input if no red or green pixels

    # Iterate through red pixels and then green pixels
    for red_row, red_col in red_pixels:
        for green_row, green_col in green_pixels:
            # Check if the green pixel is below the red pixel
            if green_row > red_row:
                # Draw the azure line
                output_grid = draw_vertical_line(output_grid, red_row, green_row - 1, green_col, 8)

    return output_grid