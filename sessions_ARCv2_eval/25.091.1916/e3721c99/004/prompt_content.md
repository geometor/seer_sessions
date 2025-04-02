
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule Description:

1.  Identify the horizontal blue separator line (color 1) spanning the grid width. This divides the grid into an upper 'key' area and a lower 'work' area.
2.  Identify all distinct non-separator colored objects within the key area. For each 'key' object, store its color, relative pixel pattern (coordinates relative to its bounding box top-left), pixel count, and bounding box dimensions (height, width).
3.  Identify all gray objects (color 5) within the work area. For each 'gray' object, store its original pixel coordinates, relative pixel pattern, and bounding box dimensions.
4.  For each gray object, determine which key object patterns *contain* the gray object's pattern. A key pattern contains the gray pattern if the gray object's shape (relative pixel set) can be translated such that all its pixels coincide with pixels within the key object's relative pattern.
5.  If a gray object's pattern is contained within multiple key patterns, apply a tie-breaking rule:
    a.  First, select the key(s) with the *smallest* bounding box area (height * width).
    b.  If there's still a tie, select the key(s) with the *largest* pixel count among those tied in area.
    c.  (Assumption: This process yields a unique key).
6.  Create an output grid initialized as a copy of the input grid.
7.  For each gray object that successfully matched a unique key, recolor all of its original pixel locations in the output grid with the color of the matched key object.
8.  The separator line and the key objects remain unchanged.
9.  Return the modified output grid.
"""

def find_objects(grid, colors):
    """Finds all connected objects of specified colors using BFS.

    Args:
        grid (np.array): The input grid.
        colors (list or set): A list/set of integer colors to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (a set of (r, c) tuples), and
              'bbox' (a tuple of min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    target_colors = set(colors)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in target_colors and not visited[r, c]:
                obj_color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (Moore neighborhood)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == obj_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                if obj_pixels:
                    objects.append({
                        'color': obj_color,
                        'pixels': obj_pixels,
                        'bbox': (min_r, min_c, max_r, max_c)
                    })
    return objects

def get_relative_pattern(pixels, top_left):
    """Converts absolute pixel coordinates to relative coordinates based on top_left.

    Args:
        pixels (set): Set of (r, c) absolute coordinates.
        top_left (tuple): (min_r, min_c) coordinates of the bounding box top-left.

    Returns:
        frozenset: A frozenset of (dr, dc) relative coordinates.
    """
    min_r, min_c = top_left
    return frozenset((r - min_r, c - min_c) for r, c in pixels)

def get_bbox_dims(bbox):
    """Calculates the height and width from bounding box coordinates."""
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def check_gray_in_key(gray_rel_pattern, key_rel_pattern):
    """Checks if the gray_rel_pattern fits inside (is a subset of) the key_rel_pattern."""
    if not gray_rel_pattern or not key_rel_pattern:
        return False
    if not gray_rel_pattern.issubset(key_rel_pattern): # Quick check if possible at all without offset
         # Check if translation makes it a subset
        max_gray_dr = max(dr for dr, dc in gray_rel_pattern) if gray_rel_pattern else -1
        max_gray_dc = max(dc for dr, dc in gray_rel_pattern) if gray_rel_pattern else -1
        max_key_dr = max(dr for dr, dc in key_rel_pattern) if key_rel_pattern else -1
        max_key_dc = max(dc for dr, dc in key_rel_pattern) if key_rel_pattern else -1

        gray_h = max_gray_dr + 1
        gray_w = max_gray_dc + 1
        key_h = max_key_dr + 1
        key_w = max_key_dc + 1
        
        # If gray is larger than key in any dimension, it can't fit
        if gray_h > key_h or gray_w > key_w:
             return False

        # Iterate through all possible top-left offsets for the gray within the key's relative bbox
        for offset_r in range(key_h - gray_h + 1):
            for offset_c in range(key_w - gray_w + 1):
                fits_at_offset = True
                # Check if every pixel of the shifted gray pattern exists in the key pattern
                for gdr, gdc in gray_rel_pattern:
                    target_rel = (gdr + offset_r, gdc + offset_c)
                    if target_rel not in key_rel_pattern:
                        fits_at_offset = False
                        break # This offset doesn't work
                
                if fits_at_offset:
                    return True # Found a working offset

        return False # No offset worked, and direct subset failed
    else:
        return True # It's a direct subset


def transform(input_grid):
    """
    Applies the transformation rule:
    - Finds key patterns above a blue line.
    - Finds gray objects below the blue line.
    - Recolors gray objects based on the key pattern that contains the gray pattern,
      using tie-breakers (smallest bbox area, then largest pixel count).
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    rows, cols = input_grid_np.shape
    separator_color = 1 # Blue
    gray_color = 5

    # --- 1. Find Separator and Define Areas ---
    separator_row = -1
    for r in range(rows):
        # Check if the entire row is the separator color
        is_separator_line = True
        for c in range(cols):
             if input_grid_np[r,c] != separator_color:
                  is_separator_line = False
                  break
        if is_separator_line:
             # Ensure it's not the only color in the grid if it's just 1xN or Nx1
             if cols > 1 or rows > 1:
                 # Check if there are other colors present anywhere
                 if np.any(input_grid_np != separator_color):
                     separator_row = r
                     break
    
    # Handle case where separator isn't found (use heuristic if needed, but rely on examples for now)
    if separator_row == -1:
        # This case shouldn't happen based on the provided examples.
        # If it did, we might assume no keys or default behavior.
        print("Warning: Separator line not found.")
        return input_grid # Return original if structure is unclear

    key_area_max_row = separator_row # Rows 0 to separator_row - 1
    work_area_min_row = separator_row + 1 # Rows separator_row + 1 to end

    # --- 2. Identify Key Objects ---
    all_objects = find_objects(input_grid_np, list(range(10))) # Find all objects first
    key_objects_info = []
    
    for obj in all_objects:
        min_r, min_c, max_r, max_c = obj['bbox']
        # Object must be entirely above the separator and not be the separator color or gray
        if max_r < key_area_max_row and obj['color'] != separator_color and obj['color'] != gray_color:
            rel_pattern = get_relative_pattern(obj['pixels'], (min_r, min_c))
            height, width = get_bbox_dims(obj['bbox'])
            key_objects_info.append({
                'color': obj['color'],
                'pattern': rel_pattern,
                'pixel_count': len(obj['pixels']),
                'bbox_dims': (height, width),
                'bbox_area': height * width
            })

    # --- 3. Identify Gray Objects ---
    gray_objects = []
    for obj in all_objects:
        min_r, min_c, _, _ = obj['bbox']
        # Object must start at or below the work area start row and be gray
        if min_r >= work_area_min_row and obj['color'] == gray_color:
            rel_pattern = get_relative_pattern(obj['pixels'], (min_r, min_c))
            gray_objects.append({
                 'pixels': obj['pixels'], # Keep original pixels for recoloring
                 'pattern': rel_pattern
            })

    # --- 4. Process Gray Objects: Matching and Tie-breaking ---
    for gray_obj in gray_objects:
        gray_rel_pattern = gray_obj['pattern']
        matching_keys = []

        # Find all keys that contain the gray pattern
        for key_info in key_objects_info:
            if check_gray_in_key(gray_rel_pattern, key_info['pattern']):
                matching_keys.append(key_info)

        if not matching_keys:
            continue # No key contains this gray object pattern

        # Apply tie-breaker 1: Smallest BBox Area
        min_area = min(k['bbox_area'] for k in matching_keys)
        keys_min_area = [k for k in matching_keys if k['bbox_area'] == min_area]

        best_key = None
        if len(keys_min_area) == 1:
            best_key = keys_min_area[0]
        elif len(keys_min_area) > 1:
            # Apply tie-breaker 2: Largest Pixel Count among those with min area
            max_pixels = max(k['pixel_count'] for k in keys_min_area)
            keys_max_pixels = [k for k in keys_min_area if k['pixel_count'] == max_pixels]
            # Assuming this results in a unique key based on problem constraints
            if len(keys_max_pixels) == 1:
                 best_key = keys_max_pixels[0]
            # else: handle unexpected multiple best keys? Print warning or pick first.
            # For now, assume unique or pick first if still tied (unlikely based on ARC)
            elif keys_max_pixels:
                 best_key = keys_max_pixels[0] # Pick the first one if tie persists

        # --- 5. Recolor ---
        if best_key:
            target_color = best_key['color']
            for r, c in gray_obj['pixels']:
                if 0 <= r < rows and 0 <= c < cols: # Bounds check
                    output_grid[r, c] = target_color

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 0 3 0 1 0 1 0 1 0 2 0 2 0 2 0 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 0 5 5 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 5 0 0 0 0 0 5 5 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 5 5 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 5 5 5 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 5 5 5 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 0 0 0 5 5 5 5 0 0 5 0 0
0 0 0 0 0 0 5 5 5 5 0 0 5 5 5 5 5 5 0 0 0 5 5 0 5 5 5 5 0 0
0 0 0 0 0 5 5 5 0 5 0 0 5 0 5 5 5 0 0 0 0 5 5 0 0 5 5 5 0 0
0 0 0 5 5 5 5 5 0 5 0 0 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0
0 0 5 5 5 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 0 5 5 5 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 0 3 0 1 0 1 0 1 0 2 0 2 0 2 0 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 3 3 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 3 3 0 4 4 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 4 4 0 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 1 1 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 1 1 1 1 0 0
0 0 0 3 3 3 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 1 1 1 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 2 0 2 0 0 0 0 1 1 1 1 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 1 1 0 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 2 2 2 0 0 0 0 1 1 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 0 3 0 1 0 1 0 1 0 2 0 2 0 2 0 2 0 0 0 0 0 0 0 0
0 4 4 4 0 3 3 3 0 1 1 1 1 1 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 5 5 5 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 0 0 0 5 5 5 5 0 0 5 0 0
0 0 0 0 0 0 5 5 5 5 0 0 5 5 5 5 5 5 0 0 0 5 5 0 5 5 5 5 0 0
0 0 0 0 0 5 5 5 0 5 0 0 5 0 5 5 5 0 0 0 0 5 5 0 0 5 5 5 0 0
0 0 0 5 5 5 5 5 0 5 0 0 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0
0 0 5 5 5 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 202
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 89.77777777777777

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 0 3 0 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 5 5 5 0 0 5 5 5 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 5 5 5 5 5 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 5 5 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 5 0 0 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0
0 0 0 0 5 0 0 5 5 0 0 0 5 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 0 0 5 0 0 0 5 5 5 5 5 5 5 0 0 5 5 5 5 0 0 0 0 0 0
0 0 0 5 5 0 5 5 0 0 0 5 0 5 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 5 0 5 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 0 3 0 1 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 3 3 3 0 0 3 3 3 0 0
0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 3 3 3 3 0
0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 3 3 3 3 0
0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 3 3 0
0 0 2 2 2 2 2 2 2 0 0 0 2 2 2 2 0 0 0 0 3 3 3 3 3 3 3 3 0 0
0 2 2 2 2 2 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 3 3 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 3 0 0 3 3 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 0 0 0 0 0 0
0 0 0 3 3 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 0 3 0 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 1 0 0 0 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 0 0 0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 5 5 5 0 0 5 5 5 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 0 0 0 0 5 5 5 5 5 5 5 5 0 0
0 5 5 5 5 5 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 5 5 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0 0 0 5 0 0 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0
0 0 0 0 5 0 0 5 5 0 0 0 5 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 0 0 5 0 0 0 5 5 5 5 5 5 5 0 0 5 5 5 5 0 0 0 0 0 0
0 0 0 5 5 0 5 5 0 0 0 5 0 5 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 5 0 5 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 246
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 109.33333333333331
