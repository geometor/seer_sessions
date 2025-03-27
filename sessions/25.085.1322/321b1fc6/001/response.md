```python
"""
The transformation identifies specific objects in the input grid based on color and uses them to define a pattern and target locations.

1.  **Initialization**: Create an output grid of the same dimensions as the input, filled with the background color (white, 0).
2.  **Object Identification**:
    *   Identify all connected components (objects) of Azure color (8). These are the 'markers'.
    *   Identify all connected components (objects) of any color other than white (0) or azure (8). These are the 'source objects'.
3.  **Pattern Template Determination**:
    *   If no source objects exist, return the empty output grid.
    *   Examine the source objects. Check if they are all identical in shape and color pattern relative to their top-left bounding box corners.
    *   If all source objects are identical (or if there's only one), select the one whose top-left corner has the minimum row index, and then the minimum column index. Extract the pattern (colors within its bounding box relative to the top-left) as the 'pattern template'.
    *   If the source objects are not identical, determine the minimal bounding box that encloses *all* pixels of *all* source objects combined. Extract the rectangular subgrid from the *input grid* corresponding to this combined bounding box. This subgrid (including any background pixels within it) becomes the 'pattern template'.
4.  **Stamping**:
    *   For each identified marker object:
        *   Find the coordinate (row, column) of its top-left pixel (minimum row, then minimum column).
        *   Overlay the 'pattern template' onto the output grid, aligning the top-left corner of the template with the marker's top-left coordinate. Pixels from the template overwrite existing pixels in the output grid. Handle boundary conditions (if the pattern extends beyond the grid limits, clip it).
5.  **Return**: Return the modified output grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects, center_of_mass
from collections import defaultdict

def find_connected_components(grid, target_colors):
    """
    Finds all connected components for a specific set of colors in the grid.

    Args:
        grid (np.array): The input grid.
        target_colors (set): A set of integer colors to find objects for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples),
              'bbox' (slice tuple from find_objects), 'top_left' (r, c),
              'relative_pattern' (np.array). Returns empty list if no objects found.
    """
    objects = []
    mask = np.isin(grid, list(target_colors))
    if not np.any(mask):
        return objects

    labeled_array, num_features = label(mask)

    found_locs = find_objects(labeled_array)

    for i in range(num_features):
        obj_slice = found_locs[i]
        obj_coords_local = np.argwhere(labeled_array[obj_slice] == (i + 1))
        obj_coords_global = obj_coords_local + np.array([obj_slice[0].start, obj_slice[1].start])

        # Determine the single color of the object
        # Check the first pixel's color; connectivity ensures they are the same
        # if finding components for *one* color at a time.
        # If finding components across *multiple* allowed colors (like source objects),
        # need to handle multi-color components differently or ensure connectivity is by *single* color.
        # Re-thinking: The problem implies source objects can be multi-colored patterns themselves (train_2).
        # But connectivity is usually defined by *same* color.
        # Let's assume connectivity means same-color neighbours.
        # If a source "pattern" is multi-colored, it's actually multiple single-color objects.
        # The natural language suggests grouping based on non-0, non-8.

        # Let's find objects color by color first, then group non-0/non-8 later if needed.
        # Or find all non-0 connected areas first, then filter.

        # Simpler approach: Find objects for *each* target color separately.

        obj_pixels = []
        min_r, min_c = float('inf'), float('inf')
        max_r, max_c = float('-inf'), float('-inf')
        first_pixel_coord = tuple(obj_coords_global[0])
        obj_color = grid[first_pixel_coord]

        # Verify all pixels in this component have the same color if assumption holds
        is_single_color = True
        for r, c in obj_coords_global:
            if grid[r, c] != obj_color:
                is_single_color = False # This shouldn't happen with standard 'label' usage per color mask
                break
            obj_pixels.append((r, c))
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

        if not is_single_color:
            # Handle error or refine object finding if components can span multiple target colors
            # For now, assume connectivity implies single color from target_colors
            print(f"Warning: Component {i+1} seems multi-colored. Unexpected.")
            continue

        # Create relative pattern based on bounding box
        bbox_slice = (slice(min_r, max_r + 1), slice(min_c, max_c + 1))
        relative_pattern = grid[bbox_slice].copy()
        # Mask out pixels not belonging to this specific object within its bbox
        mask_in_bbox = np.zeros_like(relative_pattern, dtype=bool)
        for r, c in obj_pixels:
            mask_in_bbox[r - min_r, c - min_c] = True
        relative_pattern[~mask_in_bbox] = 0 # Set non-object pixels within bbox to background


        objects.append({
            'color': obj_color,
            'pixels': obj_pixels,
            'bbox': bbox_slice, # Use calculated bbox
            'top_left': (min_r, min_c),
            'relative_pattern': relative_pattern
        })

    return objects

def find_all_objects(grid):
    """ Finds all non-background objects, separated by color. """
    all_objs = []
    colors_present = np.unique(grid)
    for color in colors_present:
        if color == 0:
            continue
        # Create mask for the current color
        mask = (grid == color)
        labeled_array, num_features = label(mask)
        found_locs = find_objects(labeled_array)

        for i in range(num_features):
            obj_slice = found_locs[i]
            obj_coords_local = np.argwhere(labeled_array[obj_slice] == (i + 1))
            obj_coords_global = obj_coords_local + np.array([obj_slice[0].start, obj_slice[1].start])

            obj_pixels = []
            min_r, min_c = float('inf'), float('inf')
            max_r, max_c = float('-inf'), float('-inf')
            for r, c in obj_coords_global:
                obj_pixels.append((r, c))
                min_r = min(min_r, r)
                min_c = min(min_c, c)
                max_r = max(max_r, r)
                max_c = max(max_c, c)

            bbox_slice = (slice(min_r, max_r + 1), slice(min_c, max_c + 1))
            # Extract the object shape within its bounding box
            obj_pattern = np.zeros((max_r - min_r + 1, max_c - min_c + 1), dtype=grid.dtype)
            for r, c in obj_pixels:
                obj_pattern[r - min_r, c - min_c] = color

            all_objs.append({
                'color': color,
                'pixels': obj_pixels,
                'bbox': bbox_slice,
                'top_left': (min_r, min_c),
                'relative_pattern': obj_pattern
            })
    return all_objs

def get_combined_bounding_box(objects):
    """ Calculates the minimal bounding box containing all pixels of given objects. """
    if not objects:
        return None
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for obj in objects:
        for r, c in obj['pixels']:
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)
    if min_r == float('inf'): # No pixels found
        return None
    return slice(min_r, max_r + 1), slice(min_c, max_c + 1)

def are_patterns_identical(pattern1, pattern2):
    """ Checks if two numpy arrays representing patterns are identical. """
    if pattern1.shape != pattern2.shape:
        return False
    return np.array_equal(pattern1, pattern2)

def stamp_pattern(output_grid, pattern, top_left_coord):
    """ Overlays the pattern onto the output grid at the specified coordinate. """
    r_start, c_start = top_left_coord
    p_h, p_w = pattern.shape
    g_h, g_w = output_grid.shape

    # Calculate the intersection of the pattern bounds and grid bounds
    r_end = min(r_start + p_h, g_h)
    c_end = min(c_start + p_w, g_w)

    # Calculate slices for pattern and grid
    p_r_slice = slice(0, r_end - r_start)
    p_c_slice = slice(0, c_end - c_start)
    g_r_slice = slice(r_start, r_end)
    g_c_slice = slice(c_start, c_end)

    # Ensure slices are valid (not negative range)
    if g_r_slice.start < g_r_slice.stop and g_c_slice.start < g_c_slice.stop:
         # Apply the pattern: only non-background pixels from the pattern overwrite
        pattern_part = pattern[p_r_slice, p_c_slice]
        target_area = output_grid[g_r_slice, g_c_slice]
        
        # If the pattern template came from a combined bounding box, it might contain 0s
        # that should be stamped. If it came from a single object definition, 0s represent
        # areas outside the object. Let's refine this: always stamp non-zero?
        # The examples suggest stamping the whole template, including background 0s if present (train_1 combined pattern).
        
        # Update: Let's stamp everything from the pattern template.
        output_grid[g_r_slice, g_c_slice] = pattern_part
        
        # # Alternative: Only stamp non-zero pixels from pattern
        # non_zero_mask = pattern_part != 0
        # target_area[non_zero_mask] = pattern_part[non_zero_mask]
        # output_grid[g_r_slice, g_c_slice] = target_area


def transform(input_grid):
    """
    Applies the pattern stamping transformation.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.zeros_like(input_grid)
    grid_h, grid_w = input_grid.shape

    # 1. Find all objects
    all_objects = find_all_objects(input_grid)

    # 2. Separate markers (color 8) and source objects (others, non-0)
    marker_objects = [obj for obj in all_objects if obj['color'] == 8]
    source_objects = [obj for obj in all_objects if obj['color'] != 8 and obj['color'] != 0]

    # Handle edge case: No source objects
    if not source_objects:
        return output_grid.tolist() # Return empty grid if no pattern source

    # Handle edge case: No marker objects
    if not marker_objects:
         # If no markers, what should happen? The examples don't cover this.
         # Assume output is empty grid.
         return output_grid.tolist()

    # 3. Determine Pattern Template
    pattern_template = None
    if len(source_objects) == 1:
        # Single source object: its relative pattern is the template
        pattern_template = source_objects[0]['relative_pattern']
    else:
        # Multiple source objects: check if they are identical
        first_pattern = source_objects[0]['relative_pattern']
        all_identical = True
        for i in range(1, len(source_objects)):
            if not are_patterns_identical(first_pattern, source_objects[i]['relative_pattern']):
                all_identical = False
                break

        if all_identical:
            # Find the top-leftmost source object
            top_leftmost_obj = min(source_objects, key=lambda obj: (obj['top_left'][0], obj['top_left'][1]))
            pattern_template = top_leftmost_obj['relative_pattern']
        else:
            # Not identical: use combined bounding box from input grid
            combined_bbox = get_combined_bounding_box(source_objects)
            if combined_bbox:
                pattern_template = input_grid[combined_bbox]
            else: # Should not happen if source_objects is not empty
                 return output_grid.tolist()


    if pattern_template is None: # Should not happen if source_objects exist
         return output_grid.tolist()


    # 4. Stamping Process
    for marker in marker_objects:
        marker_tl = marker['top_left']
        stamp_pattern(output_grid, pattern_template, marker_tl)

    # 5. Return final grid
    return output_grid.tolist()

```