import numpy as np
from scipy.ndimage import label, find_objects

"""
Identifies all distinct contiguous objects composed of green pixels (color 3).
For each green object, determines if its bounding box completely contains the bounding box of any other distinct green object.
Recolors the objects based on containment relationships:
- If a green object's bounding box contains another green object's bounding box, the containing object is recolored blue (color 1).
- If a green object's bounding box is contained within another green object's bounding box, the contained object is recolored magenta (color 6).
- If a green object neither contains nor is contained by any other green object, it is recolored red (color 2).
All other pixels remain their original color (typically white, color 0).
"""

def find_green_objects(grid):
    """
    Finds all connected components (objects) of green pixels (3) in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing:
            - labeled_array (np.ndarray): An array where each green object has a unique integer label.
            - object_slices (list): A list of slice objects representing the bounding box of each found object.
            - object_coords (dict): A dictionary mapping object labels (int > 0) to lists of (row, col) coordinates.
    """
    green_mask = (grid == 3)
    labeled_array, num_features = label(green_mask)
    object_slices = find_objects(labeled_array)
    
    object_coords = {}
    if num_features > 0:
        for label_id in range(1, num_features + 1):
            coords = np.argwhere(labeled_array == label_id)
            object_coords[label_id] = [tuple(coord) for coord in coords]
            
    return labeled_array, object_slices, object_coords

def get_bounding_box(obj_slice):
    """ Extracts min/max row/col from object slices. """
    min_row, max_row = obj_slice[0].start, obj_slice[0].stop
    min_col, max_col = obj_slice[1].start, obj_slice[1].stop
    return min_row, min_col, max_row, max_col # Note: max_row/max_col are exclusive bounds from slices

def is_contained(bbox1, bbox2):
    """ Checks if bbox2 is strictly contained within bbox1. """
    min_r1, min_c1, max_r1, max_c1 = bbox1
    min_r2, min_c2, max_r2, max_c2 = bbox2
    return min_r1 <= min_r2 and min_c1 <= min_c2 and max_r1 >= max_r2 and max_c1 >= max_c2

def transform(input_grid):
    """
    Transforms the input grid by recoloring green objects based on bounding box containment.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np) # Start with a copy

    # Find all green objects and their properties
    labeled_array, object_slices, object_coords = find_green_objects(input_np)
    num_objects = len(object_slices)

    if num_objects == 0:
        return output_grid.tolist() # No green objects, return original

    # Calculate bounding boxes for all objects
    bboxes = {}
    for i, obj_slice in enumerate(object_slices):
         if obj_slice is not None: # find_objects can return None for missing labels
            label_id = i + 1 # Labels are 1-based
            bboxes[label_id] = get_bounding_box(obj_slice)

    # Determine containment relationships
    contains_other = {label_id: False for label_id in bboxes}
    is_contained_by_other = {label_id: False for label_id in bboxes}

    object_ids = list(bboxes.keys())
    for i in range(len(object_ids)):
        for j in range(len(object_ids)):
            if i == j:
                continue # Don't compare an object to itself

            label_id1 = object_ids[i]
            label_id2 = object_ids[j]
            bbox1 = bboxes[label_id1]
            bbox2 = bboxes[label_id2]

            if is_contained(bbox1, bbox2):
                contains_other[label_id1] = True
                is_contained_by_other[label_id2] = True

    # Recolor objects based on containment
    for label_id, coords in object_coords.items():
        new_color = 0 # Default or placeholder
        if contains_other[label_id]:
            new_color = 1 # Blue for container
        elif is_contained_by_other[label_id]:
            new_color = 6 # Magenta for contained
        else:
            new_color = 2 # Red for standalone

        # Apply the new color to the output grid
        for r, c in coords:
            output_grid[r, c] = new_color

    return output_grid.tolist()