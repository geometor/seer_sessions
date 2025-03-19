# aba27056 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all connected regions (objects) of non-zero pixels in the input grid.
2.  **Identify Background:** Locate all regions (objects) of pixels with zero value
3. **Outer Border Insertion**: For every background (color 0) pixel that is directly adjacent (not diagonal) to any non-zero pixel, change color to 4 (yellow). If non-zero pixel is already adjacent to existing 4 pixel, do not perform change
4. **Inner Border Insertion**: For every non-zero pixel that is directly adjacent (not diagonal) to any background (color 0) pixel, change color to 4 (yellow).
5.  **Output:** Return the modified grid.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c))  # Down
    if c > 0:
        neighbors.append((r, c - 1))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the border insertion rule."""
    
    input_grid = np.array(input_grid) # ensure numpy array
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Outer Border Insertion (for background pixels)
            if input_grid[r, c] == 0:
                for nr, nc in get_neighbors(input_grid, r, c):
                    if input_grid[nr, nc] != 0 :
                        output_grid[r,c] = 4
                        break # only insert one border
            # Inner border insertion (for non zero pixels)
            elif input_grid[r,c] != 0 and input_grid[r,c] != 4:
                for nr, nc in get_neighbors(input_grid, r, c):
                    if input_grid[nr, nc] == 0:
                        output_grid[r,c] = 4
                        break

    return output_grid.tolist()
```
