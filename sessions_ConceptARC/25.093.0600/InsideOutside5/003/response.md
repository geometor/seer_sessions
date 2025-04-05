Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Identify all connected non-zero objects using 8-way connectivity.
Keep an object if and only if none of its adjacent cells (8-way connectivity) 
are background cells (0) that are connected (via an 8-way path of 0s) 
to the border of the grid. Remove all other objects, replacing their 
cells with 0 in the output grid.
"""

def _find_neighbors(grid_shape, object_coords):
    """
    Finds all unique neighboring cells (8-way adjacency) adjacent to any cell
    of the object, excluding cells that are part of the object itself.

    Args:
        grid_shape (tuple): The (rows, cols) shape of the grid.
        object_coords (set): A set of (row, col) tuples representing the object's cells.

    Returns:
        set: A set of (row, col) tuples representing unique neighbor cells.
    """
    rows, cols = grid_shape
    neighbors = set()
    # Define 8 directions (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]

    for r, c in object_coords:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                # Add if it's not part of the object itself
                if neighbor_coord not in object_coords:
                    neighbors.add(neighbor_coord)
    return neighbors

def _find_objects(grid, visited_mask):
    """
    Finds all distinct connected non-zero objects in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        visited_mask (np.array): A boolean array to track visited cells across calls.

    Yields:
        tuple: A tuple containing (object_color, object_coords_set) for each object found.
    """
    rows, cols = grid.shape
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited_mask[r, c]:
                object_color = grid[r, c]
                object_coords = set()
                q = deque([(r, c)])
                visited_mask[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    object_coords.add((curr_r, curr_c))

                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        if (0 <= nr < rows and 0 <= nc < cols and
                                grid[nr, nc] == object_color and
                                not visited_mask[nr, nc]):
                            visited_mask[nr, nc] = True
                            q.append((nr, nc))
                
                yield (object_color, object_coords)


def _flood_fill_exterior_background(grid):
    """
    Performs flood fill from border zeros to mark exterior background.

    Args:
        grid (np.array): The input grid.

    Returns:
        np.array: A boolean array where True indicates an exterior background cell.
    """
    rows, cols = grid.shape
    exterior_bg = np.zeros_like(grid, dtype=bool)
    q = deque()
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # Add all border zeros to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not exterior_bg[r, c]:
                exterior_bg[r, c] = True
                q.append((r, c))
    for c in range(cols): # Avoid double-adding corners
        for r in [0, rows - 1]:
             if grid[r, c] == 0 and not exterior_bg[r, c]:
                exterior_bg[r, c] = True
                q.append((r, c))

    # Perform BFS for background connected to border
    while q:
        curr_r, curr_c = q.popleft()
        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr, nc] == 0 and not exterior_bg[nr, nc]):
                exterior_bg[nr, nc] = True
                q.append((nr, nc))

    return exterior_bg


def transform(input_grid):
    """
    Filters the grid to keep only objects not adjacent to exterior background.

    Args:
        input_grid (list of lists): The input 2D grid.

    Returns:
        list of lists: The transformed 2D grid.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    output_grid = np.zeros_like(grid)
    
    # 1. Mark exterior background cells
    exterior_bg_mask = _flood_fill_exterior_background(grid)

    # 2. Find all objects and check their neighbors
    visited_obj_mask = np.zeros_like(grid, dtype=bool) # Track visited cells for object finding
    
    for obj_color, obj_coords in _find_objects(grid, visited_obj_mask):
        # 3a. Find neighbors of the current object
        neighbor_coords = _find_neighbors(grid.shape, obj_coords)

        # 3b. Check if any neighbor is an exterior background cell
        is_adjacent_
---
