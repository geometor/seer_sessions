"""
1. Identify the Target Object: In the input grid, locate the horizontal line composed of yellow (4) pixels.
2. Isolate Target Object: Disregard all other objects/colors in the input. Focus solely on the identified yellow line.
3. Bounding Box: find the minimum size of the isolated object, specifically looking for horizontal lines.
4. Create output using the dimensions of the bounding box and fill with the target object's color.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def is_horizontal_line(coords):
    # Check if a set of coordinates forms a horizontal line.
    if len(coords) == 0:
        return False
    rows = coords[:, 0]
    return np.all(rows == rows[0])

def bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the yellow object (color 4).
    yellow_coords = find_object(input_grid, 4)

    # if no yellow object is found
    if len(yellow_coords) == 0:
        return [[]]
    
    # Check if the yellow object forms a horizontal line.
    if not is_horizontal_line(yellow_coords):
        return [[]] # or perhaps raise an exception, depending on desired behavior

    # Calculate the bounding box of the yellow object.
    min_row, max_row, min_col, max_col = bounding_box(yellow_coords)

    # compute height and width
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # Create an output grid filled with yellow (4).
    output_grid = np.full((height, width), 4)

    return output_grid.tolist()