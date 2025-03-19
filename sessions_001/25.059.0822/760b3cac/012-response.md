# 760b3cac • 012 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous regions (objects) of azure (8), yellow (4), and black (0) pixels.

2.  **Azure Expansion:** Starting from any azure (8) pixel, iteratively expand the azure color to all adjacent black (0) pixels. Continue this expansion until no more black (0) pixels are adjacent to any azure (8) pixel. This is a "flood fill" operation.

3.  **Yellow Preservation:** The yellow (4) pixels remain unchanged throughout the process. They act as boundaries for the azure expansion.

4. **Black background:** The black (0) pixels are replaced by the expanding azure.
"""

import numpy as np

def flood_fill(grid, r, c, target_color, replacement_color):
    """
    Performs a flood fill operation on the grid.

    Args:
        grid: The 2D numpy array representing the grid.
        r: Starting row index.
        c: Starting column index.
        target_color: The color to be replaced.
        replacement_color: The color to replace with.
    """
    rows, cols = len(grid), len(grid[0])
    if r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != target_color:
        return

    grid[r, c] = replacement_color

    # Recursively fill adjacent pixels
    flood_fill(grid, r + 1, c, target_color, replacement_color)
    flood_fill(grid, r - 1, c, target_color, replacement_color)
    flood_fill(grid, r, c + 1, target_color, replacement_color)
    flood_fill(grid, r, c - 1, target_color, replacement_color)

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the first azure pixel to start flood fill
    start_r, start_c = -1, -1
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 8:
                start_r, start_c = r, c
                break  # Start from the first 8 we find.
        if start_r != -1:
          break
    
    #Perform flood fill if an azure pixel was found
    if start_r != -1:
        flood_fill(output_grid, start_r, start_c, 0, 8)

    return output_grid
```
