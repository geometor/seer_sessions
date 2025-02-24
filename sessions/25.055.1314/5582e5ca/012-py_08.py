"""
The transformation rule identifies the topmost non-zero color in the input grid and replicates that color across its entire row in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by replicating the topmost non-zero color across its row.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                # Found the topmost non-zero color in this row.
                topmost_color = input_grid[r, c]
                # Replicate the color across the entire row.
                output_grid[r, :] = topmost_color
                break  # Move to the next row after finding the first non-zero color.

    return output_grid.tolist()