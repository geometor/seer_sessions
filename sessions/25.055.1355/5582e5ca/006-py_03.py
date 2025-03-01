"""
The transformation rule identifies the color of the largest contiguous object (a group of connected pixels of the same color) within the input grid. The output grid is created with the same dimensions as the input grid, and all its pixels are set to the color of the largest object found in the input.
"""

import numpy as np
from scipy.ndimage import label

def find_largest_object(grid):
    """
    Finds the color of the largest contiguous object in a grid.
    """
    labeled_grid, num_features = label(grid)
    if num_features == 0:
        return 0  # Handle empty grid case

    largest_object_size = 0
    largest_object_color = 0

    for i in range(1, num_features + 1):
        object_pixels = (labeled_grid == i)
        object_color = grid[object_pixels][0]  # Get color of the object
        
        #consider only non-white objects
        if object_color != 0:
            object_size = np.sum(object_pixels)
            if object_size > largest_object_size:
                largest_object_size = object_size
                largest_object_color = object_color

    return largest_object_color

def transform(input_grid):
    # initialize output_grid with same dimensions and type
    output_grid = np.zeros_like(input_grid)

    # find largest object
    target_color = find_largest_object(input_grid)

    # change output pixels 
    output_grid[:] = target_color

    return output_grid