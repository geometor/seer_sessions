"""
1.  Identify the horizontal yellow line: Scan the input grid to find a row where all non-zero pixels are yellow (color 4). This is the reflection axis. If no such line exists, no transformation occurs.
2.  Reflect across the line: For each pixel *above* the yellow line that is *not* yellow and *not* black (color 0):
    *   Calculate its vertical distance (number of rows) to the yellow line.
    *   Find the position that is the *same* vertical distance *below* the yellow line, and the *same* horizontal position (column).
    *   Change the pixel at that new position to be the same color as the original pixel.
3.  Leave the Yellow line intact: The yellow line itself does not move or change.
4. Leave all other cells as they are: All other pixels in the image that aren't part of the reflection remain in their original positions and retain their original colors.
"""

import numpy as np

def find_yellow_line(grid):
    # Iterate through rows to find a row where all non-zero pixels are yellow (4)
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row if pixel != 0):
            return i
    return -1  # Return -1 if no yellow line is found

def transform(input_grid):
    """
    Transforms the input grid by reflecting non-yellow, non-black pixels above a horizontal yellow line across that line.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    yellow_line_row = find_yellow_line(input_grid)

    if yellow_line_row == -1:
        return output_grid # No transformation if no yellow line

    # Iterate through the input grid above the yellow line
    for r in range(yellow_line_row):
        for c in range(input_grid.shape[1]):
             # Reflect non-yellow, non-black pixels
            if input_grid[r, c] != 4 and input_grid[r,c] != 0:
                distance = yellow_line_row - r
                new_row = yellow_line_row + distance
                # Check bounds: Ensure new_row is within grid dimensions
                if new_row < output_grid.shape[0]:
                  output_grid[new_row, c] = input_grid[r, c]

    return output_grid