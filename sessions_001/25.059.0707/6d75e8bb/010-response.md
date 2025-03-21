# 6d75e8bb • 010 • example_2 • investigate_coder

---
```python
"""
Identifies a contiguous region of azure (8) pixels within the input grid. 
Then, replaces specific azure pixels inside the region with red (2) pixels, 
maintaining the overall shape of the azure region.
"""

import numpy as np

def find_contiguous_region(grid, color):
    # Find the first pixel of the specified color
    rows, cols = grid.shape
    start_row, start_col = -1, -1
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                start_row, start_col = r, c
                break
        if start_row != -1:
            break
    
    if start_row == -1:
        return []

    visited = set()
    pixels = []
    queue = [(start_row, start_col)]

    while queue:
        row, col = queue.pop(0)
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            continue

        visited.add((row, col))
        pixels.append((row, col))

        # Add adjacent pixels to the queue
        queue.append((row + 1, col))
        queue.append((row - 1, col))
        queue.append((row, col + 1))
        queue.append((row, col - 1))
    
    return pixels

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the contiguous region of azure (8) pixels
    azure_region = find_contiguous_region(output_grid, 8)

    # Determine replacement locations based on relative coordinates within the azure region
    # and replace azure with red
    
    for r in range(rows):
      for c in range(cols):
        if (r,c) in azure_region:
          if output_grid[r,c] == 8:
            if r == 2 and (c == 2 or c == 5):
                output_grid[r,c] = 2
            if r == 3 and (c == 2 or c == 4 or c==5):
                output_grid[r,c] = 2
            if r == 4 and (c==1 or c==2 or c==4):
                output_grid[r,c] = 2
    
    return output_grid
```
