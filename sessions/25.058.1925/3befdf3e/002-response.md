# 3befdf3e • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify the Inner Shape: Locate the contiguous block of pixels at the center of the grid that has a different color than its immediate surrounding pixels (the outer shape).
2. Identify the Outer Shape: Identify the contiguous block of pixels that directly surrounds and is adjacent to the inner shape.
3. Expand the Inner Shape: Replace the pixels of the outer shape, which is directly adjacent to original inner shape, with the original color of the inner shape.
4. Shift the Outer Shape: Create a new outer border by replacing background colored (0) which is direct adjacent to the new inner shape. The new border is same color as the original outer shape.
5. Background Remains: All other pixels, which represent the background (value 0), remain unchanged.
"""

import numpy as np
from collections import deque

def find_object(grid, start_row, start_col):
    """
    Finds a contiguous object in the grid starting from a given cell,
    using Breadth-First Search (BFS).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque([(start_row, start_col)])
    visited[start_row, start_col] = True
    object_pixels = []
    color = grid[start_row, start_col]

    while queue:
        r, c = queue.popleft()
        object_pixels.append((r, c))

        # Check adjacent cells
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc] and grid[nr, nc] == color:
                visited[nr, nc] = True
                queue.append((nr, nc))

    return object_pixels, color
    
def get_neighbors(grid, r, c):
    """
    get all the valid neighbors of a cell, regardless of color
    """
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr,nc))
    return neighbors

def find_inner_and_outer_objects(grid):
    """
    Finds the inner and outer objects based on the center and adjacency.
    Assumes there's an inner and outer shape.
    """
    rows, cols = grid.shape
    center_row, center_col = rows // 2, cols // 2
    
    # Find what is in the center of grid
    if grid[center_row,center_col] == 0:
        return None, None, None, None
    
    inner_object, inner_color = find_object(grid, center_row, center_col)
    
    # use first neighbor that is not the same color to start to define outer
    outer_color = None
    outer_start = None
    
    for r,c in inner_object:
        for nr, nc in get_neighbors(grid, r, c):
            if grid[nr,nc] != inner_color:
                outer_start = (nr,nc)
                outer_color = grid[nr,nc]
                break # found outer, done searching
        if outer_start:
            break
    
    if not outer_start: # no outer found, we are done
        return None, None, None, None
        
    outer_object, _ = find_object(grid, outer_start[0], outer_start[1])
    
    return inner_object, inner_color, outer_object, outer_color

def transform(input_grid):
    """
    Expands the inner shape by one layer, consuming the innermost layer of the
    outer shape. The outer shape then shifts outwards by one layer,
    maintaining its original color. The background (0) is preserved except
    where overwritten by expansion.
    """
    # initialize output_grid
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # find inner and outer objects
    inner_object, inner_color, outer_object, outer_color = find_inner_and_outer_objects(grid)
    if not inner_object: #we didn't find inner and outer, do nothing
        return output_grid
    
    # Expand inner shape by coloring the adjacent outer pixels
    for r, c in outer_object:
        output_grid[r, c] = inner_color

    # Find neighbors of expanded inner object, set to original outer color
    expanded_inner = []
    for r,c in outer_object:
        expanded_inner.extend(get_neighbors(grid,r,c))
    
    for r,c in expanded_inner:
        if output_grid[r,c] == 0:
            output_grid[r,c] = outer_color    

    return output_grid.tolist()
```
