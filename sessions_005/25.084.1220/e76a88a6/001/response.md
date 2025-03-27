```python
import numpy as np
from collections import deque

"""
Identify the unique multi-colored (non-gray) object in the input grid as the 'pattern'.
Identify all objects composed solely of gray pixels as 'targets'.
Replace each target object in the output grid with a copy of the pattern object, aligning the top-left corner of the pattern copy with the top-left corner of the target object's bounding box.
The original pattern object and background pixels remain unchanged unless overwritten by a pattern placement.
"""

def find_objects(grid):
    """
    Finds connected components (objects) of non-background (non-zero) pixels in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (set of (r, c) tuples), 'colors' (set of color values),
              'min_row', 'min_col', 'max_row', 'max_col', and 'top_left' ((r, c) tuple).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start BFS to find a new object
                obj_pixels = set()
                obj_colors = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.add((curr_r, curr_c))
                    obj_colors.add(grid[curr_r, curr_c])
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'pixels': obj_pixels,
                    'colors': obj_colors,
                    'min_row': min_r,
                    'min_col': min_c,
                    'max_row': max_r,
                    'max_col': max_c,
                    'top_left': (min_r, min_c)
                })
    return objects

def extract_pattern_data(grid, pattern_obj):
    """
    Extracts the pixel data of the pattern object relative to its top-left corner.

    Args:
        grid (np.ndarray): The input grid.
        pattern_obj (dict): The dictionary representing the pattern object.

    Returns:
        np.ndarray: A grid containing the pattern's pixel data.
        int: The height of the pattern grid.
        int: The width of the pattern grid.
    """
    min_r, min_c = pattern_obj['top_left']
    height = pattern_obj['max_row'] - min_r + 1
    width = pattern_obj['max_col'] - min_c + 1
    
    pattern_grid = np.zeros((height, width), dtype=int)
    
    for r, c in pattern_obj['pixels']:
        relative_r = r - min_r
        relative_c = c - min_c
        pattern_grid[relative_r, relative_c] = grid[r,c]
        
    return pattern_grid, height, width

def transform(input_grid):
    """
    Applies the transformation rule: identifies a pattern object (non-gray)
    and target objects (gray), then replaces targets with the pattern.

    Args:
        input_grid (np.ndarray): The input 2D array representing the grid.

    Returns:
        np.ndarray: The transformed 2D array.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_rows, grid_cols = output_grid.shape

    # 1. & 2. Find all non-white objects
    all_objects = find_objects(input_grid)

    # 3. Identify the pattern object (non-gray) and target objects (gray)
    pattern_object = None
    target_objects = []
    for obj in all_objects:
        if 5 in obj['colors'] and len(obj['colors']) == 1: # Exclusively gray
             target_objects.append(obj)
        elif 5 not in obj['colors'] and obj['colors']: # Contains non-gray colors
            if pattern_object is None: # Found the first (and should be only) pattern
                pattern_object = obj
            else:
                # Error case: Multiple potential patterns found, which contradicts the assumption.
                # For ARC, we usually assume the examples guide us to a single interpretation.
                # We'll proceed with the first one found, but this might need refinement if tasks allow multiple patterns.
                pass 

    # If no pattern object is found, return the original grid
    if pattern_object is None:
        return output_grid

    # Extract the pattern's pixel data relative to its top-left corner
    pattern_data, pattern_h, pattern_w = extract_pattern_data(input_grid, pattern_object)

    # 5. For each target object, replace it with the pattern
    for target in target_objects:
        target_r, target_c = target['top_left']

        # Iterate through the pattern's pixels
        for r_offset in range(pattern_h):
            for c_offset in range(pattern_w):
                # Calculate the coordinates in the output grid
                out_r = target_r + r_offset
                out_c = target_c + c_offset

                # Check if the coordinate is within the grid bounds
                if 0 <= out_r < grid_rows and 0 <= out_c < grid_cols:
                    # Get the color from the pattern data
                    pattern_color = pattern_data[r_offset, c_offset]
                    # Only overwrite if the pattern pixel is not background (0)
                    # This preserves the shape of the pattern if it's not rectangular
                    if pattern_color != 0:
                         output_grid[out_r, out_c] = pattern_color
                    # If the pattern pixel IS background (0), we need to consider
                    # if the original pixel at the target location *within the target object's bounds*
                    # should be cleared. Since we replace the *entire* target object conceptually,
                    # pixels within the pattern's bounding box overlaid on the target location
                    # should become 0 if the corresponding pattern pixel is 0.
                    # However, the prompt implies stamping the non-zero part of the pattern.
                    # Let's stick to only overwriting with non-zero pattern pixels for now.
                    # Re-evaluating train_1 output: it seems the gray pixels under the pattern's zero pixels ARE cleared.
                    # Let's adjust: overwrite with pattern color, even if it's 0, but only within the bounds.
                    elif pattern_color == 0:
                         # Check if the original pixel belonged to the target object being replaced.
                         # This is complex. A simpler approach matching the examples:
                         # Overwrite with the pattern pixel's value regardless, within bounds.
                         # This implicitly clears pixels if the pattern has 0s.
                         output_grid[out_r, out_c] = pattern_color


    # 6. Return the modified grid (original pattern object is already preserved unless overwritten)
    return output_grid
```