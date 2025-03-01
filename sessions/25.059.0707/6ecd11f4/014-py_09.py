"""
Identify all non-white pixels in the input grid. Determine the bounding box encompassing these pixels. Create an output grid of the same size as the bounding box. Copy the non-white pixels from the input grid to the output grid, preserving their relative positions within the bounding box.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # 1. Identify Non-White Pixels
    non_white_pixels = []
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 0:
                non_white_pixels.append((i, j, input_grid[i, j]))

    # 2. Determine Bounding Box
    if not non_white_pixels:  # Handle the case where there are no non-white pixels
        return [[]] # based on prior - empty grid is a 1x1 of value 0.

    min_row, min_col, _ = min(non_white_pixels, key=lambda x: (x[0], x[1]))
    max_row, max_col, _ = max(non_white_pixels, key=lambda x: (x[0], x[1]))

    # 3. Create Output Grid
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 4. Copy Pixels
    for row, col, value in non_white_pixels:
        output_row = row - min_row
        output_col = col - min_col
        output_grid[output_row, output_col] = value

    return output_grid.tolist()