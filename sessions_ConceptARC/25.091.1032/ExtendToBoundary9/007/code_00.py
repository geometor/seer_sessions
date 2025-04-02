"""
Transformation Rule:
1. Identify the two distinct non-white connected objects in the input grid using 8-way connectivity. Assume one acts as an 'outer_frame' enclosing the other, the 'inner_object'.
2. Determine which object is the outer frame and which is the inner object based on bounding box containment. If exactly two objects are not found, or if neither encloses the other, return the original grid.
3. Record the color of the 'inner_object' ('inner_color').
4. Determine the minimum and maximum row indices occupied by the 'inner_object' ('inner_min_row', 'inner_max_row').
5. Create a copy of the input grid.
6. Iterate through each row 'r' from 'inner_min_row' to 'inner_max_row'.
7. For each row 'r', find the minimum ('min_col_frame') and maximum ('max_col_frame') column indices where the 'outer_frame' exists in that specific row.
8. Within row 'r', iterate through columns 'c' from 'min_col_frame' to 'max_col_frame'.
9. If the pixel at (r, c) in the *input* grid has the background color (0), change its color in the *output* grid to 'inner_color'.
10. Return the modified output grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects

# Define 8-connectivity structure for scipy.ndimage.label
CONNECTIVITY_STRUCTURE_8 = np.ones((3, 3), dtype=bool)

def find_connected_components(grid, background_color=0, connectivity_structure=CONNECTIVITY_STRUCTURE_8):
    """
    Finds connected components of non-background colors using specified connectivity.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to treat as background.
        connectivity_structure (np.array): The structure defining pixel connectivity.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'label', 'color', 'coords', 'slice', 'size', 'bbox'.
              Returns an empty list if no non-background objects are found.
    """
    objects = []
    mask = grid != background_color
    # Label connected components using the specified connectivity structure
    labeled_array, num_features = label(mask, structure=connectivity_structure) 
    
    if num_features == 0:
        return objects

    slices = find_objects(labeled_array)
    
    for i in range(num_features):
        component_label = i + 1
        # Ensure slices[i] is not None before accessing its attributes
        if slices[i] is None:
            continue # Should not happen if num_features > 0, but good practice

        loc = slices[i]
        coords = np.argwhere(labeled_array == component_label)
        
        if coords.size > 0:
            color = grid[coords[0, 0], coords[0, 1]] 
            size = len(coords)
            # Ensure loc has the expected structure (tuple of slices)
            if isinstance(loc, tuple) and len(loc) == 2 and \
               isinstance(loc[0], slice) and isinstance(loc[1], slice):
                min_row = loc[0].start
                min_col = loc[1].start
                max_row = loc[0].stop - 1 
                max_col = loc[1].stop - 1
                bbox = (min_row, min_col, max_row, max_col)

                objects.append({
                    'label': component_label,
                    'color': color,
                    'coords': coords, # Array of [row, col] pairs
                    'slice': loc,
                    'size': size,
                    'bbox': bbox 
                })
            else:
                # Handle unexpected slice format if necessary
                print(f"Warning: Unexpected slice format for component {component_label}: {loc}")
                # Fallback: calculate bbox from coords
                min_row = np.min(coords[:, 0])
                min_col = np.min(coords[:, 1])
                max_row = np.max(coords[:, 0])
                max_col = np.max(coords[:, 1])
                bbox = (min_row, min_col, max_row, max_col)
                objects.append({
                    'label': component_label,
                    'color': color,
                    'coords': coords,
                    'slice': loc, # Store original slice even if format was odd
                    'size': size,
                    'bbox': bbox
                })

    return objects

def is_bbox_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly contained within outer_bbox."""
    inner_min_r, inner_min_c, inner_max_r, inner_max_c = inner_bbox
    outer_min_r, outer_min_c, outer_max_r, outer_max_c = outer_bbox
    # Use strict inequality to ensure the inner object is truly inside
    return (outer_min_r < inner_min_r and
            outer_min_c < inner_min_c and
            outer_max_r > inner_max_r and
            outer_max_c > inner_max_c)

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    background_color = 0
    
    # --- Step 1: Identify Objects using 8-way connectivity ---
    objects = find_connected_components(input_grid, background_color=background_color, connectivity_structure=CONNECTIVITY_STRUCTURE_8)
    
    # --- Step 2: Verify exactly two objects and determine frame/inner ---
    if len(objects) != 2:
        # If not exactly two objects, pattern doesn't match; return original grid.
        return output_grid 
        
    obj1 = objects[0]
    obj2 = objects[1]
    
    # Check for bounding box containment to identify outer and inner
    if is_bbox_contained(obj2['bbox'], obj1['bbox']):
        outer_frame = obj1
        inner_object = obj2
    elif is_bbox_contained(obj1['bbox'], obj2['bbox']):
        outer_frame = obj2
        inner_object = obj1
    else:
        # No clear containment, pattern doesn't match; return original grid.
        return output_grid

    # --- Step 3: Record inner object's color ---
    inner_color = inner_object['color']

    # --- Step 4: Determine row range of the inner object ---
    inner_min_row, _, inner_max_row, _ = inner_object['bbox']

    # Precompute frame coordinates for efficient lookup per row
    frame_coords_set = set(tuple(coord) for coord in outer_frame['coords'])

    # --- Steps 5-9: Iterate through relevant rows and columns and fill ---
    # Iterate through each row spanned by the inner object
    for r in range(inner_min_row, inner_max_row + 1):
        # Find the horizontal extent (min/max columns) of the outer frame *in this specific row*
        frame_cols_in_row = [c for row, c in outer_frame['coords'] if row == r]
        
        # If the frame doesn't exist in this row (e.g., concave shapes), skip row? 
        # Or should we use the overall bbox col limits? 
        # Based on example 1, seems we need frame boundary in that row.
        if not frame_cols_in_row:
            continue # Skip rows where the outer frame has no presence

        min_col_frame = min(frame_cols_in_row)
        max_col_frame = max(frame_cols_in_row)

        # Iterate through columns within the frame's bounds for this row
        for c in range(min_col_frame, max_col_frame + 1):
            # Check if the pixel in the *input* grid is background
            if input_grid[r, c] == background_color:
                 # Fill the corresponding pixel in the output grid
                 output_grid[r, c] = inner_color

    # --- Step 10: Return the modified grid ---
    return output_grid