```python
import numpy as np
from collections import deque
import itertools

"""
Transforms an input grid by duplicating a composite structure (a 'container' object 
and the 'contained' objects within its bounding box) to a new location. The new 
location is determined by the position of an 'orphan' object, typically one that 
shares characteristics (like color) with a contained object. The process involves:
1. Identifying all distinct objects (contiguous non-white pixels).
2. Identifying the 'container' object, defined as an object whose bounding box 
   inclusively encloses the bounding box of at least one other object of a 
   different color.
3. Identifying 'contained' objects enclosed within the container's bounding box.
4. Identifying 'orphan' objects (neither container nor contained).
5. Selecting a 'primary orphan' (often matching a contained object's color) to 
   dictate placement.
6. Calculating the target location for the copy, maintaining a 2-pixel gap from 
   the primary orphan's original position.
7. Creating an output grid by copying the input.
8. Removing all orphan objects from the output grid.
9. Extracting the pattern (container's bounding box region) from the original input.
10. Pasting the pattern onto the output grid at the target location.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid using Breadth-First Search.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dicts, where each dict represents an object and contains:
              - 'id': A unique integer identifier for the object.
              - 'coords': set of (row, col) coordinates.
              - 'bbox': tuple (min_r, min_c, max_r, max_c).
              - 'color': int color value.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r, min_c, max_r, max_c = min(min_r, row), min(min_c, col), max(max_r, row), max(max_c, col)

                    # Check neighbors (4-directional: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_coords:
                    bounding_box = (min_r, min_c, max_r, max_c)
                    objects.append({'id': object_id_counter, 'coords': obj_coords, 'bbox': bounding_box, 'color': color})
                    object_id_counter += 1
    return objects

def is_inclusively_enclosed(inner_box, outer_box):
    """
    Checks if inner_box is inclusively inside outer_box (edges can touch).
    Requires the boxes to be distinct.

    Args:
        inner_box (tuple): Bbox (min_r, min_c, max_r, max_c).
        outer_box (tuple): Bbox (min_r, min_c, max_r, max_c).

    Returns:
        bool: True if inner_box is enclosed by outer_box, False otherwise.
    """
    if inner_box == outer_box: # An object cannot enclose itself
        return False
    min_r1, min_c1, max_r1, max_c1 = inner_box
    min_r2, min_c2, max_r2, max_c2 = outer_box
    return min_r1 >= min_r2 and min_c1 >= min_c2 and max_r1 <= max_r2 and max_c1 <= max_c2

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify all distinct objects
    all_objects = find_objects(input_np)
    if not all_objects:
        return input_grid # Return original if no objects

    # 2. & 3. Identify Container and Contained Objects
    container = None
    contained_objects_map = {} # Store {container_id: [contained_obj1, contained_obj2,...]}

    for obj_i in all_objects:
        current_contained = []
        for obj_j in all_objects:
            if obj_i['id'] == obj_j['id']:
                continue
            # Check for enclosure and different color
            if obj_i['color'] != obj_j['color'] and is_inclusively_enclosed(obj_j['bbox'], obj_i['bbox']):
                 current_contained.append(obj_j)

        if current_contained: # If obj_i encloses at least one object of a different color
             contained_objects_map[obj_i['id']] = current_contained
             # Simple selection: Assume the first object found that meets the criteria is the container
             # More robust logic might be needed for complex cases (e.g., largest area, most enclosed)
             if container is None:
                 container = obj_i

    # If no container identified based on criteria, return original
    if container is None:
        # print("Warning: No container found meeting criteria.")
        return input_grid

    container_id = container['id']
    container_bbox = container['bbox']
    contained_objects = contained_objects_map.get(container_id, [])
    contained_ids = {obj['id'] for obj in contained_objects}
    contained_colors = {obj['color'] for obj in contained_objects}

    # 4. Identify Orphan Objects
    orphan_objects = []
    for obj in all_objects:
        if obj['id'] != container_id and obj['id'] not in contained_ids:
            orphan_objects.append(obj)

    if not orphan_objects:
        # print("Warning: Container and contained objects found, but no orphans.")
        return input_grid # Needs an orphan to determine placement

    # 5. Select Primary Orphan
    primary_orphan = None
    # Look for an orphan whose color matches a contained object's color
    for orphan in orphan_objects:
        if orphan['color'] in contained_colors:
            primary_orphan = orphan
            break # Use the first one found

    # Fallback: If no orphan matches contained color, use the first orphan found
    if primary_orphan is None:
        primary_orphan = orphan_objects[0]
        
    orphan_bbox = primary_orphan['bbox']

    # 6. Calculate Target Location
    c_min_r, c_min_c, c_max_r, c_max_c = container_bbox
    o_min_r, o_min_c, o_max_r, o_max_c = orphan_bbox
    target_row, target_col = -1, -1

    # Determine relative position and calculate target coordinate with 2-pixel gap
    # Check primary directions based on non-overlapping bounding boxes
    is_below = o_min_r > c_max_r
    is_right = o_min_c > c_max_c
    is_above = o_max_r < c_min_r
    is_left = o_max_c < c_min_c

    if is_below:
        target_row = o_min_r - 2
        target_col = c_min_c
    elif is_right:
        target_row = c_min_r
        target_col = o_min_c - 2
    elif is_above: # Added for completeness, untested by examples
        target_row = o_max_r + 2 # Place top edge 2 pixels below orphan's bottom edge
        target_col = c_min_c
    elif is_left: # Added for completeness, untested by examples
        target_row = c_min_r
        target_col = o_max_c + 2 # Place left edge 2 pixels right of orphan's right edge
    else:
        # Handle ambiguous cases if necessary (e.g., diagonal, overlapping)
        # print(f"Warning: Ambiguous relative position between container {container_bbox} and primary orphan {orphan_bbox}.")
        return input_grid # Cannot determine placement

    # 7. Create Output Grid
    output_np = np.copy(input_np)

    # 8. Remove ALL Orphan Objects
    for orphan in orphan_objects:
        for r, c in orphan['coords']:
            if 0 <= r < rows and 0 <= c < cols:
                output_np[r, c] = 0 # Set orphan pixels to background color

    # 9. Extract Pattern from ORIGINAL Input Grid
    pattern = input_np[c_min_r : c_max_r + 1, c_min_c : c_max_c + 1]
    pattern_h, pattern_w = pattern.shape

    # 10. Place Pattern onto Output Grid (with clipping)
    if target_row != -1 and target_col != -1 and pattern_h > 0 and pattern_w > 0:
        # Define the target slice in the output grid
        end_row = target_row + pattern_h
        end_col = target_col + pattern_w

        # Calculate clipping boundaries for pasting
        paste_start_row = max(0, target_row)
        paste_start_col = max(0, target_col)
        paste_end_row = min(rows, end_row)
        paste_end_col = min(cols, end_col)

        # Calculate corresponding slice from the pattern to copy
        pattern_start_row = max(0, -target_row)
        pattern_start_col = max(0, -target_col)
        pattern_end_row = pattern_start_row + (paste_end_row - paste_start_row)
        pattern_end_col = pattern_start_col + (paste_end_col - paste_start_col)

        # Paste if the calculated slices are valid (have positive dimensions)
        if paste_start_row < paste_end_row and paste_start_col < paste_end_col:
            output_np[paste_start_row:paste_end_row, paste_start_col:paste_end_col] = \
                pattern[pattern_start_row:pattern_end_row, pattern_start_col:pattern_end_col]
        # else: # Debugging: uncomment if needed
            # print(f"Warning: Calculated placement ({target_row},{target_col}) resulted in no valid area to paste.")
            # print(f"Paste Area: ({paste_start_row}:{paste_end_row}, {paste_start_col}:{paste_end_col})")
            # print(f"Pattern Area: ({pattern_start_row}:{pattern_end_row}, {pattern_start_col}:{pattern_end_col})")

    # else: # Debugging: uncomment if needed
        # print("Warning: Invalid target coordinates or pattern dimensions for pasting.")
        # print(f"Target: ({target_row},{target_col}), Pattern Shape: ({pattern_h},{pattern_w})")

    # Convert back to list of lists for ARC standard
    return output_np.tolist()
```