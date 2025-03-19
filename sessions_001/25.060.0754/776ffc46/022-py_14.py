"""
Identifies blue (1) shapes in the input grid. If a blue shape partially covers a white region and is adjacent to the largest green region, covering a portion of it, the color of that blue shape changes to green (3).
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    color_mask = (grid == color)
    labeled_array, num_features = label(color_mask)
    objects = []
    for i in range(1, num_features + 1):
        obj_coords = np.where(labeled_array == i)
        objects.append(list(zip(obj_coords[0], obj_coords[1])))
    return objects

def is_adjacent(obj1_coords, obj2_coords):
    """Checks if two objects are adjacent (including diagonals)."""
    for r1, c1 in obj1_coords:
        for r2, c2 in obj2_coords:
            if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                return True
    return False
    
def is_overlapping_and_covering(obj1_coords, obj2_coords):
    """
    checks that the target obj (obj1) is not entirely contained in the green (obj2) region
    """
    
    obj1_set = set(obj1_coords)
    obj2_set = set(obj2_coords)
        
    if obj1_set.intersection(obj2_set) and not obj1_set.issubset(obj2_set):
        return True
    
    return False

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    
    # Find blue objects
    blue_objects = find_objects(input_grid, 1)
    
    # Find green objects
    green_objects = find_objects(input_grid, 3)
    
    # find largest green objects
    max_len = 0
    largest_green_coords = []

    for obj in green_objects:
        if len(obj) > max_len:
            max_len = len(obj)
            largest_green_coords = obj

    # Iterate through blue objects and apply the transformation rule
    for blue_obj_coords in blue_objects:
        if is_adjacent(blue_obj_coords, largest_green_coords):
          if is_overlapping_and_covering(blue_obj_coords,largest_green_coords):
                # Change the color of the blue object to green
                for r, c in blue_obj_coords:
                    output_grid[r, c] = 3

    return output_grid