import numpy as np
from collections import deque

"""
Identify all distinct contiguous non-white objects in the input grid. 
Find the object with the minimum color value. 
Shift this selected object one column to the left. 
The original position of the shifted object becomes white (background color 0). 
The new position takes the color of the shifted object, overwriting any previous content. 
All other objects remain unchanged.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'coords' (set of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({'color': color, 'coords': obj_coords})
    return objects

def transform(input_grid):
    """
    Identifies the object with the minimum color value in the input grid
    and shifts it one column to the left. Other objects remain stationary.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # Find all non-background objects
    objects = find_objects(grid_np)

    # If no objects are found, return the original grid
    if not objects:
        return input_grid

    # Find the minimum color value among the objects
    min_color = min(obj['color'] for obj in objects)

    # Find the object(s) with the minimum color
    # In case of ties, the current find_objects implementation will return them
    # in scan order. We'll arbitrarily pick the first one found.
    target_object = None
    for obj in objects:
        if obj['color'] == min_color:
            target_object = obj
            break # Select the first object found with the minimum color

    # If for some reason no target object was selected (shouldn't happen if objects exist)
    if target_object is None:
        return input_grid

    # Initialize output_grid as a copy of the input grid
    output_grid = grid_np.copy()

    # Step 1: Erase the original position of the target object
    for r, c in target_object['coords']:
        output_grid[r, c] = 0 # Set to background color (white)

    # Step 2: Draw the target object at the new, shifted position
    target_color = target_object['color']
    for r, c in target_object['coords']:
        new_c = c - 1
        # Check if the new position is within the grid boundaries
        if new_c >= 0:
            output_grid[r, new_c] = target_color

    # Convert the result back to a list of lists
    return output_grid.tolist()