"""
1. Identify the Horizontal Yellow Line: Find the row index of the horizontal line where all pixels are yellow (color 4).
2. Mirror Above to Below: For each column, reflect the pixels located *above* the yellow line across the yellow line and copy these mirrored pixel values to the corresponding positions *below* the yellow line. Specifically, if a pixel is *n* rows above the yellow line, its mirrored value should be placed *n* rows below the yellow line.
"""

import numpy as np

def find_yellow_line(grid):
    """Finds the row index of the horizontal yellow line."""
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row):
            return i
    return -1  # Should not happen in these examples

def transform(input_grid):
    """Transforms the input grid according to the mirroring rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    yellow_line_row = find_yellow_line(input_grid)

    # Iterate through columns
    for col in range(input_grid.shape[1]):
        # Iterate through rows above the yellow line
        for row in range(yellow_line_row):
            # Calculate corresponding location below yellow line
            mirror_row = yellow_line_row + (yellow_line_row - row)
            # Check if the mirrored position is within the grid bounds
            if mirror_row < output_grid.shape[0]:
                # Copy the pixel value from above the line to below
                output_grid[mirror_row, col] = input_grid[row, col]

    return output_grid.tolist()