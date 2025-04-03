```python
import numpy as np
from collections import Counter, deque

"""
Transforms the input grid based on the relative positions of unique Red(2) and Green(3) bar objects.
1. Identifies the background color (most frequent).
2. Finds all non-background objects.
3. Specifically locates the 5-pixel Red bar and the 5-pixel Green bar.
4. Identifies all 13-pixel plus-sign shaped objects.
5. Determines if the Red bar is horizontally left or right of the Green bar.
6. Based on this relative position, selects a target plus-sign color and modification mode:
    - Red Left of Green: Target Maroon(9) ('all' mode) if present, else target Green(3) ('topmost' mode) if present.
    - Red Right of Green: Target Magenta(6) ('all' mode) if present, else target Green(3) ('topmost' mode) if present.
7. Creates an output grid by:
    - Copying the input grid.
    - Removing the Red and Green bars (changing their pixels to the background color).
    - Modifying the targeted plus-signs: changing pixels to Gray(5). If mode is 'all', all matching plus-signs are changed. If mode is 'topmost', only the highest one (minimum top row) is changed.
"""

# Imports are already included above

def find_objects(grid, background_color):
    """
    Finds all connected components (objects) of non-background colors in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'pixels' (set of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_pixels:
                    objects.append({'color': color, 'pixels': obj_pixels})
    return objects

def get_object_bounds(obj_pixels):
    """Calculates the bounding box, size, and min/max row/col of an object."""
    if not obj_pixels:
        return None, None, None, None, 0, None, None # min_r, min_c, height, width, size, max_r, max_c
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    size = len(obj_pixels)
    return min_r, min_c, height, width, size, max_r, max_c

def is_plus_sign(obj_pixels):
    """Checks if an object represented by pixels forms a 13-pixel plus sign shape."""
    min_r, min_c, height, width, size, _, _ = get_object_bounds(obj_pixels)
    # Quick check for size and bounding box dimensions
    if size != 13 or height != 5 or width != 5:
        return False
    
    # Verify the exact shape: center + 2 pixels in each cardinal direction
    center_r, center_c = min_r + 2, min_c + 2
    
    expected_pixels = set()
    # Horizontal bar part
    for dc in range(-2, 3):
        expected_pixels.add((center_r, center_c + dc))
    # Vertical bar part (add only vertical pixels not already in horizontal)
    for dr in range(-2, 3):
         if dr != 0: # Avoid adding center twice
             expected_pixels.add((center_r + dr, center_c))
        
    # Check if the generated shape matches the input pixels exactly
    return obj_pixels == expected_pixels

def is_bar(obj_pixels):
    """Checks if an object represented by pixels forms a 5-pixel bar (1x5 or 5x1)."""
    _, _, height, width, size, _, _ = get_object_bounds(obj_pixels)
    if size != 5:
        return False
    # Check for 1x5 or 5x1 dimensions
    if (height == 5 and width == 1) or (height == 1 and width == 5):
        return True
    return False

def get_topmost_object(objects):
    """Finds the object with the minimum top row index from a list of objects."""
    if not objects:
        return None
        
    topmost_obj = None
    min_top_row = float('inf')

    for obj in objects:
        # Use min_r from bounds calculation
        obj_min_r, _, _, _, _, _, _ = get_object_bounds(obj['pixels'])
        if obj_min_r < min_top_row:
            min_top_row = obj_min_r
            topmost_obj = obj
        # Tie-breaking: If rows are equal, implicitly takes the first one found.
        # ARC tasks usually don't rely on ambiguous tie-breaking unless specified.
            
    return topmost_obj

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify and return
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Find background color
    all_pixels = grid.flatten()
    if len(all_pixels) == 0: return output_grid.tolist() # Handle empty grid
    background_color = Counter(all_pixels).most_common(1)[0][0]

    # 2. Find all objects
    objects = find_objects(grid, background_color)

    # 3. Identify bars and plus-signs, collecting relevant info
    red_bar = None
    green_bar = None
    maroon_plus_signs = []
    magenta_plus_signs = []
    green_plus_signs = []
    red_bar_min_c = -1
    green_bar_min_c = -1

    for obj in objects:
        pixels = obj['pixels']
        color = obj['color']
        
        if is_bar(pixels):
            if color == 2: # Red
                red_bar = obj
                _, red_bar_min_c, _, _, _, _, _ = get_object_bounds(pixels)
            elif color == 3: # Green
                green_bar = obj
                _, green_bar_min_c, _, _, _, _, _ = get_object_bounds(pixels)
        elif is_plus_sign(pixels):
            if color == 9: # Maroon
                maroon_plus_signs.append(obj)
            elif color == 6: # Magenta
                magenta_plus_signs.append(obj)
            elif color == 3: # Green (plus sign, not bar)
                green_plus_signs.append(obj)

    # Check if essential control bars were found
    if red_bar is None or green_bar is None:
        # If control bars aren't found, the transformation cannot be determined.
        # Return the original grid as per common ARC interpretation (or handle error).
        # print("Warning: Red or Green bar not found. Returning original grid.")
        return output_grid.tolist() 

    # 4. Determine target color and mode based on bar positions
    target_color = None
    target_mode = None # 'all' or 'topmost'

    if red_bar_min_c < green_bar_min_c:
        # Red is left of Green
        if maroon_plus_signs:
            target_color = 9 # Maroon
            target_mode = 'all'
        elif green_plus_signs:
            target_color = 3 # Green
            target_mode = 'topmost'
    else:
        # Red is right of Green (or same column, unlikely based on examples)
        if magenta_plus_signs:
            target_color = 6 # Magenta
            target_mode = 'all'
        elif green_plus_signs:
            target_color = 3 # Green
            target_mode = 'topmost'

    # 5. Apply Transformations to the output grid
    
    # 5a. Remove Red and Green bars
    for r, c in red_bar['pixels']:
        output_grid[r, c] = background_color
    for r, c in green_bar['pixels']:
        output_grid[r, c] = background_color

    # 5b. Modify target plus-signs
    if target_color is not None and target_mode is not None:
        objects_to_modify = []
        if target_color == 9:
            objects_to_modify = maroon_plus_signs
        elif target_color == 6:
            objects_to_modify = magenta_plus_signs
        elif target_color == 3:
            objects_to_modify = green_plus_signs # List of potential candidates

        if target_mode == 'all':
             for ps_obj in objects_to_modify:
                 for r, c in ps_obj['pixels']:
                     output_grid[r, c] = 5 # Gray
        elif target_mode == 'topmost':
             # Find the single topmost object from the candidates
             topmost_target = get_topmost_object(objects_to_modify)
             if topmost_target:
                 for r, c in topmost_target['pixels']:
                     output_grid[r, c] = 5 # Gray

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()
```