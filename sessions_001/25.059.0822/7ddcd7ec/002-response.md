# 7ddcd7ec • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying a colored object (contiguous block of non-zero pixels) in the input grid and extending it diagonally downwards and to the right, creating a diagonal line of the object. The diagonal extension continues to the edges of the grid.
"""

import numpy as np

def find_object(grid):
    """Finds the first object in a grid and returns its color, bounding box, and pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                pixels = []
                min_row, max_row = rows, -1
                min_col, max_col = cols, -1

                stack = [(r, c)]
                while stack:
                    row, col = stack.pop()
                    if 0 <= row < rows and 0 <= col < cols and grid[row, col] == color and not visited[row, col]:
                        visited[row, col] = True
                        pixels.append((row, col))
                        min_row = min(min_row, row)
                        max_row = max(max_row, row)
                        min_col = min(min_col, col)
                        max_col = max(max_col, col)
                        
                        stack.extend([(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)])

                return color, (min_row, max_row, min_col, max_col), pixels
    return None, None, None

def transform(input_grid):
    """Transforms the input grid by extending a colored object diagonally."""
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the first object in the grid
    color, bbox, pixels = find_object(input_grid)
    
    if color is None:
       return output_grid

    # Get original object dimensions and starting position
    min_row, max_row, min_col, max_col = bbox
    
    # Calculate the offset for diagonal extension
    row_offset, col_offset = 0,0

    # Extend the object diagonally downwards and to the right
    while min_row + row_offset < output_grid.shape[0] and min_col + col_offset < output_grid.shape[1]:

      for r,c in pixels:
        r_new = r - min_row + min_row + row_offset
        c_new = c - min_col + min_col + col_offset
        if 0 <= r_new < output_grid.shape[0] and 0 <= c_new < output_grid.shape[1]:
            output_grid[r_new, c_new] = color


      row_offset += 1
      col_offset += 1

    return output_grid
```
