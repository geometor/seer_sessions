# fcc82909 • 016 • example_3 • investigate_coder

---
```python
"""
Identifies 2x2 colored squares in the input grid, then fills the connecting '0' (white) areas with '3' (green), effectively connecting the original objects with a green background while preserving the original objects.
"""

import numpy as np

def find_objects(grid):
    # Find 2x2 colored squares
    objects = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            square = grid[r:r+2, c:c+2]
            if np.all(square > 0) and np.all(square == square[0,0])==False: # Check if all elements are same and > 0
                objects.append((r, c))
    return objects

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the 2x2 objects
    objects = find_objects(output_grid)

    # Flood fill with green (3), starting from white (0) areas, bounded by objects
    visited = np.zeros_like(output_grid, dtype=bool)
    
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def flood_fill(r, c):
        if not is_valid(r, c) or visited[r, c] or output_grid[r,c] != 0 :
            return
        
        visited[r,c] = True
        output_grid[r,c] = 3
        
        flood_fill(r + 1, c)
        flood_fill(r - 1, c)
        flood_fill(r, c + 1)
        flood_fill(r, c - 1)
        
    for r in range(rows):
        for c in range(cols):
             if output_grid[r,c] == 0:
                flood_fill(r,c)
    

    return output_grid
```
