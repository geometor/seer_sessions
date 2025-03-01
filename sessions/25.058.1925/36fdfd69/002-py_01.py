"""
Finds connected components/regions of color, and replaces the color of any such color regions of size 1 of color 2, 3 or 8 to 4.
"""

import numpy as np
from scipy.ndimage import measurements

def get_neighbors(r, c, rows, cols):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid by changing the color of isolated color blocks.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    labeled_grid, num_labels = measurements.label(input_grid)
    object_slices = measurements.find_objects(labeled_grid)

    for label in range(1,num_labels+1):

        current_slice = object_slices[label-1]
        region = input_grid[current_slice]

        # check isolated block
        size = region.size
        color = region.flatten()[0]

        if (size == 1):
           r, c = current_slice[0].start, current_slice[1].start
           if color in [2,3,8]:
               output_grid[r,c] = 4

    return output_grid.tolist()