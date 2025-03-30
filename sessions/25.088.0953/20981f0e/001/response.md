```python
import numpy as np
from collections import deque

"""
Simulate gravity on blue objects within a grid.

The grid contains white (0) background, blue (1) objects, and red (2) static barriers.
Blue objects are defined as contiguous groups of blue pixels (including diagonals, based on the examples, although typically connectivity is orthogonal - let's assume orthogonal for now and adjust if needed. A check on examples reveals it's orthogonal connectivity).
The transformation involves moving blue objects downwards until they encounter:
1. A red pixel directly below any part of the object.
2. Another blue pixel directly below any part of the object (which belongs to a different object or has already settled).
3. The bottom edge of the grid.

Red pixels remain fixed.
Blue objects maintain their shape during the fall.
The process repeats until no blue object can move further down.
"""

def find_connected_components(grid, color):
    """
    Finds all connected components of a given color in the grid using BFS.
    Connectivity is orthogonal (up, down, left, right).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS for a new component
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
    Checks if an entire object can move down by one step.
    """
    rows, cols = grid.shape
    
    for r, c in obj_coords:
        below_r = r + 1
        # Check boundary
        if below_r >= rows:
            return False # Reached bottom
        # Check cell below
        # If the cell below is part of the *same* object, it's fine (internal).
        # If it's outside the object and not white (0), it's blocked.
        if (below_r, c) not in obj_coords and grid[below_r, c] != 0:
             return False # Blocked by red or another blue object
            
    return True # Can move

def transform(input_grid):
    """
    Applies gravity to blue objects (color 1) in the grid, stopping at red objects (color 2) 
    or the grid bottom.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    blue_color = 1
    background_color = 0

    while True:
        moved_in_iteration = False
        
        # Find all current blue objects
        blue_objects = find_connected_components(grid, blue_color)
        
        # Sort objects by their lowest point (max row index) in descending order.
        # This helps ensure lower objects settle before objects above them try to move.
        blue_objects.sort(key=lambda obj: max(r for r, c in obj), reverse=True)

        # Create a temporary grid or manage updates carefully to avoid conflicts
        # where one object moves into the space just vacated by another in the same step.
        # A simple way is to process moves object by object.
        
        current_grid_state = grid.copy() # Use a snapshot for checks within this iteration

        for obj_coords in blue_objects:
             # Check using the state *before* any moves in this iteration
             # to decide if the object *should* move.
             # However, the actual move needs to be checked against the *updated* grid state
             # to handle cases where an object settles above another one that just moved.
             # Let's rethink: The simplest stable approach is one move per object per iteration.
             
             # Check if this object *can* move based on the current grid state
            if can_object_move_down(grid, obj_coords):
                moved_in_iteration = True
                
                # Erase object from current position
                for r, c in obj_coords:
                    grid[r, c] = background_color
                    
                # Draw object in new position (one step down)
                for r, c in obj_coords:
                    grid[r + 1, c] = blue_color
                    
        # If no object moved in this entire pass, the grid is stable
        if not moved_in_iteration:
            break
            
    # Return the final grid state, converted back to list of lists if necessary
    return grid.tolist()
```