```python
import numpy as np
from collections import deque

"""
Identify an object B completely enclosed within another object A, where A and B
have different non-white colors, and output the color of B. An object is
enclosed if all its adjacent (including diagonal) pixels are either part of
the object itself or part of the enclosing object. If no such enclosure of a
non-white object by another non-white object exists, output a 2x2 white grid.
"""

def find_objects(grid):
    """
    Finds all distinct contiguous objects of non-white colors in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents an object
              and contains (color, set_of_coordinates).
              Returns an empty list if the grid is empty or contains only white.
    """
    if grid is None or grid.size == 0:
        return []

    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If the pixel is non-white (not 0) and not yet visited
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = row + dr, col + dc
                            
                            # Check boundaries
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if neighbor is the same color and not visited
                                if grid[nr, nc] == color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    obj_coords.add((nr, nc))
                                    q.append((nr, nc))
                                    
                if obj_coords:
                    objects.append((color, obj_coords))
                    
    return objects

def is_enclosed(obj_b_coords, obj_a_coords, grid_shape):
    """
    Checks if object B is completely enclosed by object A.

    Args:
        obj_b_coords (set): Set of coordinates for object B.
        obj_a_coords (set): Set of coordinates for object A.
        grid_shape (tuple): The dimensions (rows, cols) of the grid.

    Returns:
        bool: True if object B is enclosed by object A, False otherwise.
    """
    rows, cols = grid_shape
    
    # Iterate through each pixel of object B
    for r, c in obj_b_coords:
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                
                nr, nc = r + dr, c + dc
                
                # Check boundaries - if a neighbor is outside, it cannot be enclosed
                if not (0 <= nr < rows and 0 <= nc < cols):
                   return False # Should ideally not happen if object B is within grid

                neighbor_coord = (nr, nc)

                # The neighbor must be part of B or part of A
                if neighbor_coord not in obj_b_coords and neighbor_coord not in obj_a_coords:
                    return False # Found a neighbor that is not A or B, so not enclosed

    # If all neighbors of all pixels in B are either B or A, it's enclosed
    return True


def transform(input_grid):
    """
    Transforms the input grid based on the enclosure rule.

    Finds a non-white object B enclosed by a different non-white object A.
    If found, returns a 1x1 grid with the color of B.
    Otherwise, returns a 2x2 white grid.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    
    # Find all non-white objects in the input grid
    objects = find_objects(input_grid)
    grid_shape = input_grid.shape

    # Iterate through all pairs of distinct objects (A, B)
    for i in range(len(objects)):
        color_a, coords_a = objects[i]
        for j in range(len(objects)):
            # Don't compare an object with itself
            if i == j:
                continue
                
            color_b, coords_b = objects[j]

            # Check if colors are different (and both non-white, which is guaranteed by find_objects)
            if color_a != color_b:
                # Check if object B is enclosed by object A
                if is_enclosed(coords_b, coords_a, grid_shape):
                    # If enclosed, return a 1x1 grid with the color of object B
                    return np.array([[color_b]], dtype=int)

    # If no such enclosure was found after checking all pairs
    # Return the default 2x2 white grid
    return np.zeros((2, 2), dtype=int)

```