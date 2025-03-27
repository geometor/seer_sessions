import numpy as np
from collections import Counter

"""
Identifies sequences of objects separated by gray horizontal lines in the input grid.
Each section between separators (or grid boundaries) contains one instance of an object.
The transformation analyzes how a specific property of the object (either its width or its horizontal starting position) changes across these sections.
It assumes the property follows an arithmetic progression.
The function predicts the next object in the sequence based on this progression.
The output is a 3-row grid containing only the predicted next object, placed on the middle row (row index 1), against a white background.
"""

def find_separator_rows(grid):
    """Finds rows that consist entirely of the separator color (5)."""
    separator_rows = []
    separator_color = 5
    for r_idx, row in enumerate(grid):
        if all(pixel == separator_color for pixel in row):
            separator_rows.append(r_idx)
    return separator_rows

def find_object_in_frame(frame_grid):
    """
    Finds the first contiguous non-background (0) and non-separator (5) object in a frame.
    Returns its properties: pattern (relative coordinates and colors),
    absolute position (top-left corner in original grid coordinates), size,
    and the raw pixel coordinates.
    """
    ignored_colors = {0, 5}
    object_pixels = [] # List of (r, c, color) tuples
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    
    rows, cols = frame_grid.shape

    # Find all non-ignored pixels and bounding box
    found_pixels_coords = set()
    for r in range(rows):
        for c in range(cols):
            color = frame_grid[r, c]
            if color not in ignored_colors:
                 found_pixels_coords.add((r,c))

    # Simple flood fill / connected component find from the first found pixel
    if not found_pixels_coords:
        return None

    q = [min(found_pixels_coords)] # Start BFS from top-leftmost non-ignored pixel
    visited = set()
    
    while q:
        r, c = q.pop(0)
        if (r,c) in visited or not (0 <= r < rows and 0 <= c < cols):
            continue
        
        color = frame_grid[r,c]
        if color not in ignored_colors:
            visited.add((r,c))
            object_pixels.append({'r': r, 'c': c, 'color': color})
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)
            
            # Add neighbors (4-connectivity)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) not in visited and (nr, nc) in found_pixels_coords:
                     q.append((nr, nc))


    if not object_pixels:
        return None

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Create relative pattern
    pattern = []
    for p in object_pixels:
        pattern.append({
            'r': p['r'] - min_r,
            'c': p['c'] - min_c,
            'color': p['color']
        })
        
    # Sort object pixels for consistent comparison if needed later
    object_pixels.sort(key=lambda p: (p['r'], p['c']))
    pattern.sort(key=lambda p: (p['r'], p['c']))


    return {
        'pattern': pattern, # Relative coordinates and colors
        'position': (min_r, min_c), # Top-left corner within the frame
        'size': (height, width),
        'pixels': object_pixels # Coordinates relative to frame
    }


def transform(input_grid):
    """
    Transforms the input grid based on sequence extrapolation.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    output_height = 3
    
    # --- 1. Identify Frames ---
    separator_rows = find_separator_rows(grid)
    
    frame_boundaries = []
    last_sep = -1
    for sep_r in separator_rows:
        frame_boundaries.append((last_sep + 1, sep_r))
        last_sep = sep_r
    frame_boundaries.append((last_sep + 1, height)) # Add last frame

    # --- 2. Extract Objects and Properties from each Frame ---
    objects_in_sequence = []
    for start_row, end_row in frame_boundaries:
        if start_row >= end_row: # Skip empty frames if separators are adjacent
             continue
        frame = grid[start_row:end_row, :]
        # We need the original row offset for absolute positioning later if needed
        obj_info = find_object_in_frame(frame)
        if obj_info:
            # Adjust position to be relative to the original grid
            obj_info['abs_position'] = (obj_info['position'][0] + start_row, obj_info['position'][1])
            objects_in_sequence.append(obj_info)

    if len(objects_in_sequence) < 2:
        # Cannot determine a sequence with less than 2 objects
        # Return a default empty grid or handle as an error
        return [[0]*width for _ in range(output_height)] 

    # --- 3. Analyze Sequence ---
    first_obj = objects_in_sequence[0]
    last_obj = objects_in_sequence[-1]
    
    # Check if pattern remains constant (structurally)
    # Note: Simple check - assumes pattern list is sorted consistently
    patterns_match = all(o['pattern'] == first_obj['pattern'] for o in objects_in_sequence[1:])
    
    widths = [obj['size'][1] for obj in objects_in_sequence]
    start_cols = [obj['abs_position'][1] for obj in objects_in_sequence] # Use absolute col

    delta_widths = [widths[i] - widths[i-1] for i in range(1, len(widths))]
    delta_cols = [start_cols[i] - start_cols[i-1] for i in range(1, len(start_cols))]

    is_width_sequence = len(set(delta_widths)) == 1 and delta_widths[0] != 0
    is_col_sequence = len(set(delta_cols)) == 1 and delta_cols[0] != 0 and patterns_match # Position change requires same pattern

    next_width = -1
    next_col = -1
    prediction_type = None

    if is_width_sequence and not is_col_sequence:
        # Sequence based on width change (like train_1)
        diff = delta_widths[0]
        next_width = last_obj['size'][1] + diff
        next_col = last_obj['abs_position'][1] # Column usually stays the same
        prediction_type = 'width'
        
        # Check if it's a simple horizontal line
        if not (last_obj['size'][0] == 1 and len(set(p['color'] for p in last_obj['pattern'])) == 1) :
             # This logic currently only handles simple horizontal line width extension
             print("Warning: Width sequence detected, but object is not a simple horizontal line. Prediction might be incorrect.")
             # Fallback or error? For now, proceed assuming line.

    elif is_col_sequence and not is_width_sequence:
        # Sequence based on column change (like train_2)
        diff = delta_cols[0]
        next_col = last_obj['abs_position'][1] + diff
        next_width = last_obj['size'][1] # Width stays the same
        prediction_type = 'position'
    
    elif is_width_sequence and is_col_sequence:
         # Ambiguous or complex sequence - requires more rules.
         # For now, prioritize position if pattern matched, else width? Let's default to position for now.
         print("Warning: Both width and position seem to change arithmetically. Prioritizing position change.")
         diff = delta_cols[0]
         next_col = last_obj['abs_position'][1] + diff
         next_width = last_obj['size'][1] # Width stays the same
         prediction_type = 'position'
         
    else:
        # No clear arithmetic sequence found in width or position
         print("Warning: No arithmetic sequence detected.")
         return [[0]*width for _ in range(output_height)] # Return empty grid

    # --- 4. Construct Next Object and Render Output ---
    output_grid = np.zeros((output_height, width), dtype=int)
    output_row = 1 # Place on the middle row

    if prediction_type == 'width':
        # Reconstruct object based on next_width, assuming horizontal line
        if next_width > 0 and 0 <= next_col < width:
             obj_color = last_obj['pattern'][0]['color'] # Assumes line, get color from first pixel
             for c_offset in range(next_width):
                 if 0 <= next_col + c_offset < width:
                     output_grid[output_row, next_col + c_offset] = obj_color
                     
    elif prediction_type == 'position':
         # Use the last object's pattern and place it at next_col
         pattern_to_draw = last_obj['pattern']
         obj_height = last_obj['size'][0] 
         
         # Check if object fits vertically (should always fit if height is 1 for row 1)
         if output_row + obj_height <= output_height:
             for p in pattern_to_draw:
                 place_r = output_row + p['r']
                 place_c = next_col + p['c']
                 # Check bounds
                 if 0 <= place_c < width:
                     output_grid[place_r, place_c] = p['color']

    return output_grid.tolist()
