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
                                     by a list of its coordinate tuples (row, col). Returns
                                     an empty list if no objects of the specified color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                component = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    component.append((row, col))

                    # Check neighbors (orthogonal: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Add the found component (object) to the list if it's not empty
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
    # Use a set for efficient checking if a coordinate belongs to the current object
    obj_coords_set = set(obj_coords)

    # Iterate through each pixel coordinate (r, c) of the object
    for r, c in obj_coords:
        below_r = r + 1
        below_c = c

        # Check 1: Bottom grid boundary
        # If moving any pixel down would go past the last row, the object cannot move.
        if below_r >= rows:
            return False # Object hit the bottom edge

        # Check 2: Obstacle below (that is NOT part of the current object)
        # If the cell below the current pixel IS part of the object itself, it doesn't block movement.
        # We only care about external obstacles (background, red, other blue objects).
        if (below_r, below_c) not in obj_coords_set:
            # Check the color of the cell directly below the current pixel
            # If it's not background (0), it's an obstacle (red=2 or another blue object=1)
            if grid[below_r, below_c] != 0: # 0 is background color
                 return False # Blocked by red or another blue object

    # If we looped through all pixels of the object and found no blocking conditions
    # for any of the cells immediately below them (considering only external obstacles or boundaries),
    # then the entire object can move down.
    return True

def transform(input_grid):
    """
    Applies gravity to blue objects (color 1) in the grid, making them fall downwards
    until they hit red barriers (color 2), other settled blue objects, or the grid bottom.
    Objects fall one step at a time, and the process repeats until no object can move further.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid with blue objects settled.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    blue_color = 1
    background_color = 0

    # Main simulation loop: continues as long as any object successfully moves in a pass
    while True:
        moved_this_pass = False # Flag to track if any movement occurred in the current pass

        # Find all distinct blue objects based on the current grid state
        # This needs to be done inside the loop because objects' positions change
        blue_objects = find_connected_components(grid, blue_color)

        # If there are no blue objects left to move, the simulation is finished
        if not blue_objects:
            break

        # Sort objects by their lowest point (maximum row index) in descending order.
        # This ensures we attempt to move the objects closest to the bottom first.
        blue_objects.sort(key=lambda obj: max(r for r, c in obj), reverse=True)

        # Iterate through the objects found (from bottom-most to top-most)
        for obj_coords in blue_objects:
            # Check if the current object can move down one step
            if can_object_move_down(grid, obj_coords):
                # --- Perform the move ---
                # 1. Erase the object from its current position by setting pixels to background color
                for r, c in obj_coords:
                    grid[r, c] = background_color

                # 2. Redraw the object one step lower
                # (The can_object_move_down check already confirmed r+1 is within bounds)
                for r, c in obj_coords:
                    grid[r + 1, c] = blue_color

                # --- Update state and control flow ---
                # Mark that at least one object moved in this pass
                moved_this_pass = True

                # IMPORTANT: Since the grid state has changed (one object moved),
                # the conditions for other objects might have changed. We must restart
                # the process: break out of the inner 'for' loop and begin a new
                # iteration of the outer 'while' loop. This re-finds, re-sorts,
                # and re-evaluates all objects based on the newly updated grid.
                break # Exit the 'for obj_coords...' loop

        # If we completed a full pass through all found objects (the 'for' loop finished
        # without the 'break' being triggered), it means no object could move.
        # The grid configuration is stable.
        if not moved_this_pass:
            break # Exit the 'while True' loop

    # Return the final stable grid state as a standard Python list of lists
    return grid.tolist()