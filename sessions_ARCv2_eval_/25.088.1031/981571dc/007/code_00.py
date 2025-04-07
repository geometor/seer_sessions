import numpy as np
from collections import deque

"""
Transforms an input grid by performing the following steps:
1.  Initializes an output grid potentially larger than the input, filled with white (0).
2.  Identifies all distinct contiguous non-white objects in the input grid.
3.  For each object, calculates the maximum possible downward shift (delta_r >= 0) such that the space directly below the shifted object's final position is either occupied by a non-white pixel in the *original input grid* or is the bottom edge of the original input grid. Essentially, the object "falls" until it lands on something or the original floor.
4.  Determines the required height of the output grid to accommodate both the original content and all the shifted object copies.
5.  Copies the non-white pixels from the original input grid into the correctly sized output grid.
6.  Copies the pixels of each original object to their calculated shifted positions (original_row + delta_r, original_col) in the output grid.
"""

def _find_objects(grid_np):
    """
    Finds contiguous non-white objects in the grid using BFS.

    Args:
        grid_np (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'pixels' (list of (r, c) tuples).
              Returns empty list if no non-white pixels are found.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS from a non-white, unvisited pixel
            if grid_np[r, c] != 0 and not visited[r, c]:
                color = grid_np[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid_np[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the found object to the list
                if obj_pixels:
                    # Sort pixels for consistency (e.g., by row then column)
                    objects.append({'color': int(color), 'pixels': sorted(obj_pixels)}) 

    # Sort objects primarily by top-most row, then left-most column for deterministic processing order
    objects.sort(key=lambda obj: obj['pixels'][0])
    return objects


def transform(input_grid):
    """
    Applies the gravity transformation: copies objects downwards until they hit 
    an obstacle in the original grid or the original grid's floor.
    Keeps the original objects in place as well. Resizes grid if necessary.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_rows, input_cols = input_np.shape

    # 1. Find all non-white objects
    objects = _find_objects(input_np)

    # If no objects, return the original grid
    if not objects:
        return input_grid

    object_shifts = []
    max_shifted_row = input_rows - 1 # Track the max row index needed for shifted objects

    # 2. For each object, determine its downward shift (delta_r)
    for obj in objects:
        obj_pixels = obj['pixels']
        delta_r = 0
        while True:
            is_stable = False
            current_max_r_for_obj = -1 # Track max row for this object at current delta_r
            
            # Check if the position below the object (at current delta_r) is blocked or is the floor
            for r, c in obj_pixels:
                current_max_r_for_obj = max(current_max_r_for_obj, r + delta_r)
                
                check_r = r + delta_r + 1 # Row below the pixel's potential shifted position
                check_c = c

                # Condition to stop falling:
                # a) Reached or exceeded the original grid's bottom boundary
                # b) The cell directly below in the *original* grid is non-white
                if check_r >= input_rows or \
                   (0 <= check_r < input_rows and 0 <= check_c < input_cols and input_np[check_r, check_c] != 0):
                    is_stable = True
                    break # Found an obstacle or floor below this pixel, object is stable at current delta_r
            
            if is_stable:
                # Found the final resting position (delta_r) for this object
                object_shifts.append({'object': obj, 'delta_r': delta_r})
                # Update the overall maximum row needed based on this object's final position
                max_shifted_row = max(max_shifted_row, current_max_r_for_obj) 
                break # Move to the next object
            else:
                # Object can fall further, increment shift and check again
                delta_r += 1

    # 3. Determine final output grid size
    # Required rows = max(original rows, max row reached by any shifted pixel + 1)
    required_rows = max(input_rows, max_shifted_row + 1)
    
    # 4. Create the output grid, initialized to white (0)
    output_np = np.zeros((required_rows, input_cols), dtype=int)

    # 5. Copy original non-white pixels to the output grid
    # Iterate through original grid and copy non-white cells
    for r in range(input_rows):
        for c in range(input_cols):
            if input_np[r, c] != 0:
                output_np[r, c] = input_np[r, c]

    # 6. Place the shifted copies of objects onto the output grid
    for item in object_shifts:
        obj = item['object']
        delta_r = item['delta_r']
        color = obj['color']
        
        for r, c in obj['pixels']:
            target_r = r + delta_r
            target_c = c
            # Check bounds just in case, though resizing should prevent out-of-bounds
            if 0 <= target_r < required_rows and 0 <= target_c < input_cols:
                 output_np[target_r, target_c] = color # Overwrite if necessary

    # 7. Convert back to list of lists and return
    return output_np.tolist()