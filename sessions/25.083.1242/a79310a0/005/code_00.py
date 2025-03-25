"""
Transforms the input grid by replacing an azure object with a red object of the same shape.
The red object is placed starting at row 1, column 0 of the output grid.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    # Calculate the bounding box of the object.
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    # Extract the object's shape.
    obj = grid[min_row:max_row+1, min_col:max_col+1]
    return obj, min_row, max_row, min_col

def transform(input_grid):
    input_grid = np.array(input_grid)
    # Find the azure object.
    azure_object, _, _, _ = find_object(input_grid, 8)

    # Initialize the output grid with all black pixels.
    output_grid = np.zeros_like(input_grid)

    if azure_object is not None:
        # Create the red object of the same shape.
        red_object = np.where(azure_object == 8, 2, azure_object)
        height = red_object.shape[0]
        width = red_object.shape[1]
        rows, cols = output_grid.shape

        # Place the red object in the output grid, starting at row 1, column 0.
        new_row = 1
        new_col = 0
        for r in range(min(height, rows - new_row)):
            for c in range(min(width, cols - new_col)):
                output_grid[new_row + r, new_col + c] = red_object[r, c]

    return output_grid.tolist()