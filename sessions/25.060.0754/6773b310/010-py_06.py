"""
Divides the input grid into nine sections (3x3 meta-grid).
For each section:
    - If the section contains any azure (8) pixels, the output grid has a blue (1) pixel.
    - Otherwise, the output grid has a white (0) pixel.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Calculate section boundaries.  Use // for integer division
    row_step = rows // 3
    col_step = cols // 3

    # Iterate through the 9 sections
    for i in range(3):
        for j in range(3):
            # Define row and column boundaries for the current section
            row_start = i * row_step
            row_end = (i + 1) * row_step if i < 2 else rows # edge condition
            col_start = j * col_step
            col_end = (j + 1) * col_step if j < 2 else cols # edge condition

            # Extract the current section
            section = input_grid[row_start:row_end, col_start:col_end]

            # Check for the presence of azure (8) in the section
            if np.any(section == 8):
                output_grid[i, j] = 1  # Set to blue (1)

    return output_grid.tolist()