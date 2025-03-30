
Previous Code:
```python
import numpy as np
from collections import deque

# --- Constants for Shape Definitions ---
SHAPE_HOLLOW = frozenset({(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}) # 8 pixels
SHAPE_PLUS = frozenset({(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}) # 5 pixels
SHAPE_DIAGONAL = frozenset({(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)}) # 5 pixels

# Map shapes to names for clarity
SHAPE_TYPE_MAP = {
    SHAPE_HOLLOW: "Hollow",
    SHAPE_PLUS: "Plus",
    SHAPE_DIAGONAL: "Diagonal"
}
# Inverse map for convenience if needed later
# TYPE_SHAPE_MAP = {v: k for k, v in SHAPE_TYPE_MAP.items()}

# --- Helper Functions ---

def pad_grid(grid_list):
    """
    Pads a potentially ragged grid_list (list of lists or tuples) or converts
    a NumPy array to a padded list of lists of integers.
    Ensures all rows have the same maximum width found in the input, padding with 0.
    Handles non-integer elements by converting them to 0.
    Returns an empty list if the input is invalid or empty.
    """
    if isinstance(grid_list, np.ndarray):
        # Convert numpy array to list of lists first
        try:
            grid_list = grid_list.tolist()
        except Exception:
            return [] # Cannot convert

    if not isinstance(grid_list, (list, tuple)) or not grid_list:
        return [] # Input must be a non-empty list or tuple

    max_width = 0
    processed_rows = []

    # First pass: Process rows and find max_width
    for i, row in enumerate(grid_list):
        if not isinstance(row, (list, tuple)):
           # If a row is not a list/tuple, treat it as empty for width calculation
           # but create a placeholder list for the padding step.
           processed_rows.append([])
           continue # Skip max_width calculation for invalid row type

        current_row = []
        for x in row:
            try:
                current_row.append(int(x))
            except (ValueError, TypeError):
                current_row.append(0) # Default invalid cell to white (0)
        processed_rows.append(current_row)
        max_width = max(max_width, len(current_row))

    if max_width == 0 and not processed_rows: # Check if input was completely invalid
        return []

    # Second pass: Pad rows
    padded_grid = []
    for row in processed_rows:
        padded_row = row + [0] * (max_width - len(row))
        padded_grid.append(padded_row)

    return padded_grid

def find_separator_row(grid_np):
    """
    Finds the row index containing a horizontal gray line (color 5).
    Expects an integer NumPy array. Returns -1 if not found.
    """
    if grid_np.ndim != 2 or grid_np.dtype.kind not in 'iu': # Check dimension and integer type
         return -1
    rows, cols = grid_np.shape
    for r in range(rows):
        # Ensure comparison works even if cols is 0
        if cols > 0 and np.all(grid_np[r, :] == 5):
            return r
    return -1 # Separator not found

def find_objects(grid_np, ignore_colors=frozenset({0, 5})):
    """
    Finds connected objects (8-way connectivity) of the same color in the grid.
    Ignores specified colors (typically background 0 and separator 5).
    Expects an integer NumPy array.
    Returns a list of objects, where each object is a dict containing:
    'color', 'coords' (set of (r, c) tuples), 'bbox' (min_r, min_c, max_r, max_c),
    'shape' (frozenset of relative coords), 'height', 'width'.
    """
    if grid_np.ndim != 2 or grid_np.dtype.kind not in 'iu':
        return [] # Invalid grid input
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid_np[r, c]
            if visited[r, c] or color in ignore_colors:
                continue

            obj_coords = set()
            q = deque([(r, c)])
            visited[r, c] = True
            min_r, min_c = r, c
            max_r, max_c = r, c

            while q:
                row, col = q.popleft()
                obj_coords.add((row, col))
                min_r = min(min_r, row)
                min_c = min(min_c, col)
                max_r = max(max_r, row)
                max_c = max(max_c, col)

                # Check 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid_np[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

            if obj_coords:
                # Calculate relative shape
                shape = frozenset((rr - min_r, cc - min_c) for rr, cc in obj_coords)
                height = max_r - min_r + 1
                width = max_c - min_c + 1

                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'shape': shape,
                    'height': height,
                    'width': width,
                    'id': len(objects) # Assign a unique ID for tracking
                })
    return objects

def get_relative_shape(obj):
    """ Safely returns the shape from an object dict, or empty frozenset. """
    return obj.get('shape', frozenset())

def get_object_dims(obj):
    """ Safely returns height and width from an object dict, or (0, 0). """
    return obj.get('height', 0), obj.get('width', 0)

def draw_object(output_grid_np, obj, target_start_row, target_start_col):
    """
    Draws an object onto the output grid (NumPy array) at the specified top-left position.
    Uses the object's relative shape and color.
    """
    if not obj or 'coords' not in obj or not obj['coords']:
        return # Do nothing if object is invalid

    out_rows, out_cols = output_grid_np.shape
    min_r, min_c, _, _ = obj['bbox']
    color = obj['color']

    for r, c in obj['coords']:
        # Calculate offset from object's top-left
        dr = r - min_r
        dc = c - min_c
        # Calculate target position in output grid
        out_r = target_start_row + dr
        out_c = target_start_col + dc
        # Check bounds before drawing
        if 0 <= out_r < out_rows and 0 <= out_c < out_cols:
            output_grid_np[out_r, out_c] = color


# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms a 15x15 input grid based on the following rules:
    1.  Finds a horizontal gray separator line (row 5).
    2.  Identifies three 3x3 colored objects above the line (Left, Middle, Right)
        and one blue 3x3 key object below the line.
    3.  Analyzes the key object's shape (Hollow, Plus, Diagonal) and vertical
        position (High if top row < 10, Low otherwise).
    4.  Finds the upper object whose shape matches the key object's shape (Matched Object).
    5.  Selects the Matched Object and the Rightmost upper object for the output.
        (If the Rightmost is the Matched object, selects the Leftmost instead).
    6.  Determines the stacking order of the two selected objects based on Key Type and Key Height:
        - Base Order: Plus key -> Matched object on top; Hollow/Diagonal keys -> Other selected object on top.
        - Modification: If Key Type is Hollow AND Key Height is High, flip the Base Order.
    7.  Determines the vertical starting row for the top object in the 9x15 output grid based on Key Type and Key Height:
        - High Key: Hollow -> Row 3, Diagonal -> Row 0, Plus -> Row 1.
        - Low Key: Hollow -> Row 2. (Other types assumed to follow High rules if they occur).
    8.  Constructs the output grid (9x15) by stacking the selected objects in the
        determined order, starting at the calculated row, and centered horizontally.
    """
    # 0. Initialize and Validate Input
    padded_input_list = pad_grid(input_grid)
    if not padded_input_list:
        # Return default 9x15 white grid if input padding failed
        return [[0] * 15 for _ in range(9)]

    input_np = np.array(padded_input_list, dtype=int)

    # Expect 15x15 input, produce 9x15 output
    expected_input_h, expected_input_w = 15, 15
    output_h, output_w = 9, 15
    default_output = np.zeros((output_h, output_w), dtype=int)

    if input_np.shape != (expected_input_h, expected_input_w):
         # Handle unexpected input dimensions if necessary, here returning default
         return default_output.tolist()

    # 1. Identify Separator
    separator_row = find_separator_row(input_np)
    if separator_row != 5: # Expect separator specifically at row 5
        return default_output.tolist()

    # 2. Identify Objects
    all_objects = find_objects(input_np, ignore_colors=frozenset({0, 5}))

    # Filter objects above and below the separator
    upper_objects_raw = [obj for obj in all_objects if obj['bbox'][0] < separator_row]
    lower_objects = [obj for obj in all_objects if obj['bbox'][0] > separator_row]

    # Validate assumptions: 3 upper, 1 lower (blue)
    if len(upper_objects_raw) != 3 or len(lower_objects) != 1:
        return default_output.tolist()

    key_object = lower_objects[0]
    if key_object['color'] != 1: # Key must be blue
         return default_output.tolist()

    # Sort upper objects by horizontal position (min_c) and assign location names
    upper_objects = sorted(upper_objects_raw, key=lambda obj: obj['bbox'][1])
    if len(upper_objects) == 3:
        upper_objects[0]['location'] = 'Left'
        upper_objects[1]['location'] = 'Middle'
        upper_objects[2]['location'] = 'Right'
    else: # Should not happen based on length check, but safety belt
        return default_output.tolist()

    # 3. Analyze Key Object
    key_shape = get_relative_shape(key_object)
    key_type = SHAPE_TYPE_MAP.get(key_shape, "Unknown")
    if key_type == "Unknown":
        return default_output.tolist() # Cannot proceed if key shape is unrecognized

    key_min_row = key_object['bbox'][0]
    is_key_high = key_min_row < 10 # Definition: High if top row < 10

    # 4. Find Match
    matched_object = None
    for obj in upper_objects:
        if get_relative_shape(obj) == key_shape:
            matched_object = obj
            break # Found the match

    if matched_object is None:
        return default_output.tolist() # Cannot proceed without a match

    # 5. Select Objects for Output
    # Select Matched object and Rightmost object.
    # If Rightmost IS the matched object, select Leftmost instead.
    rightmost_object = upper_objects[2]
    leftmost_object = upper_objects[0]

    if matched_object['id'] == rightmost_object['id']:
        other_selected_object = leftmost_object
    else:
        other_selected_object = rightmost_object

    # We now have 'matched_object' and 'other_selected_object'

    # 6. Determine Stacking Order
    top_object = None
    bottom_object = None

    # Base order: Plus key -> Matched on top; Hollow/Diagonal -> Other on top
    if key_type == "Plus":
        base_top = matched_object
        base_bottom = other_selected_object
    elif key_type == "Hollow" or key_type == "Diagonal":
        base_top = other_selected_object
        base_bottom = matched_object
    else: # Should be unreachable due to earlier key_type check
         return default_output.tolist()

    # Modification: Flip for Hollow + High Key
    if key_type == "Hollow" and is_key_high:
        top_object = base_bottom
        bottom_object = base_top
    else:
        top_object = base_top
        bottom_object = base_bottom

    # 7. Determine Vertical Placement
    output_start_row = -1 # Initialize to invalid value

    # Rules based on Key Type and Key Height
    if is_key_high:
        if key_type == "Hollow": output_start_row = 3
        elif key_type == "Diagonal": output_start_row = 0
        elif key_type == "Plus": output_start_row = 1
    else: # Key is Low
        # Assume only Hollow is observed for Low keys in examples
        if key_type == "Hollow": output_start_row = 2
        # Add rules for other low keys if observed, otherwise they might default to -1
        # Fallback assumption: use High rules if type/height combo not specified
        elif key_type == "Diagonal": output_start_row = 0 # Assuming same as high
        elif key_type == "Plus": output_start_row = 1 # Assuming same as high


    if output_start_row == -1:
        # If placement rule didn't match (e.g., unexpected key type/height combo)
        return default_output.tolist()

    # 8. Construct Output Grid
    output_grid_np = np.zeros((output_h, output_w), dtype=int)

    # All objects are assumed 3x3, calculate centering column
    obj_width = 3 # Assuming all relevant objects are 3 wide
    center_start_col = (output_w - obj_width) // 2 # (15 - 3) // 2 = 6

    # Draw the top object
    top_h, _ = get_object_dims(top_object)
    draw_object(output_grid_np, top_object, output_start_row, center_start_col)

    # Draw the bottom object immediately below the top one
    # Assuming top object height is 3
    bottom_start_row = output_start_row + 3 # top_h should be 3
    draw_object(output_grid_np, bottom_object, bottom_start_row, center_start_col)

    # Return as list of lists
    return output_grid_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 2 0 0 0 3 0 0 0
0 0 1 0 1 0 0 2 0 0 3 3 3 0 0
0 0 1 1 1 0 2 2 2 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 10.370370370370381

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 0 2 0 0 4 4 4 0 0
0 0 0 1 0 0 0 2 0 0 4 4 4 0 0
0 0 1 0 1 0 2 2 2 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 11.851851851851848

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 2 2 2 0 6 6 6 0 0
0 0 1 1 1 0 0 2 0 0 6 0 6 0 0
0 0 0 1 0 0 0 2 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 2 2 2 0 0 7 0 0 0
0 0 0 1 0 0 0 2 0 0 7 0 7 0 0
0 0 0 1 1 0 0 2 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 13.333333333333343
