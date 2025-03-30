import numpy as np
from collections import deque

"""
Identifies a horizontal gray separator line (row 5) in the 15x15 input grid.
Finds three colored objects above the line (Left, Middle, Right) and one blue key object below.
Analyzes the key object's shape (Hollow, Plus, Diagonal) and vertical position (High if top row < 10, Low otherwise).
Matches the key object's shape to one of the upper objects (always the Left object in examples).
Selects the Matched Object (Left) and the Right upper object for the output.
Determines the stacking order of these two selected objects based on Key Type and Key Height:
  - Base Order: Hollow/Diagonal keys -> Right object on top; Plus key -> Left object on top.
  - Modification: If Key Type is Hollow AND Key Height is High, flip the Base Order.
Determines the vertical starting row for the top object in the 9x15 output grid based on Key Type and Key Height:
  - High Key: Hollow -> Row 3, Diagonal -> Row 0, Plus -> Row 1.
  - Low Key: Hollow -> Row 2. (Other types not observed for Low key).
Constructs the output grid by stacking the selected objects in the determined order, starting at the calculated row, and centered horizontally.
"""

# --- Constants for Shape Definitions ---
SHAPE_HOLLOW = frozenset({(0, 1), (1, 2), (2, 1), (0, 0), (2, 0), (0, 2), (2, 2), (1, 0)})
SHAPE_PLUS = frozenset({(0, 1), (1, 2), (2, 1), (1, 0), (1, 1)})
SHAPE_DIAGONAL = frozenset({(0, 2), (2, 2), (0, 0), (1, 1), (2, 0)})

SHAPE_TYPE_MAP = {
    SHAPE_HOLLOW: "Hollow",
    SHAPE_PLUS: "Plus",
    SHAPE_DIAGONAL: "Diagonal"
}

# --- Helper Functions ---

def pad_grid(grid_list):
    """Pads a potentially ragged grid_list to be rectangular."""
    max_width = 0
    if not grid_list: return [] 
    for row in grid_list:
        if isinstance(row, (list, tuple)):
            max_width = max(max_width, len(row))
        else:
           pass # Assume rows are lists/tuples

    padded_grid = []
    for row in grid_list:
         if isinstance(row, (list, tuple)):
            # Ensure row elements are integers, default invalid elements to 0
            processed_row = []
            for x in row:
                try:
                    processed_row.append(int(x))
                except (ValueError, TypeError):
                    processed_row.append(0) # Default invalid cell to white
            padded_row = processed_row + [0] * (max_width - len(processed_row)) 
            padded_grid.append(padded_row)
         else:
            padded_grid.append([0] * max_width)
            
    return padded_grid

def find_separator_row(grid):
    """Finds the row index containing the horizontal gray line (color 5)."""
    # Expects numpy array
    rows, cols = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == 5):
            return r
    return -1 # Separator not found

def find_objects(grid, ignore_colors=[0, 5]):
    """
    Finds connected objects of the same color in the grid, ignoring specified colors.
    Uses Breadth-First Search (BFS). Handles numpy array input.
    Returns a list of objects, where each object is a dict containing:
    'color', 'coords' (set of (r, c) tuples), 'bbox' (min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Ensure grid value is treated as int for comparison
            current_pixel = int(grid[r, c]) 
            if (r, c) in visited or current_pixel in ignore_colors:
                continue

            color = current_pixel
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
                           (nr, nc) not in visited and int(grid[nr, nc]) == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))

            if obj_coords: # Only add if an object was actually found
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
    if not obj or 'coords' not in obj or not obj['coords']:
         return frozenset() # Return empty for invalid object
    min_r, min_c, _, _ = obj['bbox']
    shape = set()
    for r, c in obj['coords']:
        shape.add((r - min_r, c - min_c))
    return frozenset(shape) # Use frozenset to make it hashable for comparison

def get_object_dims(obj):
    """Calculates the height and width of an object's bounding box."""
    if not obj or 'bbox' not in obj:
        return 0, 0
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def draw_object(output_grid, obj, target_start_row, target_start_col):
    """Draws an object onto the output grid at the specified top-left position."""
    if not obj or 'coords' not in obj or not obj['coords']:
        return # Do nothing if object is invalid
    min_r, min_c, _, _ = obj['bbox']
    out_rows, out_cols = output_grid.shape
    for r, c in obj['coords']:
        dr = r - min_r
        dc = c - min_c
        out_r = target_start_row + dr
        out_c = target_start_col + dc
        # Check bounds before drawing
        if 0 <= out_r < out_rows and 0 <= out_c < out_cols:
            output_grid[out_r, out_c] = obj['color']

# --- Main Transformation Function ---

def transform(input_grid):
    # 0. Initialization and Input Validation
    padded_input_list = pad_grid(input_grid)
    if not padded_input_list:
        return [[0]*15 for _ in range(9)] # Return default empty grid if input is bad
        
    input_np = np.array(padded_input_list, dtype=int)
    height, width = input_np.shape
    output_height = 9
    output_width = width # Output width is same as input
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 1. Identify Components
    separator_row = find_separator_row(input_np)
    if separator_row == -1:
        # Fallback: Maybe return input or default grid if separator missing
        return output_grid.tolist() 
        
    all_objects = find_objects(input_np)

    upper_objects_raw = [obj for obj in all_objects if obj['bbox'][0] < separator_row]
    lower_objects = [obj for obj in all_objects if obj['bbox'][0] > separator_row]

    # Validate assumptions
    if len(upper_objects_raw) != 3 or len(lower_objects) != 1 or lower_objects[0]['color'] != 1:
        # Fallback if assumptions invalid
        return output_grid.tolist() 

    key_object = lower_objects[0]
    # Sort upper objects by horizontal position (using min_c) and add original index
    upper_objects = sorted(upper_objects_raw, key=lambda obj: obj['bbox'][1])
    for i, obj in enumerate(upper_objects):
        obj['original_index'] = i # 0:Left, 1:Middle, 2:Right

    # 2. Analyze Key Object
    key_shape = get_relative_shape(key_object)
    key_min_row = key_object['bbox'][0]
    
    key_type = SHAPE_TYPE_MAP.get(key_shape, "Unknown")
    is_key_high = key_min_row < 10 # High if top row < 10

    if key_type == "Unknown":
         return output_grid.tolist() # Cannot proceed if key shape is unrecognized

    # 3. Find Match
    matched_object = None
    matched_object_idx = -1
    for obj in upper_objects:
        obj['shape'] = get_relative_shape(obj)
        if obj['shape'] == key_shape:
            matched_object = obj
            matched_object_idx = obj['original_index']
            break # Found the match

    if matched_object is None:
        return output_grid.tolist() # Cannot proceed without a match

    # 4. Select Objects for Output
    # In all examples, Left (idx 0) matches. Select Matched (0) and Right (2).
    # Generalizing (though not strictly needed for training examples):
    if matched_object_idx == 0: # Matched Left
        non_matched_object = upper_objects[2] # Select Right
    elif matched_object_idx == 2: # Matched Right
        non_matched_object = upper_objects[0] # Select Left
    else: # Matched Middle (idx 1)
        non_matched_object = upper_objects[2] # Select Right (based on assumption)

    objects_to_stack = [matched_object, non_matched_object]

    # 5. Determine Stacking Order
    top_object = None
    bottom_object = None
    
    # Determine base order: Leftmost original index vs Rightmost original index
    obj_a, obj_b = objects_to_stack[0], objects_to_stack[1]
    left_orig_obj = obj_a if obj_a['original_index'] < obj_b['original_index'] else obj_b
    right_orig_obj = obj_b if obj_a['original_index'] < obj_b['original_index'] else obj_a

    # Base order: Rightmost on top for Hollow/Diagonal, Leftmost on top for Plus
    if key_type == "Hollow" or key_type == "Diagonal":
        base_top = right_orig_obj
        base_bottom = left_orig_obj
    else: # key_type == "Plus"
        base_top = left_orig_obj
        base_bottom = right_orig_obj

    # Modification: Flip for Hollow + High Key
    if key_type == "Hollow" and is_key_high:
        top_object = base_bottom
        bottom_object = base_top
    else:
        top_object = base_top
        bottom_object = base_bottom
        
    # 6. Determine Vertical Placement
    output_start_row = -1
    if is_key_high:
        if key_type == "Hollow": output_start_row = 3
        elif key_type == "Diagonal": output_start_row = 0
        elif key_type == "Plus": output_start_row = 1
    else: # Key is Low
        if key_type == "Hollow": output_start_row = 2
        # Add fallbacks or assumptions for Diagonal/Plus Low if needed
        # else: output_start_row = 1 # Default assumption?

    if output_start_row == -1:
        return output_grid.tolist() # Cannot place if start row is undetermined

    # 7. Construct Output Grid
    top_height, top_width = get_object_dims(top_object)
    top_start_col = (output_width - top_width) // 2
    draw_object(output_grid, top_object, output_start_row, top_start_col)

    bottom_start_row = output_start_row + top_height # Place immediately below
    bottom_height, bottom_width = get_object_dims(bottom_object)
    bottom_start_col = (output_width - bottom_width) // 2
    draw_object(output_grid, bottom_object, bottom_start_row, bottom_start_col)

    # Return as list of lists
    return output_grid.tolist()