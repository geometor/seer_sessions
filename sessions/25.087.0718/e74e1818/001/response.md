```python
import numpy as np
from collections import deque

"""
Identifies distinct connected objects of the same non-background color in the 
input grid. For each object, determines its vertical extent (minimum and maximum
row indices). Then, for each unique vertical extent found across all objects, 
reverses the order of the corresponding horizontal rows from the input grid and 
places them into the output grid at the same vertical position.
"""

def find_objects(grid):
    """
    Finds all distinct connected objects of the same non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples 
                   representing the coordinates of a single object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Found the start of a potential new object
                current_color = grid[r, c]
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == current_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object_coords:
                    objects.append(current_object_coords)
    
    return objects

def transform(input_grid):
    """
    Vertically flips the rows within the vertical bounds of each distinct object 
    found in the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    
    # Initialize output_grid as a copy of the input grid.
    # Transformations will be applied directly to this copy.
    output_grid = np.copy(input_grid)
    
    # Find all distinct objects (connected components of the same color)
    objects = find_objects(input_grid)
    
    # Determine the vertical extents (min_row, max_row) for each object
    object_extents = set() # Use a set to automatically handle duplicate extents
    for obj_coords in objects:
        if not obj_coords:
            continue
        rows = [r for r, c in obj_coords]
        min_row = min(rows)
        max_row = max(rows)
        object_extents.add((min_row, max_row))
        
    # Apply the row reversal for each unique vertical extent
    # Sort extents by min_row to process consistently, though order shouldn't matter
    # if extents don't overlap in complex ways (which they don't in examples).
    sorted_extents = sorted(list(object_extents))

    for min_row, max_row in sorted_extents:
        # Extract the slice of rows from the original input grid
        input_row_slice = input_grid[min_row : max_row + 1, :]
        
        # Reverse the order of rows in the slice
        reversed_row_slice = np.flipud(input_row_slice)
        
        # Place the reversed slice into the output grid
        output_grid[min_row : max_row + 1, :] = reversed_row_slice
        
    return output_grid

```