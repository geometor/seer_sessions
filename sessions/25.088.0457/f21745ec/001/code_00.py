import numpy as np
from collections import deque

# Define white color constant
WHITE = 0

def find_objects(grid):
    """
    Finds connected components of non-white colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains:
              (color (int), set_of_pixels (set of (r, c) tuples)).
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != WHITE and not visited[r, c]:
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
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_pixels:
                    objects.append((color, obj_pixels))
                    
    return objects

def get_bounding_box(pixels):
    """
    Calculates the bounding box for a set of pixels.

    Args:
        pixels (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if pixels is empty.
    """
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid):
    """
    Transforms the input grid based on object properties.
    
    Rule:
    1. Identify all non-white connected objects.
    2. For each object:
       a. Determine its bounding box.
       b. Check if the object perfectly forms the border of its bounding box AND
          all pixels strictly inside the bounding box are white. Call this a "perfect hollow rectangle".
       c. Check if any non-white pixels exist strictly inside the bounding box.
       d. Calculate the area of the region strictly inside the bounding box.
    3. Apply transformation:
       a. If the object is a perfect hollow rectangle AND its interior area is >= 10:
          Fill the interior white pixels with the object's color.
       b. Else if there are any non-white pixels inside the bounding box:
          Keep the object as is.
       c. Otherwise (not a perfect hollow rectangle >= 10 area, AND no non-white pixels inside):
          Remove the object (set its pixels to white).
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    objects = find_objects(input_grid)

    for color, object_pixels in objects:
        # Find bounding box
        bbox = get_bounding_box(object_pixels)
        if bbox is None:
            continue
        min_r, min_c, max_r, max_c = bbox
        
        # Calculate dimensions and interior area
        obj_height = max_r - min_r + 1
        obj_width = max_c - min_c + 1
        interior_area = max(0, obj_height - 2) * max(0, obj_width - 2)

        # Check properties: perfect hollow rectangle and interior content
        is_hollow_rect = True
        has_only_white_inside = True
        has_non_white_inside = False
        
        # Check if all border pixels of bbox belong to the object
        # and check interior content simultaneously
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                is_border = (r == min_r or r == max_r or c == min_c or c == max_c)
                
                if is_border:
                    if (r, c) not in object_pixels:
                        is_hollow_rect = False
                else: # Inside the bounding box
                    if input_grid[r, c] != WHITE:
                        has_only_white_inside = False
                        has_non_white_inside = True # Found non-white inside
                    if (r, c) in object_pixels: # Object pixel inside border
                        is_hollow_rect = False
                        
        # Final check: ensure all object pixels are on the border
        if is_hollow_rect:
             for r_obj, c_obj in object_pixels:
                 if not (r_obj == min_r or r_obj == max_r or c_obj == min_c or c_obj == max_c):
                     is_hollow_rect = False
                     break # Found an object pixel inside, not hollow

        # Apply transformation rule based on checks
        if is_hollow_rect and has_only_white_inside and interior_area >= 10:
            # Fill the interior
            for r_in in range(min_r + 1, max_r):
                for c_in in range(min_c + 1, max_c):
                     # Ensure we only fill if it was originally white (redundant given has_only_white_inside check, but safe)
                    if input_grid[r_in, c_in] == WHITE:
                       output_grid[r_in, c_in] = color
        elif has_non_white_inside:
            # Keep the object (do nothing, grid was copied)
            pass
        else:
            # Remove the object
            for r_obj, c_obj in object_pixels:
                output_grid[r_obj, c_obj] = WHITE
                
    return output_grid
