"""
Expands a rectangular shape of red and blue pixels downwards by four rows,
propagating the internal pattern, and removes a single azure pixel.
"""

import numpy as np

def find_shape(grid, colors):
    # Find the bounding box of a shape defined by a set of colors.
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in colors:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if max_row == -1:  # No shape found
        return None

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the rectangular shape with red and blue pixels
    shape_bbox = find_shape(input_grid, [1, 2])

    if shape_bbox:
        min_row, min_col, max_row, max_col = shape_bbox

        # Expand the shape downwards by four rows
        new_max_row = max_row + 4

        # Ensure the new dimensions don't exceed the grid boundaries
        new_max_row = min(new_max_row, output_grid.shape[0] - 1)

        # Propagate the internal pattern of the shape
        for r in range(max_row + 1, new_max_row + 1):
            for c in range(min_col, max_col + 1):
                if c == min_col + 1 or c == min_col + 2:  # Center columns are blue
                    output_grid[r, c] = 1
                else:  # Outer columns are red
                    output_grid[r, c] = 2

    # Remove the azure pixel (set it to white/0)
    for r in range(output_grid.shape[0]):
      for c in range(output_grid.shape[1]):
        if output_grid[r,c] == 8:
            output_grid[r,c] = 0


    return output_grid