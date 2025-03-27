"""
Identify all distinct connected components (objects) of non-white (color > 0) pixels using 4-way adjacency.
Find the minimum non-white color index (c_min) present in the grid.
Identify all objects containing c_min. Let this set be O_min.

Case 1: If O_min contains exactly one object (obj):
    - If obj contains multiple different colors: Output the subgrid corresponding to the bounding box of obj.
    - If obj contains only one color (c_min): Output a single vertical column (width 1) with height equal to the number of pixels in obj, filled with c_min.

Case 2: If O_min contains more than one object:
    - Find the unique object among *all* objects in the grid that is a "solid square" (monochromatic, square bounding box, no background pixels within the bounding box).
    - Output the subgrid corresponding to the bounding box of this solid square object.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Finds all connected components (objects) of non-background pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'pixels': set of (row, col) tuples for the object's pixels.
              'colors': set of colors present in the object.
              'bbox': tuple (min_row, min_col, max_row, max_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
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
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    obj_colors.add(grid[row, col])
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-way adjacency)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'pixels': obj_pixels,
                    'colors': obj_colors,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
                
    return objects

def get_bounding_box(pixels):
    """Calculates the bounding box for a set of pixels."""
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return (min_r, min_c, max_r, max_c)

def crop_grid(grid, bbox):
    """Extracts a subgrid based on a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    return grid[min_r:max_r+1, min_c:max_c+1]

def is_solid_square(obj, grid):
    """Checks if an object is a solid square."""
    if len(obj['colors']) != 1:
        return False # Must be monochromatic

    color = list(obj['colors'])[0]
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    if height != width:
        return False # Bounding box must be square

    # Check if all pixels within the bounding box match the object's color
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r, c] != color:
                return False # Found background or different color within bbox
            # We also implicitly check if all pixels in the bbox are part of the object
            # because find_objects ensures connectivity. If a non-object pixel
            # existed inside, it would either be 0 (checked above) or a different
            # object's color (also checked above).
            
    # An alternative check: ensure the number of pixels matches the area of the bbox
    if len(obj['pixels']) != height * width:
         return False # Should not happen with the check above, but good validation

    return True

def transform(input_grid):
    """
    Transforms the input grid based on the identified rules.
    """
    input_grid = np.array(input_grid)
    
    # 1. Identify all objects
    all_objects = find_objects(input_grid)
    if not all_objects:
        return np.array([[]]) # Handle empty input or input with only background

    # 2. Find the minimum non-white color (c_min)
    non_white_pixels = input_grid[input_grid != 0]
    if non_white_pixels.size == 0:
         return np.array([[]]) # No non-white pixels found
    c_min = np.min(non_white_pixels)

    # 3. Identify objects containing c_min (O_min)
    O_min = [obj for obj in all_objects if c_min in obj['colors']]

    # 4. Apply rules based on the number of objects in O_min
    if len(O_min) == 1:
        # Case 1: Exactly one object contains c_min
        obj = O_min[0]
        
        if len(obj['colors']) > 1:
            # Case 1.a: Multi-colored object -> Crop bounding box
            output_grid = crop_grid(input_grid, obj['bbox'])
        else:
            # Case 1.b: Monochromatic object -> Vertical column
            num_pixels = len(obj['pixels'])
            output_grid = np.full((num_pixels, 1), c_min, dtype=input_grid.dtype)
            
    elif len(O_min) > 1:
        # Case 2: More than one object contains c_min -> Find unique solid square
        solid_squares = [obj for obj in all_objects if is_solid_square(obj, input_grid)]
        
        if len(solid_squares) == 1:
            obj_sq = solid_squares[0]
            output_grid = crop_grid(input_grid, obj_sq['bbox'])
        else:
            # This case shouldn't happen based on examples, but handle defensively
            # Perhaps return the largest solid square, or the first one found?
            # Or maybe default to the first object in O_min's bbox?
            # Based on example 1, there is expected to be exactly one solid square.
            # If not, we might have misinterpreted the rule or the examples.
            # Let's raise an error for now or return empty if ambiguity is high.
            # Returning empty seems safer for ARC tasks.
            # print(f"Warning: Expected 1 solid square, found {len(solid_squares)}. Input grid:\n{input_grid}")
            if len(solid_squares) > 1:
                 # Let's try returning the solid square with the highest color index as a tie-breaker?
                 # Or the one appearing first (top-left corner)?
                 # Let's stick to the assumption of uniqueness for now.
                 # If uniqueness fails, return the first found as a guess.
                 obj_sq = solid_squares[0]
                 output_grid = crop_grid(input_grid, obj_sq['bbox'])
            else: # len(solid_squares) == 0
                 # print(f"Warning: Expected 1 solid square, found 0. Input grid:\n{input_grid}")
                 output_grid = np.array([[]]) # Return empty grid if no solid square found
                 
    else: # len(O_min) == 0
        # This case means c_min was found, but no object contained it, which is impossible
        # by definition if c_min came from the grid's pixels.
        # This implies an error or edge case not covered (e.g., c_min calculation failed).
        # Return empty grid.
        output_grid = np.array([[]])

    return output_grid.tolist() # Convert back to list of lists for ARC standard