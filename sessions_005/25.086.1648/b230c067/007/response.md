```python
"""
Transforms an input grid containing white (0) and azure (8) pixels into an output grid of the same dimensions.

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with white (0).
2.  Identify all distinct connected objects composed of azure (8) pixels in the input grid. Use 8-way connectivity (including diagonals). If no azure objects are found, return the initial white output grid.
3.  Precompute the set of all white (0) pixels that are connected to the grid border (exterior white pixels).
4.  For each identified azure object, determine its properties:
    *   The set of pixel coordinates `(row, col)` belonging to the object.
    *   The bounding box containing the object: `(min_row, min_col, max_row, max_col)`.
    *   Whether the object contains or borders an internal "hole" (a contiguous area of white pixels not connected to the grid exterior). This is checked by seeing if any pixel of the object is adjacent (8-way) to a white pixel that is *not* part of the precomputed exterior white pixels.
5.  Count the total number of azure objects that possess a hole (`hole_count`).
6.  Determine which objects (if any) will be colored red (2) and blue (1) based on `hole_count`:
    *   **If `hole_count` is exactly 1:**
        *   Designate the single object *with* the hole to be colored blue (1).
        *   Among the objects *without* holes, identify the "top-right-most" one. Designate this object to be colored red (2). (The "top-right-most" object is the one with the minimum `min_row`; if there's a tie, it's the one among the tied objects with the maximum `max_col`).
        *   Designate all *other* objects (those without holes that were not chosen to be red) to be colored blue (1).
    *   **If `hole_count` is 0:**
        *   Among *all* azure objects, identify the "top-right-most" one (using the same definition as above). Designate this object to be colored red (2).
        *   Designate all *other* azure objects to be colored blue (1).
    *   **If `hole_count` is greater than 1:**
        *   No objects are designated to be colored red or blue. The output grid remains white.
7.  Populate the output grid: For every pixel `(r, c)` belonging to an object designated red, set `output_grid[r, c]` to 2. For every pixel `(r, c)` belonging to an object designated blue, set `output_grid[r, c]` to 1.
8.  Return the final output grid.
"""

import numpy as np
from collections import deque

def _get_neighbors(r, c, height, width, connectivity=8):
    """ Helper to get valid neighbors for a pixel. """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_components(grid, target_color, connectivity=8):
    """
    Finds all connected components of a specific color in the grid.
    Uses BFS and specified connectivity (4 or 8).
    Returns a list of sets, where each set contains (row, col) tuples for an object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS for a new component
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.add((curr_r, curr_c))

                    for nr, nc in _get_neighbors(curr_r, curr_c, height, width, connectivity):
                        if grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object_pixels:
                     objects.append(current_object_pixels)

    return objects

def get_bounding_box(obj_pixels):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of pixels."""
    if not obj_pixels:
        return None, None, None, None # Return None for each value
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    return min(rows), min(cols), max(rows), max(cols)

def find_exterior_white_pixels(grid):
    """ Finds all white (0) pixels connected to the grid border using BFS. """
    height, width = grid.shape
    exterior_white = set()
    q = deque()
    visited_white = set() # Keep track of visited white pixels to avoid cycles/redundancy

    # Add all border white pixels to the queue and visited set
    for r in range(height):
        for c in [0, width - 1] if width > 0 else []: # Check left/right borders
             if grid[r, c] == 0 and (r,c) not in visited_white:
                 q.append((r, c))
                 visited_white.add((r,c))
                 exterior_white.add((r,c))
                 
    for c in range(width):
        for r in [0, height-1] if height > 0 else []: # Check top/bottom borders
            # Avoid adding corners twice
             if grid[r, c] == 0 and (r,c) not in visited_white:
                 q.append((r, c))
                 visited_white.add((r,c))
                 exterior_white.add((r,c))

    # Perform BFS from border white pixels
    while q:
        curr_r, curr_c = q.popleft()
        
        # Use 8-way connectivity for checking adjacent white pixels
        for nr, nc in _get_neighbors(curr_r, curr_c, height, width, connectivity=8):
            if grid[nr, nc] == 0 and (nr, nc) not in visited_white:
                 visited_white.add((nr, nc))
                 exterior_white.add((nr, nc))
                 q.append((nr, nc))

    return exterior_white

def check_for_hole(obj_pixels, grid, exterior_white_pixels):
    """
    Checks if an object is adjacent to any white pixel not connected to the exterior.
    """
    height, width = grid.shape
    for r, c in obj_pixels:
        # Check 8 neighbors
        for nr, nc in _get_neighbors(r, c, height, width, connectivity=8):
            # If neighbor is white AND it's NOT an exterior white pixel
            if grid[nr, nc] == 0 and (nr, nc) not in exterior_white_pixels:
                return True # Found a hole pixel adjacent to the object
    return False # No adjacent hole pixels found


def transform(input_grid):
    """
    Transforms the input grid based on identifying azure objects, checking for holes,
    and applying coloring rules based on hole count and object position.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Step 1: Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # Step 2: Identify all azure (8) objects using 8-way connectivity
    azure_objects_pixels = find_connected_components(input_grid_np, 8, connectivity=8)

    # If no azure objects found, return the white grid
    if not azure_objects_pixels:
        return output_grid.tolist() 

    # Step 3: Precompute exterior white pixels
    exterior_white = find_exterior_white_pixels(input_grid_np)

    # Step 4: Analyze objects: calculate properties
    objects_data = []
    for obj_pixels in azure_objects_pixels:
        if not obj_pixels: continue # Skip if somehow an empty object was found
        min_r, min_c, max_r, max_c = get_bounding_box(obj_pixels)
        # Check if min_r is None, indicating an empty object set passed checks
        if min_r is None: continue 
        
        has_hole_flag = check_for_hole(obj_pixels, input_grid_np, exterior_white)
        
        objects_data.append({
            "pixels": obj_pixels,
            "min_row": min_r, # Top edge row index
            "max_col": max_c, # Right edge column index
            "has_hole": has_hole_flag
        })

    # Step 5: Count objects with holes
    hole_objects = [obj for obj in objects_data if obj["has_hole"]]
    non_hole_objects = [obj for obj in objects_data if not obj["has_hole"]]
    hole_count = len(hole_objects)

    # Initialize variables to store which objects get which color
    red_object_data = None
    blue_objects_data = []

    # Step 6: Apply coloring logic based on hole count
    if hole_count == 1:
        # Case: Exactly one object has a hole
        # Rule 6.a.i: The object with the hole becomes blue
        blue_objects_data.append(hole_objects[0]) 
        
        # Rule 6.a.ii: Find top-right-most among non-hole objects to become red
        if non_hole_objects:
            # Find the minimum 'min_row' among non-hole objects
            min_row_non_hole = min(obj["min_row"] for obj in non_hole_objects)
            # Filter to get all non-hole objects at that top-most row
            top_non_hole = [obj for obj in non_hole_objects if obj["min_row"] == min_row_non_hole]
            
            # Among those top-most objects, find the one with the maximum 'max_col' (right-most)
            max_col_top_non_hole = max(obj["max_col"] for obj in top_non_hole)
            # Select the first object that matches both criteria
            red_object_data = next((obj for obj in top_non_hole if obj["max_col"] == max_col_top_non_hole), None)

            # Rule 6.a.iii: All other non-hole objects become blue
            blue_objects_data.extend([obj for obj in non_hole_objects if obj != red_object_data])
        # If there were no non-hole objects, red_object_data remains None, and only the hole object is blue

    elif hole_count == 0:
        # Case: No objects have holes
        # Rule 6.b.i: Find top-right-most among *all* objects to become red
        if objects_data: # Check if there are any objects at all
            # Find the minimum 'min_row' among all objects
            min_row_all = min(obj["min_row"] for obj in objects_data)
            # Filter to get all objects at that top-most row
            top_all = [obj for obj in objects_data if obj["min_row"] == min_row_all]
            
            # Among those top-most objects, find the one with the maximum 'max_col' (right-most)
            max_col_top_all = max(obj["max_col"] for obj in top_all)
            # Select the first object matching both criteria
            red_object_data = next((obj for obj in top_all if obj["max_col"] == max_col_top_all), None)

            # Rule 6.b.ii: All other objects become blue
            blue_objects_data.extend([obj for obj in objects_data if obj != red_object_data])
            
    # Step 6.c: If hole_count > 1, red_object_data remains None and blue_objects_data remains empty. 
    # The output grid will remain white as initialized.

    # Step 7: Populate the output grid based on determined colors
    # Color the designated red object (if one was found) with red (2)
    if red_object_data:
        for r, c in red_object_data["pixels"]:
             # Basic boundary check (though coordinates should be valid)
             if 0 <= r < height and 0 <= c < width:
                 output_grid[r, c] = 2 # Red color

    # Color the designated blue objects (if any were found) with blue (1)
    for blue_obj_data in blue_objects_data:
        for r, c in blue_obj_data["pixels"]:
             # Basic boundary check
             if 0 <= r < height and 0 <= c < width:
                 # Check if the pixel is still white (0) before coloring it blue.
                 # This prevents overwriting a red pixel if an object somehow got designated both 
                 # (should not happen with current logic, but adds robustness).
                 if output_grid[r, c] == 0: 
                     output_grid[r, c] = 1 # Blue color

    # Step 8: Return the final output grid as a list of lists
    return output_grid.tolist()
```