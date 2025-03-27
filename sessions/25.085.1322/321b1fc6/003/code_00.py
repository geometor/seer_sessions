"""
1. Initialize an output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Identify all distinct connected groups of azure (8) pixels in the input grid. These are the 'markers'. If no markers exist, return the initial white output grid.
3. Identify all distinct connected groups of pixels that are *not* white (0) and *not* azure (8). These are the 'source components'.
4. Determine the 'template' pattern based on the source components:
    a. If there are no source components, the template is effectively empty, and the output grid remains white.
    b. If there is exactly one source component, the template is its 'relative_pattern' (the component's shape within its own bounding box, with other pixels as background 0).
    c. If there are multiple source components:
        i. Check if all source components have the exact same 'relative_pattern'.
        ii. If YES (all identical): Find the source component whose top-left corner has the smallest row index, breaking ties with the smallest column index. The template is the 'relative_pattern' of this specific component.
        iii. If NO (components differ): Find the single smallest bounding box that encloses *all* pixels of *all* source components. The template is the rectangular region copied directly from the *input grid* corresponding to this combined bounding box (this includes any background pixels within the box).
5. For each identified marker:
    a. Find the coordinate (row, column) of its top-leftmost pixel.
    b. Copy the determined template onto the output grid, placing the template's top-left corner at the marker's top-left coordinate. Pixels from the template overwrite the output grid. Ensure the template is clipped if it extends beyond the grid boundaries.
6. Return the final modified output grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def find_connected_components(grid, target_colors=None):
    """
    Finds all connected components for specified colors or all non-background colors.

    Args:
        grid (np.array): The input grid.
        target_colors (list or set, optional): A collection of integer colors
            to find objects for. If None, finds objects for all colors except 0.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples),
              'bbox' (slice tuple), 'top_left' (r, c),
              'relative_pattern' (np.array of the object within its bbox).
              Returns empty list if no objects found.
    """
    objects = []
    if target_colors is None:
        colors_present = np.unique(grid)
        target_colors = [c for c in colors_present if c != 0]
    if not target_colors:
        return objects

    processed_pixels = np.zeros_like(grid, dtype=bool) # Keep track of visited pixels

    for color in target_colors:
        # Create mask for the current color, considering only unprocessed pixels
        mask = (grid == color) & (~processed_pixels)
        if not np.any(mask):
            continue

        labeled_array, num_features = label(mask)
        found_locs = find_objects(labeled_array)

        for i in range(num_features):
            obj_index = i + 1
            obj_slice = found_locs[i]
            
            # Find pixels belonging to this component *globally*
            obj_coords_global = np.argwhere(labeled_array == obj_index)

            # Check if any part of this object has already been processed (shouldn't happen with current logic but safe check)
            if np.any(processed_pixels[obj_coords_global[:, 0], obj_coords_global[:, 1]]):
                continue

            # Mark pixels as processed
            processed_pixels[obj_coords_global[:, 0], obj_coords_global[:, 1]] = True
            
            obj_pixels_list = [tuple(coord) for coord in obj_coords_global]

            # Calculate precise bounding box and top-left
            min_r = np.min(obj_coords_global[:, 0])
            min_c = np.min(obj_coords_global[:, 1])
            max_r = np.max(obj_coords_global[:, 0])
            max_c = np.max(obj_coords_global[:, 1])
            bbox = (slice(min_r, max_r + 1), slice(min_c, max_c + 1))
            top_left = (min_r, min_c)
            
            # Create relative pattern (object shape in its bbox, rest 0)
            height = max_r - min_r + 1
            width = max_c - min_c + 1
            relative_pattern = np.zeros((height, width), dtype=grid.dtype)
            for r, c in obj_pixels_list:
                relative_pattern[r - min_r, c - min_c] = color

            objects.append({
                'color': color,
                'pixels': obj_pixels_list,
                'bbox': bbox,
                'top_left': top_left,
                'relative_pattern': relative_pattern
            })

    # Sort objects primarily by top-left row, then column for consistent ordering
    objects.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    return objects


def get_combined_bounding_box(objects):
    """ Calculates the minimal bounding box containing all pixels of given objects. """
    if not objects:
        return None
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    pixel_found = False
    for obj in objects:
        for r, c in obj['pixels']:
            pixel_found = True
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)
    if not pixel_found:
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
    if r_start < 0 or c_start < 0: # Avoid stamping outside grid from negative indices
        # Adjust pattern and start coords if starting negatively
        # This scenario might indicate an issue elsewhere, but let's clip defensively
         p_r_offset = 0
         p_c_offset = 0
         if r_start < 0:
             p_r_offset = -r_start
             r_start = 0
         if c_start < 0:
             p_c_offset = -c_start
             c_start = 0
         pattern = pattern[p_r_offset:, p_c_offset:] # Clip pattern from top/left


    p_h, p_w = pattern.shape
    g_h, g_w = output_grid.shape

    # Calculate the intersection bounds
    r_end = min(r_start + p_h, g_h)
    c_end = min(c_start + p_w, g_w)

    # Calculate slices for pattern and grid based on intersection
    p_r_slice = slice(0, r_end - r_start)
    p_c_slice = slice(0, c_end - c_start)
    g_r_slice = slice(r_start, r_end)
    g_c_slice = slice(c_start, c_end)

    # Ensure slices are valid (have positive range) before attempting assignment
    if g_r_slice.start < g_r_slice.stop and g_c_slice.start < g_c_slice.stop:
        output_grid[g_r_slice, g_c_slice] = pattern[p_r_slice, p_c_slice]


def transform(input_grid):
    """
    Transforms the input grid by stamping a derived pattern at locations marked by azure pixels.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.zeros_like(input_grid)
    
    # 1. Find marker objects (color 8)
    marker_color = 8
    marker_objects = find_connected_components(input_grid, target_colors=[marker_color])

    # 2. Find source objects (all colors except 0 and 8)
    all_colors = np.unique(input_grid)
    source_colors = [c for c in all_colors if c != 0 and c != marker_color]
    source_objects = find_connected_components(input_grid, target_colors=source_colors)

    # 3. Handle edge cases: no markers or no source objects
    if not marker_objects:
        return output_grid.tolist() # Return empty grid if no markers
    if not source_objects:
        return output_grid.tolist() # Return empty grid if no source pattern

    # 4. Determine the template pattern
    template = None
    if len(source_objects) == 1:
        # Case: Single source object
        template = source_objects[0]['relative_pattern']
    else:
        # Case: Multiple source objects
        first_pattern = source_objects[0]['relative_pattern']
        all_identical = True
        for i in range(1, len(source_objects)):
            if not are_patterns_identical(first_pattern, source_objects[i]['relative_pattern']):
                all_identical = False
                break

        if all_identical:
            # Subcase: All source objects are identical - use the top-leftmost one's pattern
            # Objects are already sorted by top-left position in find_connected_components
            template = source_objects[0]['relative_pattern']
        else:
            # Subcase: Source objects differ - use combined bounding box from input grid
            combined_bbox = get_combined_bounding_box(source_objects)
            if combined_bbox:
                template = input_grid[combined_bbox]
            else:
                 # This should not happen if source_objects is not empty
                 return output_grid.tolist() 

    if template is None: # Should not happen if source_objects exist
         return output_grid.tolist()

    # 5. Stamp the template for each marker
    for marker in marker_objects:
        marker_tl = marker['top_left']
        stamp_pattern(output_grid, template, marker_tl)

    # 6. Return the final grid
    return output_grid.tolist()