# 5c0a986e • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule identifies 2x2 squares in the input grid, expands them by one cell in all directions, and then places pixels of the original square's color at the top-left and bottom-right corners of the expanded area in the output grid.
"""

import numpy as np

def find_squares(grid, size=2):
    """Finds all squares of the specified size in the grid."""
    squares = []
    for r in range(grid.shape[0] - size + 1):
        for c in range(grid.shape[1] - size + 1):
            if np.all(grid[r:r+size, c:c+size] == grid[r, c]) and grid[r,c] != 0:
                squares.append((grid[r, c], (r, c)))
    return squares

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    squares = find_squares(input_grid)

    for color, (r, c) in squares:
        # Calculate the expanded corners
        top_left = (r - 1, c - 1)
        bottom_right = (r + 2, c + 2)

         #check for bounds and set pixels if within 0 - 9 bounds
        if 0 <= top_left[0] < output_grid.shape[0] and 0 <= top_left[1] < output_grid.shape[1]:
              output_grid[top_left[0], top_left[1]] = color
        if 0 <= bottom_right[0] < output_grid.shape[0] and 0 <= bottom_right[1] < output_grid.shape[1]:
          output_grid[bottom_right[0]-1, bottom_right[1]-1] = color
        
        # setting expanded top right
        top_right = (r-1, c + 2)
        if 0 <= top_right[0] < output_grid.shape[0] and 0 <= top_right[1] < output_grid.shape[1]:
              output_grid[top_right[0], top_right[1]-1] = color
        
        #setting lower left
        bottom_left = (r + 2, c -1)
        if 0 <= bottom_left[0] < output_grid.shape[0] and 0 <= bottom_left[1] < output_grid.shape[1]:
          output_grid[bottom_left[0]-1, bottom_left[1]] = color
    return output_grid
```
