"""
1.  Identify Objects: Divide the input grid into distinct objects. An object is a contiguous region of pixels of the same color.
2.  Find Dominant Object Color: Identify the color that constitutes the largest object(s) by area. We consider not only the number of pixels with same color but also the fact they should create a large area of this color (contiguous pixels). In case of several largest areas of different colors, choose any.
3.  Output: Create a 1x1 output grid. The single pixel's color in the output grid should be the color of the largest object found in the input grid, as defined in step 2.
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid):
    """
    Identifies distinct objects in the grid using connected component labeling.
    """
    labeled_grid, num_objects = label(grid)
    return labeled_grid, num_objects

def get_object_sizes(labeled_grid, num_objects):
    """
    Calculates the size of each object.
    """
    object_sizes = {}
    for i in range(1, num_objects + 1):  # Object labels start from 1
        object_sizes[i] = np.sum(labeled_grid == i)
    return object_sizes

def get_object_colors(grid, labeled_grid, num_objects):
     """
     Determine color of each object
     """
     object_colors = {}
     for i in range(1, num_objects+1):
          object_colors[i] = grid[labeled_grid == i][0] #get color from any pixel of the object
     return object_colors
     

def transform(input_grid):
    """
    Transforms the input grid based on the largest object's color.
    """
    # Identify Objects
    labeled_grid, num_objects = find_objects(input_grid)

    # Calculate object sizes
    object_sizes = get_object_sizes(labeled_grid, num_objects)
    
    # Get object colors
    object_colors = get_object_colors(input_grid, labeled_grid, num_objects)

    # Find the largest object
    largest_object_id = max(object_sizes, key=object_sizes.get)
    
    # Find color of largest object
    dominant_color = object_colors[largest_object_id]

    # Create 1x1 output grid with the dominant color
    output_grid = np.array([[dominant_color]])

    return output_grid