```python
import numpy as np
from collections import deque

"""
Simulate gravity on blue objects (color 1) within a grid.

The grid contains a background (color 0, typically white), blue objects (color 1), and static barriers (color 2, typically red).
Blue objects are defined as contiguous groups of blue pixels using orthogonal connectivity (up, down, left, right).
The transformation involves moving blue objects downwards, one step at a time, until they cannot move further.
An object stops moving if any part of it encounters:
1. A red pixel directly below it.
2. A blue pixel belonging to another object (or an already settled part of the same object in more complex scenarios, although not strictly needed with whole-object movement) directly below it.
3. The bottom edge of the grid.

Red pixels remain fixed throughout the process.
Blue objects maintain their shape during the fall.
The process iterates until no blue object can move down in a full pass.
"""

def find_connected_components(grid, color):
    """
    Finds all connected components of a given color in the grid using BFS.
    Connectivity is orthogonal (up, down, left, right).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[list[tuple[int, int]]]: A list of objects, where each object is represented
                                     by a list of its coordinate tuples (row, col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                component = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component.append((row, col))
                    
                    # Check neighbors (orthogonal)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if component:
                    objects.append(component)
                    
    return objects

def can_object_move_down(grid, obj_coords):
    """
    Checks if an entire object can move down by one step based on the current grid state.

    Args:
        grid (np.array): The grid state to check against.
        obj_coords (list[tuple[int, int]]): The coordinates of the object pixels.

    Returns:
        bool: True if the object can move down one step, False otherwise.
    """
    rows, cols = grid.shape
    object_coords_set = set(obj_coords) # Use set for faster lookups

    for r, c in obj_coords:
        below_r = r + 1
        
        # Check boundary
        if below_r >= rows:
            return False # Reached bottom edge

        # Check cell below
        # If the cell below is part of the *same* object, it's irrelevant for *this* check
        # because the whole object moves together. We only care about obstacles *outside* the object.
        if (below_r, c) not in object_coords_set:
            # Check if the cell below is occupied by something other than the background
            if grid[below_r, c] != 0: 
                 return False # Blocked by red (2) or another blue object (1)
            
    return True # Can move if no part is blocked

def transform(input_grid):
    """
    Applies gravity to blue objects (color 1) in the grid, stopping at red objects (color 2),
    other blue objects, or the grid bottom.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid with blue objects settled.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    blue_color = 1
    background_color = 0

    while True:
        moved_in_iteration = False
        
        # Find all current blue objects based on the grid state at the start of the iteration
        blue_objects = find_connected_components(grid, blue_color)
        
        # Sort objects by their lowest point (max row index) in descending order.
        # This ensures that objects lower down are considered for movement first,
        # creating a stable settling process layer by layer from the bottom up.
        blue_objects.sort(key=lambda obj: max(r for r, c in obj), reverse=True)

        # Determine which objects can move based on the current state, *before* any moves happen this iteration.
        objects_to_move_this_iteration = []
        for obj_coords in blue_objects:
             if can_object_move_down(grid, obj_coords):
                 objects_to_move_this_iteration.append(obj_coords)

        # If no objects can move, the simulation is stable.
        if not objects_to_move_this_iteration:
            break

        # Perform the moves for all objects identified as movable in this iteration.
        # Important: Erase all moving objects first, then redraw them in their new positions.
        # This prevents conflicts where one object moves into the space vacated by another
        # *within the same step*.
        
        # Erase all moving objects
        for obj_coords in objects_to_move_this_iteration:
            moved_in_iteration = True # Mark that at least one object moved
            for r, c in obj_coords:
                grid[r, c] = background_color
        
        # Redraw all moving objects one step down
        for obj_coords in objects_to_move_this_iteration:
            for r, c in obj_coords:
                grid[r + 1, c] = blue_color
            
        # If we didn't actually move anything (e.g., list was empty), break.
        # This condition is already checked by `if not objects_to_move_this_iteration:` above.
        # We keep the `moved_in_iteration` flag mostly for clarity/debugging,
        # but the primary loop control is the list emptiness.

    # Return the final grid state as a list of lists
    return grid.tolist()
```