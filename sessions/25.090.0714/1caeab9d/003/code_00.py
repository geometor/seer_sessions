import numpy as np
from collections import deque
import math

"""
The transformation identifies all distinct contiguous objects (groups of connected pixels of the same non-white color) in the input grid.
It then determines if these objects are vertically separated or if their vertical extents overlap or touch.
Based on this separation status, a target starting row ('target_start_row') is calculated:
- If objects are vertically separated (no object's vertical range [min_row, max_row] overlaps or touches another's): 'target_start_row' is the maximum of the minimum row indices across all objects.
- If objects overlap or touch vertically: 'target_start_row' is the maximum row index of the specific object that has the overall minimum starting row index among all objects.
An output grid of the same dimensions as the input is created, initialized with the background color (white, 0).
Each non-white pixel from the input grid is then mapped to the output grid. For a pixel at (r, c) belonging to an object whose topmost row is 'obj_min_r', its new row ('new_r') is calculated as 'target_start_row + (r - obj_min_r)'. The column ('new_c') remains the same as the original column 'c'. The pixel at (new_r, new_c) in the output grid is set to the color of the original pixel, provided it's within the grid bounds. This process vertically aligns all objects based on the calculated target row, preserving their internal structure and relative horizontal positions.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents an object
              and contains (color, set_of_coordinates). Returns an empty list
              if no non-white objects are found.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # If not background (0) and not visited yet, start BFS
            if color != 0 and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if neighbor has the same color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_coords: # Ensure we found coordinates for the object
                    objects.append((color, obj_coords))
                
    return objects

def get_object_extents(object_coords):
    """
    Calculates the minimum and maximum row index for a set of coordinates.

    Args:
        object_coords (set): A set of (row, col) tuples for an object.

    Returns:
        tuple: (min_row, max_row). Returns (inf, -inf) if the set is empty.
    """
    if not object_coords:
        return float('inf'), float('-inf')
    min_r = min(r for r, c in object_coords)
    max_r = max(r for r, c in object_coords)
    return min_r, max_r

def check_vertical_separation(objects_with_extents):
    """
    Checks if any objects overlap or touch vertically based on their row extents.

    Args:
        objects_with_extents (list): List of tuples (color, coords, min_r, max_r).

    Returns:
        bool: True if all objects are vertically separated, False otherwise.
    """
    if len(objects_with_extents) <= 1:
        return True # 0 or 1 object is considered separated

    # Sort objects by min_r primarily, then max_r for consistency
    sorted_objects = sorted(objects_with_extents, key=lambda x: (x[2], x[3]))

    for i in range(len(sorted_objects) - 1):
        obj1_min_r, obj1_max_r = sorted_objects[i][2], sorted_objects[i][3]
        # Check against all subsequent objects
        for j in range(i + 1, len(sorted_objects)):
             obj2_min_r, obj2_max_r = sorted_objects[j][2], sorted_objects[j][3]
             # Check for overlap or touching: max1 >= min2 means they touch or overlap
             if obj1_max_r >= obj2_min_r:
                 return False # Found overlap/touching

    return True # No overlaps found

def transform(input_grid):
    """
    Transforms the input grid based on the vertical alignment rule determined
    by object separation.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with background color 0

    # 1. Find all non-white objects
    objects = find_objects(input_grid)

    # Handle edge case: no objects found
    if not objects:
        return output_grid

    # 2. Calculate vertical extents for each object
    objects_with_extents = []
    all_non_white_pixels = [] # Also collect all pixels for easier iteration later
    pixel_to_obj_min_row = {} # Map pixel coord to its object's min_r

    min_overall_start_row = float('inf')
    object_with_min_start_row = None

    for color, coords in objects:
        if not coords: continue # Skip if an object somehow has no coordinates
        min_r, max_r = get_object_extents(coords)
        objects_with_extents.append((color, coords, min_r, max_r))
        
        # Track the object with the overall minimum starting row
        if min_r < min_overall_start_row:
            min_overall_start_row = min_r
            object_with_min_start_row = (color, coords, min_r, max_r)
        
        # Populate pixel map and list
        for r, c in coords:
            all_non_white_pixels.append(((r, c), color))
            pixel_to_obj_min_row[(r, c)] = min_r
            
    # Handle edge case: no valid objects with extents found (shouldn't happen if find_objects works)
    if not objects_with_extents:
         return output_grid

    # 3. Determine vertical separation
    are_separated = check_vertical_separation(objects_with_extents)

    # 4. Calculate target_start_row based on separation
    if are_separated:
        # Target row is the max of all minimum starting rows
        target_start_row = max(obj[2] for obj in objects_with_extents)
    else:
        # Target row is the max row of the object with the overall minimum start row
        if object_with_min_start_row:
             target_start_row = object_with_min_start_row[3] # max_r of that object
        else:
             # Fallback (should not be needed if objects exist)
             target_start_row = min_overall_start_row


    # 5. Create output grid by mapping pixels
    for (r, c), color in all_non_white_pixels:
        # Get the minimum row for the object this pixel belongs to
        # Use get() with a default just in case, although map should be complete
        obj_min_r = pixel_to_obj_min_row.get((r, c)) 
        
        if obj_min_r is not None: # Check if pixel was found in map
            # Calculate vertical offset within the object
            offset = r - obj_min_r
            
            # Calculate new position
            new_r = target_start_row + offset
            new_c = c
            
            # Place pixel in output grid if within bounds
            if 0 <= new_r < height and 0 <= new_c < width:
                output_grid[new_r, new_c] = color
        # else: # Should not happen if find_objects and mapping work correctly
        #    print(f"Warning: Pixel {(r,c)} not found in object map.")

    return output_grid