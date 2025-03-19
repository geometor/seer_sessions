"""
1. Identify Red Pixels: Locate all pixels within the input grid that have a value of 2 (red).
2. Apply Gravity to Red Pixels: Red pixels are subject to gravity and will "fall" to the lowest possible position within their column.
3. Transform White Pixels: Any white pixels (value 0) that are directly below a red pixel, in the red pixel's path due to gravity, are changed to blue pixels (value 1).
4. All Other Pixels: all other pixels are unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the gravity rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column.
    for col in range(cols):
        # Find red pixels in the current column.
        red_pixels_rows = [row for row in range(rows) if input_grid[row, col] == 2]

        # Apply gravity to each red pixel.
        for red_row in red_pixels_rows:
            # Determine the lowest possible position for the red pixel.
            lowest_row = rows - 1
            for row_below in range(red_row + 1, rows):
                if input_grid[row_below, col] != 0 and input_grid[row_below, col] != 2 : # if there is a blocking pixel, stop
                    lowest_row = row_below -1
                    break
                elif input_grid[row_below,col] == 2:
                    lowest_row = row_below
                
            # Change white pixels below the red pixel to blue.
            for row_below in range(red_row + 1, lowest_row + 1):
                if output_grid[row_below, col] == 0:
                    output_grid[row_below, col] = 1

    return output_grid