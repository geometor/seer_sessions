"""
The transformation rule appears to involve preserving specific parts, mostly yellow and some blues pixels and create a new grid.
"""

import numpy as np

def find_objects(grid, color):
    """Find contiguous regions of the specified color."""
    mask = (grid == color)
    labeled_mask, num_labels = measure.label(mask, connectivity=1, return_num=True)
    objects = []
    for i in range(1, num_labels + 1):
        obj_coords = np.where(labeled_mask == i)
        objects.append(list(zip(obj_coords[0], obj_coords[1])))
    return objects


def transform(input_grid):
    """Transforms the input grid by keeping parts that contain mostly yellow and some blue pixels."""

    # Initialize variables
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.full((rows,1),-1)
    col_index = 0

    # loop through input columns:
    for j in range(cols):
        temp_col = []
        for i in range(rows):
            # Keep every value
            if input_grid[i,j] != 7:
                temp_col.append(input_grid[i,j])
            else:
                temp_col.append(-1)

        #add col to output
        if len(temp_col) > 0:
            if output_grid.shape[1] < col_index + 1:
                output_grid = np.column_stack((output_grid, np.full((rows, 1), -1)))  # Add a new empty column
            output_grid[:,col_index] = temp_col
            col_index += 1

    #remove unused columns
    output_grid = output_grid[:, (output_grid != -1).any(axis=0)]


    return output_grid.tolist()