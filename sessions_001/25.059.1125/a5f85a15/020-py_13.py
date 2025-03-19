"""
1.  Identify Green Objects: Locate all contiguous regions (objects) of green (3) pixels.
2.  Topmost Green: For each green object, change the *topmost* green pixel to yellow (4). If there are multiple green pixels at the same highest y-coordinate within an object, change the leftmost of those to yellow.
3. Preserve other pixels. All other pixels retain their color.
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid, color):
    """
    Finds connected regions (objects) of the specified color in the grid.
    Returns a list of lists of (row, col) coordinates for each object.
    """
    mask = (grid == color).astype(int)
    labeled_array, num_features = label(mask)
    objects = []
    for i in range(1, num_features + 1):
        coords = np.where(labeled_array == i)
        objects.append(list(zip(coords[0], coords[1])))
    return objects

def find_topmost_pixel(object_coords):
    """
    Finds the topmost (and leftmost if tied) pixel coordinate in a list of coordinates.
    """
    min_row = float('inf')
    topmost_pixel = None
    for row, col in object_coords:
        if row < min_row:
            min_row = row
            topmost_pixel = (row, col)
        elif row == min_row:
            topmost_pixel = (row, min(col, topmost_pixel[1]))  # Leftmost if tied
    return topmost_pixel

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find green objects
    green_objects = find_objects(input_grid, 3)

    # change topmost green pixel in each object to yellow
    for obj in green_objects:
        topmost = find_topmost_pixel(obj)
        if topmost:  # Check if topmost is not None
          output_grid[topmost] = 4

    return output_grid