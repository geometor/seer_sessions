# 694f12f3 • 002 • example_2 • investigate_coder

---
```python
"""
Identifies rectangular regions of yellow (4) in the input grid.
If a yellow rectangle is in the top-left, its inner 2x2 center is filled with blue (1).
If a yellow rectangle is in the bottom-right, its inner area (2 rows high) is filled with red (2).
"""

import numpy as np

def find_rectangles(grid, color):
    """Finds rectangles of a specific color in the grid."""
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start of a potential rectangle
                width = 0
                while c + width < cols and grid[r, c + width] == color and not visited[r, c + width]:
                    width += 1

                height = 0
                while r + height < rows and all(grid[r + height, c:c+width] == color) and not any(visited[r + height, c:c+width]):
                    height += 1

                # Mark as visited
                visited[r:r+height, c:c+width] = True
                rectangles.append((r, c, width, height))
    return rectangles

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    yellow_rectangles = find_rectangles(input_grid, 4)
    rows, cols = input_grid.shape

    for r, c, width, height in yellow_rectangles:
        # Determine position and apply fill
        if r < rows / 2 and c < cols / 2: # Top-left
             if height >= 2 and width >=2 :
                output_grid[r+1:min(r+height-1,r+3), c+1:min(c+width-1, c+3)] = 1
        elif r >= rows/2 and c >= 0: #original logic, relaxed condition to allow fill
            if height >= 2:
                 output_grid[r+1:r+height-1, c+1:c+width-1] = 2


    return output_grid
```
