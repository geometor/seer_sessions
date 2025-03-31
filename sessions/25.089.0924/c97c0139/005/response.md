```python
"""
Transformation Rule:

1. Identify all distinct connected objects composed of red pixels (color 2), considering 8-way connectivity (including diagonals).
2. For each identified red object:
    a. Calculate its size 'L' (number of pixels).
    b. Determine a maximum Manhattan distance threshold 'k' using the formula: k = floor((L - 1) / 2). Store this threshold associated with the object.
3. Create a copy of the input grid.
4. Iterate through every pixel (r, c) in the grid.
5. If the pixel at (r, c) in the *original* input grid is white (color 0):
    a. Check if this pixel should be colored azure: Iterate through each red object found earlier.
    b. For the current red object, calculate the minimum Manhattan distance ('d_min') from the white pixel (r, c) to *any* pixel within that red object.
    c. Retrieve the threshold 'k' calculated for this specific red object.
    d. If the condition '0 < d_min <= k' is met:
        i. The white pixel (r, c) qualifies to be colored azure.
        ii. Change the color of the pixel at (r, c) in the *output grid* to azure (color 8).
        iii. Stop checking other red objects for this white pixel (r, c) and move to the next pixel in the grid.
6. Return the modified output grid.
"""

import numpy as np
from scipy.ndimage import label
import math

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (tuples or lists)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_objects(grid, color):
    """Finds connected components of a specific color."""
    structure = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) # 8-connectivity
    labeled_array, num_features = label(grid == color, structure=structure)
    objects = {}
    if num_features > 0:
        for i in range(1, num_features + 1):
            pixels = list(map(tuple, np.argwhere(labeled_array == i)))
            if pixels: # Ensure object is not empty
                 objects[i] = pixels
    return objects


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: colors white pixels azure if they are within
    a specific Manhattan distance 'k' (derived from the size of a red object)
    from that red object.
    """
    # Define colors
    white_color = 0
    red_color = 2
    azure_color = 8
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # --- Step 1 & 2: Find red objects and calculate their properties ---
    red_objects_pixels = find_objects(input_grid, red_color)
    
    # If no red objects, return the original grid copy
    if not red_objects_pixels:
        return output_grid

    # Store object properties (pixels and threshold k)
    object_properties = {}
    for obj_id, pixels in red_objects_pixels.items():
        L = len(pixels)
        k = math.floor((L - 1) / 2)
        object_properties[obj_id] = {'pixels': pixels, 'k': k}

    # --- Step 3-7: Iterate through grid and color qualifying white pixels ---
    for r in range(height):
        for c in range(width):
            # Check if the pixel in the original input is white
            if input_grid[r, c] == white_color:
                current_pos = (r, c)
                should_color_azure = False # Flag for this white pixel

                # Check against each red object
                for obj_id, properties in object_properties.items():
                    obj_pixels = properties['pixels']
                    obj_k = properties['k']

                    # Optimization: if k < 1 for this object, it cannot color any pixels
                    if obj_k < 1:
                        continue

                    # Calculate min distance from current_pos to this object
                    min_dist_to_obj = float('inf')
                    for obj_pixel_coords in obj_pixels:
                        dist = manhattan_distance(current_pos, obj_pixel_coords)
                        min_dist_to_obj = min(min_dist_to_obj, dist)
                        # Small optimization: if dist becomes 1, we know it's the minimum possible > 0
                        if min_dist_to_obj == 1: 
                           break # No need to check other pixels in this *same* object

                    # Check if the distance condition is met for this object
                    if 0 < min_dist_to_obj <= obj_k:
                        should_color_azure = True
                        break # Found a qualifying object, no need to check others for this white pixel

                # If any object qualified this pixel, color it in the output
                if should_color_azure:
                    output_grid[r, c] = azure_color

    # Return the modified grid
    return output_grid
```