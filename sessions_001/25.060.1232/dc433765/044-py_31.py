"""
1. Identify Objects: Identify all colored objects in the input grid. An object is defined as a contiguous block of pixels of the same color.
2. Consolidate Green: All green objects are consolidated into a single green pixel.
3. Preserve Other Colors: All other colored pixels, besides green, maintain their original positions and colors in the output grid.
4. Green Pixel Position: The single green pixel is placed in the grid at the following coordinates: row = ((number of input rows)//2) and column = ((number of input cols)//2).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the center coordinates
    center_row, center_col = rows // 2, cols // 2

    # Flag to check if green pixel is placed
    green_placed = False

    # Iterate through the input grid
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 3:  # Green pixel
                # Place only one green pixel in the center
                if not green_placed:
                    output_grid[center_row, center_col] = 3
                    green_placed = True
            elif input_grid[i,j] != 0:
                output_grid[i,j] = input_grid[i,j]

    return output_grid