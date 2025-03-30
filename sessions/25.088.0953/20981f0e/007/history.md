
Previous Code:
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
2. A blue pixel belonging to another object directly below it.
3. The bottom edge of the grid.

Red pixels remain fixed throughout the process.
Blue objects maintain their shape during the fall.
The process iterates until no blue object can move down in a full pass. Objects are processed effectively from bottom-to-top within each step to ensure stable settling.
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
    An object can move down only if ALL cells immediately below its constituent pixels
    are either background (0) or part of the object itself. If ANY cell below is
    a boundary, red (2), or part of *another* blue object, it cannot move.

    Args:
        grid (np.array): The grid state to check against.
        obj_coords (list[tuple[int, int]]): The coordinates of the object pixels.

    Returns:
        bool: True if the object can move down one step, False otherwise.
    """
    rows, cols = grid.shape
    obj_coords_set = set(obj_coords) # Use set for efficient lookups

    for r, c in obj_coords:
        below_r = r + 1
        below_c = c
        
        # Check 1: Bottom boundary
        if below_r >= rows:
            return False # Object hit the bottom edge

        # Check 2: Obstacle below (that is NOT part of the current object)
        # If the cell below IS part of the current object, it doesn't block movement;
        # we only care about external obstacles.
        if (below_r, below_c) not in obj_coords_set:
            # Check the color of the cell below
            if grid[below_r, below_c] != 0: # 0 is background
                 # It's blocked by red (2) or another blue object (1)
                 return False 
            
    # If we looped through all pixels of the object and found no blocking conditions
    # for any of the cells immediately below them, the object can move.
    return True 

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
    red_color = 2
    background_color = 0

    # Main simulation loop: continues as long as any object moves in an iteration
    while True:
        # Find all current blue objects in the grid at the start of this iteration
        blue_objects = find_connected_components(grid, blue_color)
        
        # Sort objects by their lowest point (max row index) in descending order.
        # This helps ensure that lower objects attempt to move and settle first,
        # providing a stable base for objects above them.
        blue_objects.sort(key=lambda obj: max(r for r, c in obj), reverse=True)

        # Identify which objects can actually move down in this step
        objects_to_move_this_iteration = []
        for obj_coords in blue_objects:
             if can_object_move_down(grid, obj_coords):
                 objects_to_move_this_iteration.append(obj_coords)

        # If no objects can move in this iteration, the simulation is stable.
        if not objects_to_move_this_iteration:
            break # Exit the while loop

        # Perform the moves for all objects identified as movable in this iteration.
        # Strategy: Erase all moving objects first, then redraw them in their new positions.
        # This prevents conflicts where an object moves into a space just vacated
        # by another object *within the same iteration*.
        
        # Erase all moving objects from their current positions
        for obj_coords in objects_to_move_this_iteration:
            for r, c in obj_coords:
                grid[r, c] = background_color
        
        # Redraw all moving objects one step down in their new positions
        for obj_coords in objects_to_move_this_iteration:
            for r, c in obj_coords:
                # The can_object_move_down check ensures r+1 is within bounds
                grid[r + 1, c] = blue_color
            
        # Continue to the next iteration of the while loop

    # Return the final stable grid state as a list of lists
    return grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 0 0 1 1 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 1 1 0 0 0 0 1 0 0 0
0 0 0 0 1 1 0 0 0 0 1 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0
0 0 0 0 1 1 0 0 0 1 1 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 0 1 1 0 0 1 1 1 1 0 0
0 0 2 1 1 0 0 2 0 1 1 0 2 1 0 0 0 2 0
```
Match: False
Pixels Off: 30
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 12.145748987854262

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0 1 1 0
0 0 1 1 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 0 1 0 0
0 0 0 0 1 0 0 0 1 0 0 0 0 1 1 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 1 0 0 0 0 1 1 0
0 0 0 1 1 0 0 0 1 1 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 1 1 0 0 0 1 0 0
0 0 0 1 1 0 0 0 1 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0
0 2 1 1 0 0 2 1 1 0 0 2 0 1 0 0
0 0 1 1 1 0 0 0 1 1 0 0 0 1 0 0
0 0 0 1 1 0 0 0 1 0 0 0 0 1 1 0
```
Match: False
Pixels Off: 38
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 16.964285714285708

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 1 1 0 0 0 0 1 1 0
0 1 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 1 1 0 0 1 1 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 1 0 0
0 0 1 1 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 1 0 0
0 0 1 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 1 1 0
0 0 1 1 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 1 0 0
0 0 0 0 0 0 0 1 1 0
0 1 1 0 0 0 0 1 0 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 1 0 0 1 1 0
2 1 0 1 1 2 0 1 0 0
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 18.82352941176471
