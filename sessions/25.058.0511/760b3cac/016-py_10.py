"""
The transformation involves manipulating two shapes, one azure (8) and one yellow (4), on a white (0) background grid. The yellow shape remains unchanged. The azure shape's bounding box is determined, and a new azure line is created one row above the original bounding box.
"""

import numpy as np

def find_shape(grid, color):
    # Find the coordinates of pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
      return None
    return coords

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure (8) and yellow (4) shapes.
    azure_coords = find_shape(input_grid, 8)
    yellow_coords = find_shape(input_grid, 4)

    # maintain yellow shape
    if yellow_coords is not None:
        for r, c in yellow_coords:
            output_grid[r,c] = 4

    # Transform the azure shape.
    if azure_coords is not None:
        # remove original
        for r, c in azure_coords:
           output_grid[r,c] = 0

        # Find the bounding box
        min_row = np.min(azure_coords[:, 0])
        max_row = np.max(azure_coords[:, 0])
        min_col = np.min(azure_coords[:, 1])
        max_col = np.max(azure_coords[:, 1])

        # fill new row above
        new_row = min_row - 1
        if new_row >= 0:
            for c in range(min_col, max_col + 1):
                output_grid[new_row, c] = 8
    

    return output_grid