"""
1. Identify the single contiguous object in the input grid.  A contiguous object is a group of pixels of the same color that are connected horizontally, vertically, or diagonally.
2. Extract this object exactly as it appears in the input.
3. The output grid should contain *only* the extracted object, with the same shape and color. There is no concept of background/canvas.
"""

import numpy as np

def find_single_object(grid):
    # Find coordinates of all non-zero pixels.
    coords = np.argwhere(grid != 0)
    if len(coords) == 0:
        return []

    # Get the color of the first non-zero pixel.
    first_color = grid[coords[0][0], coords[0][1]]

    # Find all pixels of the same color that form a single object.
    object_coords = np.argwhere(grid == first_color)

    return object_coords

def extract_object(grid, coords):
    # Calculate the bounding box of the object.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    # Calculate height and width of the object.
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    # create output grid of necessary size
    output_grid = np.zeros((height, width), dtype=int)

    # fill in the object
    for row, col in coords:
      output_grid[row-min_row, col-min_col] = grid[row, col]

    return output_grid

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the coordinates of the single object.
    object_coords = find_single_object(input_grid)

    # if no object is found
    if len(object_coords) == 0:
        return [[]]

    # Extract the object into a new grid.
    output_grid = extract_object(input_grid, object_coords)

    return output_grid.tolist()