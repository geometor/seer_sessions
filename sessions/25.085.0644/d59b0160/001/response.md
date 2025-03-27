```python
import numpy as np
from collections import deque

def find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color considered as background.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of pixels belonging to a single object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If the pixel is not background and not visited yet
            if grid[r, c] != background_color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the object
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object.add((row, col))

                    # Check neighbors (4-directional connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # If neighbor is part of the object and not visited
                            if grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Check diagonal neighbors (include 8-directional connectivity)
                q = deque(list(current_object)) # Re-seed queue with all current object pixels
                processed_for_diag = set(current_object) # Keep track to avoid redundant checks

                while q:
                    row, col = q.popleft()

                    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                         nr, nc = row + dr, col + dc
                         # Check grid bounds
                         if 0 <= nr < rows and 0 <= nc < cols:
                             # If diagonal neighbor is part of the object and not visited
                             if grid[nr, nc] != background_color and not visited[nr, nc]:
                                 visited[nr, nc] = True
                                 current_object.add((nr, nc))
                                 processed_for_diag.add((nr,nc)) # Add to the set for diagonal checks
                                 q.append((nr, nc)) # Add to queue to check its neighbours too

                if current_object:
                    objects.append(current_object)
    return objects

def contains_color(grid, obj_coords, color_to_check):
    """Checks if any pixel in the object has the specified color."""
    for r, c in obj_coords:
        if grid[r, c] == color_to_check:
            return True
    return False

def touches_border(obj_coords, grid_shape):
    """Checks if any pixel in the object touches the grid border."""
    rows, cols = grid_shape
    for r, c in obj_coords:
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return True
    return False

def transform(input_grid):
    """
    Identifies contiguous objects of non-background colors (not orange/7).
    An object is removed (replaced with the background color orange/7) if it meets two conditions:
    1. It contains at least one white (0) pixel.
    2. It does not touch any of the four borders of the grid.
    Objects that do not meet both conditions remain unchanged.
    """
    # Convert input list of lists to numpy array if necessary
    if not isinstance(input_grid, np.ndarray):
        grid = np.array(input_grid, dtype=int)
    else:
        grid = input_grid.copy() # Ensure we work with a copy if it's already numpy

    output_grid = grid.copy()
    rows, cols = grid.shape
    background_color = 7
    white_color = 0

    # Find all distinct objects (contiguous non-background pixels)
    objects = find_objects(grid, background_color)

    # Iterate through each found object
    for obj_coords in objects:
        # Check condition 1: Does the object contain white?
        has_white = contains_color(grid, obj_coords, white_color)

        # Check condition 2: Does the object touch the border?
        touches = touches_border(obj_coords, (rows, cols))

        # If object contains white AND does NOT touch the border, remove it
        if has_white and not touches:
            # Replace object pixels with background color in the output grid
            for r, c in obj_coords:
                output_grid[r, c] = background_color

    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists as per standard ARC format
```