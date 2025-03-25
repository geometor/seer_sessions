"""
Identifies contiguous blocks of non-zero colored pixels in a 1x33 grid and sets to white (value 0) the pixels at the
beginning and end of the colored block, preserving the longest sequence of colored pixels.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous blocks of the same color (objects) in a 1D grid."""
    objects = []
    current_object = []
    for i, pixel in enumerate(grid):
        if pixel != 0:  # Consider only non-zero pixels as part of objects
            current_object.append((i, pixel))
        elif current_object:
            objects.append(current_object)
            current_object = []
    if current_object:  # Append the last object if it exists
        objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid with the same values as the input grid
    output_grid = np.copy(input_grid)
    
    # find the objects
    objects = find_objects(input_grid)

    for obj in objects:
        # change the pixels color from start to the pixel before the max_length starts
        if len(obj)>0:
            # find the max_len contiguous pixels
            max_len = 0
            start = 0
            current_len = 0
            current_start = 0
        
            for i in range(len(obj)):
                current_len +=1
                if current_len > max_len:
                    max_len = current_len
                    start = current_start
        
            # convert to white pixels outside the main object
            for i in range(len(obj)):
                if not(i>=start and i < start+max_len):
                    pos = obj[i][0]
                    output_grid[pos]=0
    return output_grid