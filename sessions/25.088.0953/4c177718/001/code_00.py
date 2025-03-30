import numpy as np
from collections import deque

"""
Identifies a horizontal gray separator line in the input grid.
Finds three colored objects above the line and one blue key object below the line.
Determines which upper object's shape matches the key object's shape.
Discards the matched object.
Stacks the remaining two upper objects vertically in a new 9-row output grid.
The stacking order (which object is on top) depends on the horizontal position (Left, Middle, Right) of the discarded object.
  - Discard Left: Right object on top of Middle object.
  - Discard Middle: Left object on top of Right object.
  - Discard Right: Left object on top of Middle object.
The vertical starting position of the stack in the output grid depends on the vertical position of the key object (High/Low) and the horizontal position of the discarded object.
  - Key Low & Discard Left: Start Row 2
  - Key High & Discard Left: Start Row 0
  - Key Low & Discard Middle/Right: Start Row 1
  - Key High & Discard Middle/Right: Start Row 3
The stacked objects are centered horizontally in the output grid.
"""

def find_separator_row(grid):
    """Finds the row index containing the horizontal gray line (color 5)."""
    for r, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return r
    return -1 # Should not happen based on examples

def find_objects(grid, ignore_colors=[0, 5]):
    """
    Finds connected objects of the same color in the grid, ignoring specified colors.
    Uses Breadth-First Search (BFS).
    Returns a list of objects, where each object is a dict containing:
    'color', 'coords' (set of (r, c) tuples), 'bbox' (min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited or grid[r, c] in ignore_colors:
                continue

            color = grid[r, c]
            obj_coords = set()
            q = deque([(r, c)])
            visited.add((r, c))
            min_r, min_c = r, c
            max_r, max_c = r, c

            while q:
                row, col = q.popleft()
                obj_coords.add((row, col))
                min_r = min(min_r, row)
                min_c = min(min_c, col)
                max_r = max(max_r, row)
                max_c = max(max_c, col)

                # Check 8 neighbors (including diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))

            objects.append({
                'color': color,
                'coords': obj_coords,
                'bbox': (min_r, min_c, max_r, max_c)
            })
    return objects

def get_relative_shape(obj):
    """
    Calculates the shape of an object relative to its bounding box top-left corner.
    Returns a frozenset of (dr, dc) tuples.
    """
    min_r, min_c, _, _ = obj['bbox']
    shape = set()
    for r, c in obj['coords']:
        shape.add((r - min_r, c - min_c))
    return frozenset(shape) # Use frozenset to make it hashable for comparison

def get_object_dims(obj):
    """Calculates the height and width of an object's bounding box."""
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def draw_object(output_grid, obj, target_start_row, target_start_col):
    """Draws an object onto the output grid at the specified top-left position."""
    min_r, min_c, _, _ = obj['bbox']
    for r, c in obj['coords']:
        dr = r - min_r
        dc = c - min_c
        out_r = target_start_row + dr
        out_c = target_start_col + dc
        # Check bounds before drawing
        if 0 <= out_r < output_grid.shape[0] and 0 <= out_c < output_grid.shape[1]:
            output_grid[out_r, out_c] = obj['color']

def transform(input_grid):
    """
    Applies the transformation logic described in the docstring.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_height = 9

    # 1. Find separator and objects
    separator_row = find_separator_row(input_np)
    if separator_row == -1:
        # Fallback or error handling if separator not found
        return [[0]*width for _ in range(output_height)] 
        
    all_objects = find_objects(input_np)

    # 2. Separate upper and lower objects
    upper_objects = [obj for obj in all_objects if obj['bbox'][0] < separator_row]
    lower_objects = [obj for obj in all_objects if obj['bbox'][0] > separator_row]

    # Validate assumptions (3 upper, 1 lower, lower is blue)
    if len(upper_objects) != 3 or len(lower_objects) != 1 or lower_objects[0]['color'] != 1:
         # Fallback or error handling if assumptions invalid
        return [[0]*width for _ in range(output_height)] 

    key_object = lower_objects[0]

    # 3. Sort upper objects by horizontal position (using min_c)
    upper_objects.sort(key=lambda obj: obj['bbox'][1])
    position_map = {i: obj for i, obj in enumerate(upper_objects)} # 0:Left, 1:Middle, 2:Right

    # 4. Find the matched object
    key_shape = get_relative_shape(key_object)
    matched_object = None
    matched_object_pos_idx = -1
    kept_objects = []

    for i, obj in enumerate(upper_objects):
        obj['shape'] = get_relative_shape(obj)
        obj['dims'] = get_object_dims(obj)
        if obj['shape'] == key_shape:
            matched_object = obj
            matched_object_pos_idx = i
        else:
            kept_objects.append(obj)

    if matched_object is None:
        # Fallback or error handling if no match found
        return [[0]*width for _ in range(output_height)] 

    # 5. Determine stacking order
    top_object = None
    bottom_object = None
    if matched_object_pos_idx == 0: # Matched Left
        # Right kept obj above Middle kept obj
        # Kept objects are already sorted by original position
        # So kept_objects[0] is Middle, kept_objects[1] is Right
        top_object = kept_objects[1]
        bottom_object = kept_objects[0]
    elif matched_object_pos_idx == 1: # Matched Middle
        # Left kept obj above Right kept obj
        # kept_objects[0] is Left, kept_objects[1] is Right
        top_object = kept_objects[0]
        bottom_object = kept_objects[1]
    elif matched_object_pos_idx == 2: # Matched Right
        # Left kept obj above Middle kept obj
        # kept_objects[0] is Left, kept_objects[1] is Middle
        top_object = kept_objects[0]
        bottom_object = kept_objects[1]

    # 6. Determine key object vertical position
    key_min_row = key_object['bbox'][0]
    # Using row 10 as the threshold based on examples (separator at 5)
    # Example 1&3 key starts row 11 (Low). Example 2&4 key starts row 9 (High).
    is_key_high = key_min_row < 10 

    # 7. Determine output start row for the top object
    output_start_row = 0
    if is_key_high:
        if matched_object_pos_idx == 0: # Match Left
            output_start_row = 0
        else: # Match Middle or Right
            output_start_row = 3
    else: # Key Low
        if matched_object_pos_idx == 0: # Match Left
            output_start_row = 2
        else: # Match Middle or Right
            output_start_row = 1

    # 8. Create output grid
    output_grid = np.zeros((output_height, width), dtype=int)

    # 9. Calculate placement and draw top object
    top_height, top_width = top_object['dims']
    top_start_col = (width - top_width) // 2
    draw_object(output_grid, top_object, output_start_row, top_start_col)

    # 10. Calculate placement and draw bottom object
    bottom_start_row = output_start_row + top_height # Place immediately below
    bottom_height, bottom_width = bottom_object['dims']
    bottom_start_col = (width - bottom_width) // 2
    draw_object(output_grid, bottom_object, bottom_start_row, bottom_start_col)

    # 11. Return as list of lists
    return output_grid.tolist()