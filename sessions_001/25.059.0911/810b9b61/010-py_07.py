"""
1.  **Identify Blue Shapes:** Locate all contiguous groups of blue (1) pixels in the input grid. These constitute the "blue shapes."

2.  **Segment Top:** For each blue shape found on the top part, identify the top segment to be replaced.

3.  **Change to Green:** Change to green (3) all the top blue segment.

4  **Preserve the rest:** leave blue all bottom segments that weren't selected.

5.  **Background:** All other pixels remain white (0).
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid, color):
    mask = (grid == color)
    labeled_array, num_features = label(mask)
    objects = []
    for i in range(1, num_features + 1):
        obj_pixels = np.where(labeled_array == i)
        objects.append(list(zip(obj_pixels[0], obj_pixels[1])))
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find blue objects
    blue_objects = find_objects(input_grid, 1)
    
    # Iterate through each blue object
    for obj in blue_objects:
        # Find the top-most row of the object
        min_row = min(pixel[0] for pixel in obj)
        
        # Identify pixels in the top segment
        top_segment = [pixel for pixel in obj if pixel[0] == min_row]

        # Change top segment to green
        for pixel in top_segment:
            output_grid[pixel] = 3

    return output_grid