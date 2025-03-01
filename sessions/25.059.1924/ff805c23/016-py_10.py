"""
Extracts a 5x5 sub-grid from the top-left corner of the largest connected component of grey (5) pixels in the input grid.
If the grey object is smaller, return the extracted shape based on the object dimension, then fill the rest part with 0 (white).
"""

import numpy as np

def find_object(grid, color):
    # Find all pixels of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return [], 0, 0
    
    # Use a simple bounding box approach to define the object
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    object_coords = []

    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col+1):
            if grid[r,c] == color:
                object_coords.append((r,c))


    return object_coords, min_row, min_col

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the grey (5) object and its top-left corner
    object_coords, min_row, min_col = find_object(input_grid, 5)

    # Initialize the output grid as 5x5 filled with white (0)
    output_grid = np.zeros((5, 5), dtype=int)
    
    #fill based on grey area
    for r in range(5):
        for c in range(5):
            if (min_row+r,min_col+c) in object_coords:
                output_grid[r,c] = 5

    return output_grid.tolist()