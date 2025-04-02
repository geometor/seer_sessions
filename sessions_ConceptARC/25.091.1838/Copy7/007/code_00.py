import numpy as np
from collections import deque, Counter
import math

"""
Identifies the two largest non-white objects in the input grid.
One object (source) contains an internal pattern composed of pixels of a single color 
different from the object's primary color and the background (white).
This pattern is then transferred to the second largest object (target).
The transfer is based on aligning the centers of the bounding boxes of the source 
and target objects. The translation vector calculated from this center alignment 
is applied to the absolute coordinates of the source pattern pixels to determine 
their new locations. The pattern color replaces the existing color at these new 
target locations only if the new location falls within the target object's 
original bounding box. All other pixels remain unchanged.
"""

# === Helper Functions ===

def _get_neighbors(r, c, rows, cols):
    """ Helper function to get valid 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects_bfs(grid):
    """ Finds connected components of non-white pixels using BFS. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 1

    for r in range(rows):
        for c in range(cols):
            # Start BFS from an unvisited non-white pixel
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                obj_colors = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Perform BFS to find all connected non-white pixels for this object
                while q:
                    curr_r, curr_c = q.popleft()

                    obj_pixels.append((curr_r, curr_c))
                    obj_colors.append(grid[curr_r, curr_c])

                    # Update bounding box coordinates (inclusive)
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols):
                        if grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels:
                    # Determine primary color (most frequent non-white color in the object)
                    non_white_colors = [col for col in obj_colors if col != 0]
                    if not non_white_colors: continue # Skip if only background somehow included
                    primary_color = Counter(non_white_colors).most_common(1)[0][0]
                    
                    # Bounding box (exclusive max: min_row, min_col, max_row + 1, max_col + 1)
                    bbox = (min_r, min_c, max_r + 1, max_c + 1) 

                    objects.append({
                        'id': object_id_counter,
                        'pixels': obj_pixels,
                        'bbox': bbox,
                        'primary_color': primary_color,
                        'size': len(obj_pixels) # Use actual pixel count
                    })
                    object_id_counter += 1

    # Sort objects by size (descending) to easily find the largest ones
    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects

def _calculate_bbox_center(bbox):
    """ Calculates the geometric center of a bounding box. """
    min_r, min_c, max_r, max_c = bbox # bbox uses exclusive max
    center_r = min_r + (max_r - min_r) / 2.0
    center_c = min_c + (max_c - min_c) / 2.0
    return center_r, center_c

def _find_pattern_in_bbox(grid, obj):
    """ 
    Checks an object's bounding box for an internal pattern.
    Returns (found_pattern, pattern_color, pattern_absolute_coords)
    """
    rows, cols = grid.shape
    bbox = obj['bbox']
    min_r, min_c, max_r, max_c = bbox # Exclusive max convention
    primary_color = obj['primary_color']
    
    found_pattern = False
    potential_pattern_color = -1 # Initialize with invalid color
    abs_coords = []

    # Iterate through the bounding box of the potential source
    for r in range(min_r, max_r):
        for c in range(min_c, max_c):
             # Check grid bounds just in case (should be redundant if bbox is correct)
            if 0 <= r < rows and 0 <= c < cols:
                color = grid[r, c]
                # Look for a color that is not background (0) and not the object's primary color
                if color != 0 and color != primary_color:
                    # If this is the first pattern pixel found, store its color
                    if not found_pattern:
                        potential_pattern_color = color
                        found_pattern = True
                    
                    # Ensure all pattern pixels have the same color (task assumption)
                    if color == potential_pattern_color:
                        # Store absolute coordinates
                        abs_coords.append((r, c))
                    else:
                        # Found a different internal color - this doesn't fit the pattern model
                        return False, -1, [] 
                        
    return found_pattern, potential_pattern_color, abs_coords

# === Main Transformation Function ===

def transform(input_grid):
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Identify all non-white objects using BFS
    objects = _find_objects_bfs(input_grid)

    # 3. Need at least two objects for the transformation
    if len(objects) < 2:
        return output_grid # No transformation possible

    # 4. Assume the two largest objects are the source/target pair
    obj_a = objects[0]
    obj_b = objects[1]

    # 5. Try to find the source, target, pattern color, and pattern absolute coordinates
    source_object = None
    target_object = None
    pattern_color = None
    pattern_coords_absolute = [] # Store absolute coordinates

    # Check Object A as potential source
    found_in_a, color_a, coords_a = _find_pattern_in_bbox(input_grid, obj_a)
    if found_in_a:
        source_object = obj_a
        target_object = obj_b
        pattern_color = color_a
        pattern_coords_absolute = coords_a
    else:
        # Check Object B as potential source
        found_in_b, color_b, coords_b = _find_pattern_in_bbox(input_grid, obj_b)
        if found_in_b:
            source_object = obj_b
            target_object = obj_a
            pattern_color = color_b
            pattern_coords_absolute = coords_b

    # 6. If no source/pattern was identified, return the original grid
    if source_object is None or pattern_color is None or not pattern_coords_absolute:
        return output_grid

    # 7. Calculate centers and translation vector
    source_bbox = source_object['bbox']
    target_bbox = target_object['bbox']

    source_center_r, source_center_c = _calculate_bbox_center(source_bbox)
    target_center_r, target_center_c = _calculate_bbox_center(target_bbox)

    # Translation = Target Center - Source Center
    delta_r = target_center_r - source_center_r
    delta_c = target_center_c - source_center_c

    # 8. Apply the translated pattern, clipping to the target object's bounding box
    min_rt, min_ct, max_rt, max_ct = target_bbox # Target bbox for clipping

    for src_r, src_c in pattern_coords_absolute:
        # Calculate potential target coordinates by applying the translation vector
        # Round to nearest integer for pixel coordinates
        target_r = round(src_r + delta_r)
        target_c = round(src_c + delta_c)

        # Validate: Check if the calculated coordinate is within grid bounds
        is_within_grid = (0 <= target_r < rows and 0 <= target_c < cols)
        
        # Validate: Check if the calculated coordinate is within the target's bounding box
        is_within_target_bbox = (min_rt <= target_r < max_rt and min_ct <= target_c < max_ct)

        # Apply the pattern color only if BOTH conditions are met
        if is_within_grid and is_within_target_bbox:
            output_grid[target_r, target_c] = pattern_color

    # 9. Return the modified grid
    return output_grid