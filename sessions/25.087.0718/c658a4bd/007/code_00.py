import numpy as np
from collections import deque

"""
Transform the input grid based on object identification, framing, and concentric nesting rules:
1.  Identify all contiguous, non-white objects (4-way adjacency).
2.  Filter out objects with a bounding box area of 1 (singletons).
3.  Identify the remaining object with the largest bounding box area as the 'Frame Object'.
4.  All other remaining objects are 'Nested Objects'.
5.  If no nested objects exist, output a 3x3 grid of the frame color.
6.  Otherwise, determine output size based on the largest nested object's bounding box (+2 padding).
7.  Create the output grid filled with the frame color.
8.  Place nested objects onto the output grid, centered, from largest area to smallest area.
9.  If nested objects exist and the innermost (smallest area) object has odd bounding box dimensions (both height and width), place a red pixel at the absolute center of the output grid.
"""

# Helper function to find connected components (objects) using 4-way connectivity
def find_objects(grid):
    """Finds all connected components of non-background pixels."""
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                q = deque([(r, c)])
                points = set([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # 4-way connectivity
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            points.add((nr, nc))

                bbox = (min_r, min_c, max_r, max_c)
                bbox_h = max_r - min_r + 1
                bbox_w = max_c - min_c + 1
                # Extract grid representation immediately
                obj_grid = np.zeros((bbox_h, bbox_w), dtype=int)
                for pr, pc in points:
                    obj_grid[pr - min_r, pc - min_c] = color

                objects.append({
                    'color': color,
                    'points': points,
                    'bbox': bbox,
                    'grid': obj_grid, # Store minimal grid representation
                    'bbox_h': bbox_h,
                    'bbox_w': bbox_w,
                    'bbox_area': bbox_h * bbox_w,
                 })
    return objects

def transform(input_grid_list):
    """
    Applies the transformation rules to the input grid.
    Input is expected as a list of lists, converted to numpy array internally.
    """
    input_grid = np.array(input_grid_list, dtype=int)

    # 1. Identify and Filter Objects
    all_objects = find_objects(input_grid)
    significant_objects = [obj for obj in all_objects if obj['bbox_area'] > 1]

    # 2. Determine Frame and Nested Objects
    if not significant_objects:
        # If no significant objects, return 3x3 white grid
        return np.zeros((3, 3), dtype=int).tolist()

    # Find frame object (max bbox area)
    significant_objects.sort(key=lambda o: o['bbox_area'], reverse=True)
    frame_object = significant_objects[0]
    frame_color = frame_object['color']

    # Identify nested objects
    nested_objects = significant_objects[1:]

    # 3. Determine Output Grid Size
    if not nested_objects:
        # Only frame object exists (after filtering singletons)
        output_grid = np.full((3, 3), frame_color, dtype=int)
        return output_grid.tolist()
    else:
        # Find largest nested object (already sorted, first in nested_objects list)
        # Note: largest_nested_object was determined before sorting for frame ID,
        #       but since nested_objects is the rest of the sorted list, the
        #       *first* element *after* sorting the whole list by area (desc)
        #       will be the largest *nested* object if nested_objects exist.
        #       Wait, that's not right. Need largest area among nested_objects specifically.
        nested_objects.sort(key=lambda o: o['bbox_area'], reverse=True) # Sort nested desc by area
        largest_nested_object = nested_objects[0] # Largest is now first
        largest_h, largest_w = largest_nested_object['bbox_h'], largest_nested_object['bbox_w']
        output_h = largest_h + 2
        output_w = largest_w + 2

    # 4. Construct Initial Output Grid
    output_grid = np.full((output_h, output_w), frame_color, dtype=int)

    # 5. Place Nested Objects (Largest Area First)
    # The list nested_objects is already sorted by area descending
    for obj in nested_objects:
        obj_h, obj_w = obj['bbox_h'], obj['bbox_w']
        obj_grid_repr = obj['grid'] # Use the stored minimal grid representation

        # Calculate top-left corner for centering within the output grid's inner area
        start_r = (output_h - obj_h) // 2
        start_c = (output_w - obj_w) // 2

        # Place object pixels onto output grid, overwriting frame/previous objects
        for r in range(obj_h):
            for c in range(obj_w):
                if obj_grid_repr[r, c] != 0: # Only copy the object's actual pixels
                     # Check bounds just in case, though centering should be correct
                    if 0 <= start_r + r < output_h and 0 <= start_c + c < output_w:
                         output_grid[start_r + r, start_c + c] = obj_grid_repr[r, c]

    # 6. Add Optional Center Pixel
    if nested_objects: # Ensure there was at least one nested object placed
        # Find innermost object (smallest area)
        # Sort nested_objects by area ascending to find the smallest
        nested_objects.sort(key=lambda o: o['bbox_area'])
        innermost_object = nested_objects[0]
        inner_h, inner_w = innermost_object['bbox_h'], innermost_object['bbox_w']

        # Check if both dimensions of the innermost object's bounding box are odd
        if inner_h % 2 != 0 and inner_w % 2 != 0:
            center_r = output_h // 2
            center_c = output_w // 2
            # Ensure center coords are within grid bounds (should always be true)
            if 0 <= center_r < output_h and 0 <= center_c < output_w:
                output_grid[center_r, center_c] = 2 # Set center to Red

    # 7. Final Result
    return output_grid.tolist()