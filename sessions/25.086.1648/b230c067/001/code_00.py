"""
This module transforms an input grid containing white (0) and azure (8) pixels
into an output grid of the same dimensions. The transformation involves identifying
distinct azure objects, analyzing their properties (specifically, whether they enclose
a "hole" of white pixels and their top-right position), and recoloring them
either blue (1) or red (2) based on specific rules.

The rules are:
1. Identify all connected components (objects) of azure (8) pixels.
2. For each object, determine its bounding box and if it contains a hole (enclosed white area).
3. Count the number of objects with holes.
4. If exactly one object has a hole:
    - This object with the hole is colored blue (1).
    - Among the objects *without* holes, find the "top-right-most" one (minimum row index of the bounding box top edge, breaking ties with maximum column index of the bounding box right edge). This object is colored red (2).
    - All other objects (without holes, not selected as red) are colored blue (1).
5. If zero objects have holes:
    - Among *all* objects, find the "top-right-most" one (minimum row index, maximum column index tie-breaker). This object is colored red (2).
    - All other objects are colored blue (1).
6. The background white (0) pixels remain unchanged.
"""

import numpy as np
from scipy.ndimage import label, find_objects, binary_erosion, generate_binary_structure

def find_connected_components(grid, color):
    """
    Finds all connected components of a specific color in the grid.
    Uses 8-connectivity (including diagonals).
    """
    binary_grid = (grid == color)
    # Use 8-connectivity
    structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool)
    labeled_grid, num_labels = label(binary_grid, structure=structure)
    
    objects = []
    if num_labels > 0:
        # find_objects returns slices, convert them to coordinates
        object_slices = find_objects(labeled_grid)
        for i in range(num_labels):
            label_id = i + 1
            coords = tuple(zip(*np.where(labeled_grid == label_id)))
            # coords is a list of (row, col) tuples
            objects.append(set(coords)) 
            
    return objects

def get_bounding_box(obj_pixels):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of pixels."""
    if not obj_pixels:
        return None
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    return min(rows), min(cols), max(rows), max(cols)

def has_hole(obj_pixels, grid_shape):
    """
    Checks if an object, defined by its pixels, encloses a hole of background (0).
    
    Args:
        obj_pixels (set): Set of (row, col) tuples for the object.
        grid_shape (tuple): (height, width) of the original grid.

    Returns:
        bool: True if the object has a hole, False otherwise.
    """
    if not obj_pixels:
        return False

    min_r, min_c, max_r, max_c = get_bounding_box(obj_pixels)
    
    # Create a small grid representing the bounding box area plus a 1-pixel border
    # The border helps handle objects touching the grid edges correctly.
    padded_min_r = max(0, min_r - 1)
    padded_min_c = max(0, min_c - 1)
    padded_max_r = min(grid_shape[0] - 1, max_r + 1)
    padded_max_c = min(grid_shape[1] - 1, max_c + 1)

    # Create a boolean grid: True for background, False for object pixels within padded bbox
    subgrid_shape = (padded_max_r - padded_min_r + 1, padded_max_c - padded_min_c + 1)
    background_mask = np.ones(subgrid_shape, dtype=bool)

    for r_obj, c_obj in obj_pixels:
        # Map object coordinates to the padded subgrid coordinates
        sr, sc = r_obj - padded_min_r, c_obj - padded_min_c
        if 0 <= sr < subgrid_shape[0] and 0 <= sc < subgrid_shape[1]:
            background_mask[sr, sc] = False # Mark object pixels as False (not background)

    # Label connected components of the background within the padded bounding box
    structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool) # 8-connectivity
    labeled_background, num_labels = label(background_mask, structure=structure)

    if num_labels <= 1:
        # If there's 0 or 1 background component, no enclosed hole is possible
        return False

    # Identify the background component connected to the outer border
    # Any pixel on the border of background_mask corresponds to the outer region
    border_indices = set()
    if subgrid_shape[0] > 0:
        border_indices.update((0, c) for c in range(subgrid_shape[1]))
        border_indices.update((subgrid_shape[0] - 1, c) for c in range(subgrid_shape[1]))
    if subgrid_shape[1] > 0:
        border_indices.update((r, 0) for r in range(subgrid_shape[0]))
        border_indices.update((r, subgrid_shape[1] - 1) for r in range(subgrid_shape[0]))

    outer_label = None
    for r_border, c_border in border_indices:
         # Check bounds just in case shape is 1xN or Nx1
        if 0 <= r_border < subgrid_shape[0] and 0 <= c_border < subgrid_shape[1]:
            label_val = labeled_background[r_border, c_border]
            if label_val > 0: # If it's part of a labeled background component
                outer_label = label_val
                break # Found the label connected to the outside

    # If there is any background label (num_labels > 1) that is NOT the outer_label,
    # it represents an enclosed hole.
    for i in range(1, num_labels + 1):
        if i != outer_label:
            # Check if this component actually exists (sometimes label skips numbers)
            if np.any(labeled_background == i):
                 # We found an internal background component, thus a hole exists.
                 # We must ensure this internal component wasn't caused purely by padding
                 # Check if any pixel of this component maps back to the original grid's non-padded bbox
                 component_pixels = np.argwhere(labeled_background == i)
                 for r_comp, c_comp in component_pixels:
                     orig_r, orig_c = r_comp + padded_min_r, c_comp + padded_min_c
                     if min_r <= orig_r <= max_r and min_c <= orig_c <= max_c:
                         # This hole component exists within the original object's bbox
                         return True

    return False


def transform(input_grid):
    """
    Transforms the input grid based on identifying azure objects, checking for holes,
    and applying coloring rules based on hole count and object position.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.zeros_like(input_grid) # Initialize with background color 0
    grid_shape = input_grid.shape

    # 1. Identify all separate connected objects composed of azure (8) pixels
    azure_objects_pixels = find_connected_components(input_grid, 8)

    if not azure_objects_pixels:
        return output_grid.tolist() # Return background if no objects found

    # 2. Analyze objects: calculate properties
    objects_data = []
    for obj_pixels in azure_objects_pixels:
        min_r, min_c, max_r, max_c = get_bounding_box(obj_pixels)
        hole = has_hole(obj_pixels, grid_shape)
        objects_data.append({
            "pixels": obj_pixels,
            "min_row": min_r,
            "max_col": max_c,
            "has_hole": hole
        })

    # 3. Count objects with holes
    hole_objects = [obj for obj in objects_data if obj["has_hole"]]
    non_hole_objects = [obj for obj in objects_data if not obj["has_hole"]]
    hole_count = len(hole_objects)

    red_object = None
    blue_objects = []

    # 4-7. Apply coloring logic based on hole count
    if hole_count == 1:
        # Hole object is blue
        blue_objects.append(hole_objects[0])
        
        # Find top-right-most among non-hole objects to be red
        if non_hole_objects:
            min_row_non_hole = min(obj["min_row"] for obj in non_hole_objects)
            top_non_hole = [obj for obj in non_hole_objects if obj["min_row"] == min_row_non_hole]
            
            max_col_top_non_hole = max(obj["max_col"] for obj in top_non_hole)
            red_object = next(obj for obj in top_non_hole if obj["max_col"] == max_col_top_non_hole)

            # Add remaining non-hole objects to blue list
            blue_objects.extend([obj for obj in non_hole_objects if obj != red_object])
        # Else (no non-hole objects), red_object remains None, and only the hole_object is blue.

    elif hole_count == 0:
        # Find top-right-most among all objects to be red
        if objects_data: # Check if there are any objects at all
            min_row_all = min(obj["min_row"] for obj in objects_data)
            top_all = [obj for obj in objects_data if obj["min_row"] == min_row_all]
            
            max_col_top_all = max(obj["max_col"] for obj in top_all)
            red_object = next(obj for obj in top_all if obj["max_col"] == max_col_top_all)

            # Add all other objects to blue list
            blue_objects.extend([obj for obj in objects_data if obj != red_object])
            
    # Handle potential cases not explicitly covered by examples (e.g., hole_count > 1)
    # Based on the examples, we assume hole_count is 0 or 1. 
    # If it could be > 1, the logic might need adjustment. For now, assume 0 or 1.
    # If hole_count > 1, the current logic results in red_object = None and blue_objects = []
    # which means nothing gets colored. Let's refine this default - maybe color all blue?
    # Let's stick to the logic derived strictly from examples for now. If hole_count > 1, nothing is coloured.
    
    # 8. Color the red object
    if red_object:
        for r, c in red_object["pixels"]:
            output_grid[r, c] = 2 # Red

    # 9. Color the blue objects
    for blue_obj in blue_objects:
        for r, c in blue_obj["pixels"]:
             # Avoid overwriting red if somehow an object ended up in both lists (shouldn't happen with current logic)
            if output_grid[r, c] == 0:
                output_grid[r, c] = 1 # Blue

    # 10. Return the completed output grid
    return output_grid.tolist()