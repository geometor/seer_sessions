# 3c9b0459 • 006 • refine_coder

---
```python
"""
The transformation rule identifies 2x1 or 2x2 azure rectangles within the input grid. If a 2x1 azure rectangle is found, the row containing that rectangle is duplicated resulting in a 2x2 azure rectangle. If a 2x2 azure rectangle already exists, the output includes a copy of the row containing the rectangle. The dimensions of the grid otherwise remain the same.
"""

import numpy as np

def find_azure_rectangles(grid):
    """Finds 2x1 and 2x2 azure rectangles in the grid."""
    azure_rects = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for r in range(rows):
        for c in range(cols - 1):
            if grid[r][c] == 8 and grid[r][c+1] == 8:
                # Check for 2x1
                if r + 1 < rows:
                  if not (grid[r+1][c] == 8 and grid[r+1][c+1] == 8):
                    azure_rects.append((r, c, 2, 1))  # (row, col, width, height)
                # Check for 2x2
                if r + 1 < rows:
                    if grid[r+1][c] == 8 and grid[r+1][c+1] == 8:
                      azure_rects.append((r,c,2,2))
    return azure_rects

def transform(input_grid):
    # Convert input grid to numpy array
    input_array = np.array(input_grid)

    # Find azure rectangles.
    azure_rects = find_azure_rectangles(input_array.tolist())

    # Initialize output grid as a copy of the input
    output_grid = input_array.tolist()

    rows_added = 0
    for rect in azure_rects:
        row, col, width, height = rect
        
        output_grid.insert(row + rows_added + 1, input_grid[row + rows_added])
        rows_added+=1


    return output_grid
```
