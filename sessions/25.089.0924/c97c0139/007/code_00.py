import numpy as np
from scipy.ndimage import label
import math

"""
Transformation Rule:

1. Identify all distinct connected objects (8-way connectivity) composed of red 
   pixels (color 2).
2. For each red object, calculate its size 'L' (number of pixels) and determine 
   a maximum Manhattan distance threshold 'k' using the formula: 
   k = floor((L - 1) / 2). Store the pixels and 'k' for each object.
3. Create a copy of the input grid.
4. Iterate through every pixel (r, c) in the grid.
5. If the pixel at (r, c) in the original input grid is white (color 0):
    a. Find the minimum Manhattan distance ('d_min') from this white pixel (r, c) 
       to *any* red pixel across *all* identified red objects.
    b. Determine which specific red object ('closest_object') contains the red 
       pixel that yielded this minimum distance 'd_min'.
    c. Retrieve the threshold 'k_closest' calculated for this 'closest_object'.
    d. If the condition '0 < d_min <= k_closest' holds true:
        i. Change the color of the pixel at (r, c) in the output grid to 
           azure (color 8).
6. Return the modified output grid. Original red pixels remain unchanged.
"""

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (row, col tuples)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_objects(grid, color):
    """
    Finds connected components of a specific color using 8-way connectivity.

    Args:
        grid: The 2D numpy array grid.
        color: The target color integer.

    Returns:
        A dictionary where keys are object IDs (starting from 1) and values
        are lists of (row, col) tuples representing the pixels of that object.
        Returns an empty dictionary if no objects of the specified color are found.
    """
    # Structure for 8-way connectivity
    structure = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) 
    # Create a boolean mask where the target color is present
    mask = (grid == color)
    # Label the connected components in the mask
    labeled_array, num_features = label(mask, structure=structure)
    
    objects = {}
    if num_features > 0:
        # Iterate through each found feature (object) ID (1 to num_features)
        for i in range(1, num_features + 1):
            # Find the coordinates (indices) where the labeled array equals the current feature ID
            pixels = np.argwhere(labeled_array == i)
            # Convert the numpy array of [row, col] pairs to a list of (row, col) tuples
            pixel_tuples = [tuple(p) for p in pixels]
            # Store the list of pixel tuples in the dictionary with the object ID as the key
            if pixel_tuples: # Ensure the object is not empty
                 objects[i] = pixel_tuples
    return objects


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: colors white pixels azure if they are within
    a specific Manhattan distance 'k' (derived from the size of the *closest* red object)
    from that closest red object.
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
        # Calculate the object-specific distance threshold k
        k = math.floor((L - 1) / 2)
        # Store the pixels and the calculated k for this object
        object_properties[obj_id] = {'pixels': pixels, 'k': k}

    # --- Step 4-6: Iterate through grid and color qualifying white pixels ---
    for r in range(height):
        for c in range(width):
            # Check if the pixel in the original input is white (Step 5)
            if input_grid[r, c] == white_color:
                current_pos = (r, c)
                min_overall_distance = float('inf')
                closest_object_id = None

                # Step 6a, 6b: Find the minimum distance and the ID of the closest object
                for obj_id, properties in object_properties.items():
                    obj_pixels = properties['pixels']
                    
                    # Calculate min distance from current_pos to this object
                    min_dist_to_this_obj = float('inf')
                    for obj_pixel_coords in obj_pixels:
                        dist = manhattan_distance(current_pos, obj_pixel_coords)
                        min_dist_to_this_obj = min(min_dist_to_this_obj, dist)
                        # Optimization: if distance is 1, it's the minimum possible positive distance 
                        # for this specific object, no need to check other pixels *within this object*.
                        if min_dist_to_this_obj == 1:
                           break 
                    
                    # Check if this object is closer than the current closest object found so far
                    if min_dist_to_this_obj < min_overall_distance:
                        min_overall_distance = min_dist_to_this_obj
                        closest_object_id = obj_id
                        # Optimization: if the overall minimum distance becomes 1, 
                        # we've found the absolute closest pixel possible, but we still
                        # need its associated object ID, so we can't break the outer loop yet.

                # Step 6c, 6d: Check the condition using the closest object's k
                if closest_object_id is not None: # Ensure a closest object was found
                    k_closest = object_properties[closest_object_id]['k']
                    
                    # Apply the coloring rule based on the closest object's threshold
                    if 0 < min_overall_distance <= k_closest:
                        output_grid[r, c] = azure_color

    # --- Step 7: Return the modified grid ---
    return output_grid