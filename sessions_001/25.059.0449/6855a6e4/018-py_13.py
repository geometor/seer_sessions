"""
The transformation identifies red (2) "C" shapes, and repositions gray (5) pixels to fill the horizontal openings of these shapes.
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def get_object_bounds(coords):
    """Gets the bounding box (min/max x and y) of a set of coordinates."""
    if len(coords) == 0:
        return None, None, None, None
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_x, max_x, min_y, max_y

def find_contiguous_objects(grid, color):
    """
    Finds all contiguous objects of a specific color and returns their coordinates.
    Uses scipy.ndimage.label for connected component labeling.
    """
    colored_pixels = (grid == color).astype(int)
    labeled_array, num_features = label(colored_pixels)
    objects = []
    for i in range(1, num_features + 1):  # Iterate through each labeled object
        coords = np.argwhere(labeled_array == i)
        objects.append(coords)
    return objects

def find_c_shape_opening(grid, red_object_coords):
    """
    Finds the x-coordinate of the opening of a C-shaped red object.
    """
    min_x, max_x, min_y, max_y = get_object_bounds(red_object_coords)
    
    # Check for opening on the left
    if min_x > 0:
        left_column = grid[min_y:max_y+1, min_x-1]
        if not (left_column == 2).any():  # No red pixels in the column to the left
                return min_x

    # Check for opening on the right
    if max_x < grid.shape[1] - 1:
        right_column = grid[min_y:max_y + 1, max_x + 1]
        if not (right_column==2).any():
            return max_x
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    
    # Find red and gray objects
    red_coords = find_objects(input_grid, 2)
    gray_coords = find_objects(input_grid, 5)
    
    if len(red_coords) == 0 or len(gray_coords) == 0:
        return output_grid

    # Find contiguous red objects
    red_objects = find_contiguous_objects(input_grid, 2)

    # Count openings
    openings_count = 0
    openings = []
    for red_object in red_objects:
        opening_x = find_c_shape_opening(input_grid, red_object)
        if opening_x is not None:
            openings_count += 1
            openings.append((red_object, opening_x)) #store coordinates and X

    # Check if the number of openings matches the number of gray pixels
    if openings_count != len(gray_coords):
        return output_grid

    #clear grey pixels
    for y,x in gray_coords:
        output_grid[y,x] = 0

    # Reposition gray pixels into the openings
    grey_idx = 0
    for red_object, opening_x in openings:

        min_x, max_x, min_y, max_y = get_object_bounds(red_object)
        vertical_center = (min_y + max_y) // 2

        #fill the coordinates
        output_grid[vertical_center, opening_x] = 5
        grey_idx+=1

    return output_grid